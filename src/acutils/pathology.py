# Functions prefixed with "tmnt" are treatments and must have those parameters:
#  - src: absolute path to the file that will be processed (str)
#  - dstdir: absolute path to the directory that should contain new files (str)
# Also, nothing should be returned.

import math
import numpy as np
import os

try:
    import cv2
except ImportError:
    print("|WRN| You must install 'opencv-python' (cv2) to use pathology module. "
          "Leaving.")
    exit()

try:
    from openslide import OpenSlide
except ImportError:
    print("|WRN| You must install 'openslide-python' to use pathology module. "
          "Be careful, it also requires Openslide installation on your computer"
          ", the 'openslide-python' Python library is just a mapping. Leaving.")
    exit()

try:
    from PIL import Image
except ImportError:
    print("|WRN| You must install 'Pillow' to use pathology module. "
          "Leaving.")
    exit()
    
try:
    from skimage.io import imread, imsave
    from skimage.data import skin as skimgskin
except ImportError:
    print("|WRN| You must install 'scikit-image' to use pathology module. "
          "You might need a skimage optinal dependencie: 'pooch'. Leaving.")
    exit()

from . import gpu

Image.MAX_IMAGE_PIXELS = None
import numpy as aunp
import skimage as auski
gpu.set_gpu_computation() # if True import cucim.skimage as auski and cupy as aunp



def update_ref_image(img_path=None):
    '''
    Change reference image using when calling harmonize function.
    If you called `gpu.set_gpu_computation(activate=True)`, calling will load
    the image on the GPU (using cupy instead of numpy).
    
    PARAMETERS
    ----------    
	(str) img_path=None:
		Absolute path to the image that will be the reference to harmonize.
    
    RETURNS
    -------
	None    
    '''
    global IHC_REF_IMAGE, IHC_H_REF, IHC_E_REF, IHC_D_REF
    if img_path is None:
        IHC_REF_IMAGE = aunp.array(IHC_REF_IMAGE) # for switching from CPU to GPU
    else:
        IHC_REF_IMAGE = aunp.array(imread(img_path))
    
    ihc_hed = (auski.color.rgb2hed(IHC_REF_IMAGE))
    null = aunp.zeros_like(ihc_hed[:, :, 0])
    IHC_H_REF = auski.color.hed2rgb(aunp.stack((ihc_hed[:, :, 0], null, null), 
                                               axis=-1))
    IHC_E_REF = auski.color.hed2rgb(aunp.stack((null, ihc_hed[:, :, 1], null),
                                               axis=-1))
    IHC_D_REF = auski.color.hed2rgb(aunp.stack((null, null, ihc_hed[:, :, 2]),
                                               axis=-1))



IHC_REF_IMAGE = skimgskin()
update_ref_image() # default ref image is skimage.data.skin()



def harmonize(img):
    '''
    Harmonize the image through hed conversion, erase the color and keep 
    the stains. Then match the histogram with a reference image.
    You can change the reference image calling update_ref_image function.
    
    PARAMETERS
    ----------    
	(numpy.array or cupy.array of int) img:
		RGB image to harmonize.
    
    RETURNS
    -------
	None
    

    REFERENCES
    ----------
        [1] A. C. Ruifrok and D. A. Johnston:
            "Quantification of histochemical staining by color deconvolution.," 
            Analytical and quantitative cytology and histology / the International 
            Academy of Cytology [and] American Society of Cytology, vol. 23, no. 4, 
            pp. 291-9, Aug. 2001.
    '''
    ihc_hed = (auski.color.rgb2hed(img))
    null = aunp.zeros_like(ihc_hed[:, :, 0])

    ihc_h = auski.color.hed2rgb(
                    aunp.stack((ihc_hed[:, :, 0], null, null), axis=-1))
    hist_h = auski.exposure.match_histograms(ihc_h, IHC_H_REF)
    del ihc_h

    ihc_e = auski.color.hed2rgb(
                    aunp.stack((null, ihc_hed[:, :, 1], null), axis=-1))
    hist_e = auski.exposure.match_histograms(ihc_e, IHC_E_REF)
    del ihc_e

    ihc_d = auski.color.hed2rgb(
                    aunp.stack((null, null, ihc_hed[:, :, 2]), axis=-1))
    hist_d = auski.exposure.match_histograms(ihc_d, IHC_D_REF)
    del ihc_d, ihc_hed, null
    
    return (aunp.dstack((hist_h[:, :, 0], hist_e[:, :, 1], hist_d[:, :, 2])
                    )*255).astype(aunp.uint8)



def tmnt_harmonize(src, dstdir):
    '''
    Read a segment, harmonize it calling harmonize function, then save it.
    
    PARAMETERS
    ----------    
	(str) src:
		Absolute path to the file that will be processed.
    
	(str) dstdir:
		Absolute path to the directory that should contain the new file.
    
    RETURNS
    -------
	None    
    '''
    img = harmonize(aunp.array(imread(src)))
    imsave(os.path.join(dstdir, os.path.basename(src)), 
            gpu.cupy_to_numpy(img), check_contrast=False)



def get_preview(slide, lvl=-1, divider=None):
    '''
    Read the slide and returns it with low resolution.
    
    PARAMETERS
    ----------    
	(openslide.OpenSlide) slide:
		The slide.
    
	(int) lvl=-1:
		Level taken.
    
	(float) divider=None:
		Scale the preview by dividing the slide. The new width and height will be 
            the old ones divided by the divider. It is also the size of the area 
            used to load the slide, to ensure no memory overload.

    RETURNS
    -------    
	(numpy.array or cupy.array of int) preview:
		Scaled loaded slide.    
    '''
    if divider is None:
        preview = aunp.array(np.asarray(slide.get_thumbnail(
                                            slide.level_dimensions[lvl])))
        
    else:
        width, height = slide.level_dimensions[lvl]
        pw, ph = int(width/divider), int(height/divider) # size of the preview
        tw, th = int(pw/divider),  int(ph/divider) # tile size from the preview
        preview = aunp.zeros((pw, ph, 3), dtype=aunp.uint8) + 255

        # Update preview area per area
        for i in range(divider):
            for j in range(divider):
                preview[j*th:(j+1)*th, i*tw:(i+1)*tw] = aunp.array(
                    cv2.resize(
                        np.array(slide.read_region((i*pw,j*ph), 0, (pw, ph)), 
                            dtype=np.uint8)[:,:,:3], 
                        dsize=(tw, th), 
                        interpolation=cv2.INTER_NEAREST
                    )
                )
    return preview



def get_cleaned_binary(preview, fp_val=16, sigma=2):
    '''
    Split foreground (1) and background (0) using mathematic morphology.
    
    PARAMETERS
    ----------    
	(numpy.array of cupy.array of int) preview:
		Fully loaded slide with low resolution.
    
	(int) fpval=16:
		Value that is used to creates footprints for segmentation.
    
	(float) sigma=2:
		Value for gaussian filter (applied on the slide before segmentation).
    
    RETURNS
    -------    
	(numpy.array of cupy.array of bool) bw:
		Binary image from the preview.    
    '''
    bw = auski.color.rgb2gray(preview)
    bw = auski.filters.threshold_otsu(bw) > auski.filters.gaussian(bw, sigma)
    bw = auski.morphology.opening(bw, auski.morphology.square(fp_val))
    bw += auski.segmentation.clear_border(~bw)
    bw = auski.morphology.dilation(bw, auski.morphology.disk(int(fp_val*0.25)))
    return bw



def mask_rgb(rgb, mask):
    '''
    Mask rgb image with a binary image.

    PARAMETERS
    ----------    
	(numpy.array or cupy.array of int) rgb:
		RGB image.
    
	(numpy.array or cupy.array of bool) mask:
		Binary image.

    RETURNS
    -------    
	(numpy.array or cupy.array of uint8) masked_rgb:
		RGB image masked with the binary image.    
    '''
    mask_rgb = aunp.repeat(mask[...,None],3,axis=2)
    return mask_rgb*rgb + (~mask_rgb*255).astype(aunp.uint8)



def browse_segments(slide, bw, lvl=0, required_area=10000, do_harmonize=False):
    '''
    Find slices inside the preview and load it from de slide.

    PARAMETERS
    ----------    
	(openslide.OpenSlide) slide:
		The slide.
    
	(numpy.array of cupy.array of bool) bw:
		Binary image from the preview.
    
	(int) lvl=0:
		level taken.
    
	(int) required_area=10000:
		Minimum area (pixels) to keep the slice.
    
	(bool) do_harmonize=False:
		Harmonize slices using harmonize function.
    
    RETURNS
    -------    
	(generator of numpy.array of uint8) Segments:
		Found slices.    
    '''
    width, height = slide.level_dimensions[lvl]
    new_width, new_height = bw.shape[1], bw.shape[0] # for preview
    xresolution = width / new_width
    yresolution = height / new_height
    for region in auski.measure.regionprops(auski.measure.label(bw)):
        x, y = region.bbox[:2]
        w, h = region.bbox[2] - x, region.bbox[3] - y
        if w*h > required_area:
            x = int(x*xresolution)
            y = int(y*yresolution)
            w = int(w*xresolution)
            h = int(h*yresolution)
            segment_mask = auski.transform.resize(region.image, (w,h))
            if do_harmonize:
                segment = harmonize(aunp.array(np.array(slide.read_region(
                    (y,x), 0, (h, w)), dtype=aunp.uint8)[:,:,:3]))
            else:
                segment = aunp.array(np.array(slide.read_region(
                    (y,x), 0, (h, w)), dtype=aunp.uint8)[:,:,:3])
            yield gpu.cupy_to_numpy(mask_rgb(rgb=segment, mask=segment_mask))



def load_slice_preview_and_ext(src, lvl, divider=None, device=None):
    '''
    Load slide file and extract a preview of it using get_preview function.

    PARAMETERS
    ----------    
	(str) src:
		Absolute path to the slide.
    
	(int) lvl:
		Slide level taken.
    
	(float) divider=None:
		Scale the preview by dividing the slide.
    
	(int) device=None:
		Taken GPU.

    RETURNS
    -------    
	(openslide.OpenSlide) slide:
		The slide.
    
	(numpy.array of cupy.array of int) preview:
		Fully loaded slide with low resolution.
    
	(str) slide_ext:
		Slide extension.    
    '''
    gpu.select_device(device)
    slide = OpenSlide(src)
    preview = get_preview(slide, lvl, divider)
    _, slide_ext = os.path.splitext(src)
    return slide, preview, slide_ext



def tmnt_save_preview_from_slide(src, dstdir, lvl, divider=None, ext="png", device=None):
    '''
    Load slide preview and save it.
    
    PARAMETERS
    ----------    
	(str) src:
		Absolute path to the slide.
    
	(str) dstdir:
		Absolute path to the directory where to save the preview.
    
	(int) lvl:
		Slide level taken.
    
	(float) divider=None:
		Scale the preview by dividing the slide.
    
	(str) ext="png":
		Saved preview extension.
    
	(int) device=None:
		Taken GPU.
    
    RETURNS
    -------
	None    
    '''
    _, preview, slide_ext = load_slice_preview_and_ext(src, lvl, divider, device)
    imsave(os.path.join(dstdir, f"{os.path.basename(src)[:-len(slide_ext)]}.{ext}"), 
                    gpu.cupy_to_numpy(preview), check_contrast=False)



def tmnt_save_segments_from_slide(src, dstdir, lvlpreview, lvlsegment, fpval, sigma, 
                                  do_harmonize=False, divider=None, ext="png", device=None):
    '''
    Find slices inside the slide and save them.
    
    PARAMETERS
    ----------    
	(str) src:
		Absolute path to the slide.
    
	(str) dstdir:
		Absolute path to the directory where to save the preview.
    
	(int) lvlpreview:
		Slide level taken for the preview.
    
	(int) lvlsegment:
		Slide level taken for the segment.
    
	(int) fpval:
		Value that is used to creates footprints for segmentation.
    
	(float) sigma:
		Value for gaussian filter (applied on the slide before segmentation).
    
	(bool) do_harmonize=False:
		Harmonize slices using harmonize function.
    
	(float) divider=None:
		Scale the preview by dividing the slide.
    
	(str) ext="png":
		Saved segments extension.
    
	(int) device=None:
		Taken GPU.
    
    RETURNS
    -------
	None    
    '''
    slide, preview, slide_ext = load_slice_preview_and_ext(src, lvlpreview, divider, device)
    bw = get_cleaned_binary(preview, fpval, sigma)
    for i, segment in enumerate(browse_segments(slide, bw, lvlsegment, do_harmonize=do_harmonize)):
        imsave(os.path.join(dstdir, 
                f"{os.path.basename(src)[:-len(slide_ext)]}_{i}.{ext}"), segment,
                check_contrast=False)



def browse_tiles(segment, size=512, blank_tol=0.35):
    '''
    Regulary crop a segment into multiple tiles of same size.

    PARAMETERS
    ----------    
	(numpy.array of int) segment:
		Slice to tile.
    
	(int) size=512:
		Size of each tile.
    
	(float) blank_tol=0.35:
		Percentage of white pixels tolerated for a tile.

    RETURNS
    -------    
	(generator of tuple of int) coordinates:
		Tiles coordinates (x,y).
    - tiles generator of numpy.array of int): Keeped tiles.    
    '''
    width, height = segment.shape[1], segment.shape[0]
    blank_size = size*size*blank_tol # number of pixels that can be white
    
    # Center the tiles (if needed)
    extra_width = width - int(width/size)*size
    left_nudge = int(extra_width/2)
    extra_height = height - int(height/size)*size
    top_nudge = int(extra_height/2)

    # Tile the segment, yield if not too many white pixels
    for x in range(left_nudge, width-size, size):
        for y in range(top_nudge, height-size, size):
            if np.where(segment[y:y+size, x:x+size].sum(axis=2) == 765)[0].shape[0] <= blank_size:
                yield (x,y), segment[y:y+size, x:x+size]



def tmnt_save_tiles_from_segment(src, dstdir, size=512, blank_tol=0.35, ext="png"):
    '''
    Find slices inside the slide and save them.
    
    PARAMETERS
    ----------    
	(str) src:
		Absolute path to the slide.
    
	(str) dstdir:
		Absolute path to the directory where to save the preview.
    
	(int) size=512:
		Size of each tile.
    
	(float) blank_tol=0.35:
		Percentage of white pixels tolerated for a tile.
    
	(str) ext="png":
		Saved tiles extension.
    
    RETURNS
    -------
	None    
    '''
    segment = np.array(imread(src))
    _, segment_ext = os.path.splitext(src)
    for i, (coords,tile) in enumerate(
      browse_tiles(segment, size=size, blank_tol=blank_tol)):
        imsave(os.path.join(dstdir, 
                  f"{os.path.basename(src)[:-len(segment_ext)]}"
                  f"_{i}_x{coords[0]}_y{coords[1]}.{ext}"), tile, 
                  check_contrast=False)