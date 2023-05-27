import cv2
import math
import numpy as np
import os
from openslide import OpenSlide
from PIL import Image
from skimage.io import imread, imsave
from skimage.data import skin as skimgskin

from . import gpu



# A function prefixed with "tmnt" is a treatment function and must have those parameters:
#  - src: absolute path to the file that will be processed (str)
#  - dstdir: absolute path to the directory that should contain new files (str)
# Also, it shouldn't return anything.



Image.MAX_IMAGE_PIXELS = None
import skimage as axskimg
import numpy as axp
gpu.gpu_computation() # if True import cucim.skimage as axskimg and cupy as axp



def update_ref_image(img_path=None):
    '''
    Change reference image using when calling harmonize function.
    \nPARAMETERS
      img_path=None (str): absolute path to the image that will be the reference to harmonize
    \nRETURNS
      df (pandas.DataFrame): formated dataframe
    '''
    global REF_IMAGE, IHC_H_REF, IHC_E_REF, IHC_D_REF
    if img_path is None:
        REF_IMAGE = axp.array(REF_IMAGE) # if called to switch from RAM to GPU
    else:
        REF_IMAGE = axp.array(imread(img_path))
    
    ihc_hed = (axskimg.color.rgb2hed(REF_IMAGE))
    null = axp.zeros_like(ihc_hed[:, :, 0])
    IHC_H_REF = axskimg.color.hed2rgb(axp.stack((ihc_hed[:, :, 0], null, null), axis=-1))
    IHC_E_REF = axskimg.color.hed2rgb(axp.stack((null, ihc_hed[:, :, 1], null), axis=-1))
    IHC_D_REF = axskimg.color.hed2rgb(axp.stack((null, null, ihc_hed[:, :, 2]), axis=-1))


REF_IMAGE = skimgskin()
update_ref_image() # default ref image is skimage.data.skin()



def harmonize(img):
    '''
    Harmonize the image through hed conversion, erase the color and keep the stains.
    Then match the histogram with a reference image.
    You can change the reference image calling update_ref_image function.
    \nPARAMETERS
      img (numpy.array or cupy.array of int): rgb image to harmonize
    \nREFERENCES
      [1] A. C. Ruifrok and D. A. Johnston, "Quantification of histochemical
      staining by color deconvolution.," Analytical and quantitative
      cytology and histology / the International Academy of Cytology [and]
      American Society of Cytology, vol. 23, no. 4, pp. 291-9, Aug. 2001.
    '''
    ihc_hed = (axskimg.color.rgb2hed(img))
    null = axp.zeros_like(ihc_hed[:, :, 0])

    ihc_h = axskimg.color.hed2rgb(axp.stack((ihc_hed[:, :, 0], null, null), axis=-1))
    hist_h = axskimg.exposure.match_histograms(ihc_h, IHC_H_REF)
    del ihc_h

    ihc_e = axskimg.color.hed2rgb(axp.stack((null, ihc_hed[:, :, 1], null), axis=-1))
    hist_e = axskimg.exposure.match_histograms(ihc_e, IHC_E_REF)
    del ihc_e

    ihc_d = axskimg.color.hed2rgb(axp.stack((null, null, ihc_hed[:, :, 2]), axis=-1))
    hist_d = axskimg.exposure.match_histograms(ihc_d, IHC_D_REF)
    del ihc_d, ihc_hed, null
    
    return (axp.dstack((hist_h[:, :, 0], hist_e[:, :, 1], hist_d[:, :, 2])
                    )*255).astype(axp.uint8)



def tmnt_harmonize(src, dstdir):
    '''
    Read a segment, harmonize it calling harmonize function, then save it.
    \nPARAMETERS
      src (str): absolute path to the file that will be processed
      dstdir (str): absolute path to the directory that should contain the new file
    '''
    img = harmonize(axp.array(imread(src)))
    imsave(os.path.join(dstdir, os.path.basename(src)), 
            gpu.cupy_to_numpy(img), check_contrast=False)



def get_preview(slide, lvl=-1, divider=None):
    '''
    Read the slide and returns it with low resolution.
    \nPARAMETERS
      slide (openslide.OpenSlide): the slide
      lvl=-1 (int): level taken
      divider=None (float): scale the preview by dividing the slide
    \nRETURNS
      preview (numpy.array or cupy.array of int): scaled loaded slide
    '''
    if divider is None:
        preview = axp.array(np.asarray(slide.get_thumbnail(slide.level_dimensions[lvl])))
        
    else:
        width, height = slide.level_dimensions[lvl]
        new_width, new_height = int(width/divider), int(height/divider) # slide will be scaled
        amount = math.ceil(divider/4) # read area per area to avoid memory overload

        w, h = int(width/amount), int(height/amount) # area with old scale
        nw, nh = int(new_width/amount),  int(new_height/amount) # area with new scale
        preview = axp.zeros((new_height, new_width, 3), dtype=axp.uint8) + 255

        # Update prew divided area per divided area
        for i in range(amount):
            for j in range(amount):
                preview[j*nh:(j+1)*nh, i*nw:(i+1)*nw] = axp.array(cv2.resize(
                    np.array(slide.read_region((i*w,j*h), 0, (w, h)), dtype=np.uint8)[:,:,:3], 
                    dsize=(nw, nh), interpolation=cv2.INTER_NEAREST))
    return preview



def get_cleaned_binary(preview, fp_val=16, sigma=2):
    '''
    Split foreground (1) and background (0) using mathematic morphology.
    \nPARAMETERS
      preview (numpy.array of cupy.array of int): fully loaded slide with low resolution
      fpval=16 (int): value that is used to creates footprints for segmentation
      sigma=2 (float): value for gaussian filter (applied on the slide before segmentation)
    \nRETURNS
      bw (numpy.array of cupy.array of bool): binary image from the preview
    '''
    bw = axskimg.color.rgb2gray(preview)
    bw = axskimg.filters.threshold_otsu(bw) > axskimg.filters.gaussian(bw, sigma)
    bw = axskimg.morphology.opening(bw, axskimg.morphology.square(fp_val))
    bw += axskimg.segmentation.clear_border(~bw)
    bw = axskimg.morphology.dilation(bw, axskimg.morphology.disk(int(fp_val*0.25)))
    return bw



def mask_rgb(rgb, mask):
    '''
    Mask rgb image with a binary image.
    \nParameters
      rgb (numpy.array or cupy.array of int): rgb image
      mask (numpy.array or cupy.array of bool): binary image
    \nReturns
      masked_rgb (numpy.array or cupy.array of uint8): rgb image masked with the binary image
    '''
    mask_rgb = axp.repeat(mask[...,None],3,axis=2)
    return mask_rgb*rgb + (~mask_rgb*255).astype(axp.uint8)



def browse_segments(slide, bw, lvl=0, required_area=10000, do_harmonize=False):
    '''
    Find slices inside the preview and load it from de slide.
    \nPARAMETERS
      slide (openslide.OpenSlide): the slide
      bw (numpy.array of cupy.array of bool): binary image from the preview
      lvl=0 (int): level taken
      required_area=10000 (int): minimum area (pixels) to keep the slice
      do_harmonize=False (bool): harmonize slices using harmonize function
    \nRETURNS
      segments (generator of numpy.array of uint8): found slices
    '''
    width, height = slide.level_dimensions[lvl]
    new_width, new_height = bw.shape[1], bw.shape[0] # for preview
    xresolution = width / new_width
    yresolution = height / new_height
    for region in axskimg.measure.regionprops(axskimg.measure.label(bw)):
        x, y = region.bbox[:2]
        w, h = region.bbox[2] - x, region.bbox[3] - y
        if w*h > required_area:
            x = int(x*xresolution)
            y = int(y*yresolution)
            w = int(w*xresolution)
            h = int(h*yresolution)
            segment_mask = axskimg.transform.resize(region.image, (w,h))
            if do_harmonize:
                segment = harmonize(axp.array(np.array(slide.read_region(
                    (y,x), 0, (h, w)), dtype=axp.uint8)[:,:,:3]))
            else:
                segment = axp.array(np.array(slide.read_region(
                    (y,x), 0, (h, w)), dtype=axp.uint8)[:,:,:3])
            yield gpu.cupy_to_numpy(mask_rgb(rgb=segment, mask=segment_mask))



def load_slice_preview_and_ext(src, lvl, divider=None, device=None):
    '''
    Load slide file and extract a preview of it using get_preview function.
    \nPARAMETERS
      src (str): absolute path to the slide
      lvl (int): slide level taken
      divider=None (float): scale the preview by dividing the slide
      device=None (int): taken gpu
    \nRETURNS
      slide (openslide.OpenSlide): the slide
      preview (numpy.array of cupy.array of int): fully loaded slide with low resolution
      slide_ext (str): slide extension
    '''
    gpu.select_device(device)
    slide = OpenSlide(src)
    preview = get_preview(slide, lvl, divider)
    _, slide_ext = os.path.splitext(src)
    return slide, preview, slide_ext



def tmnt_save_preview_from_slide(src, dstdir, lvl, divider=None, ext="png", device=None):
    '''
    Load slide preview and save it.
    \nPARAMETERS
      src (str): absolute path to the slide
      dstdir (str): absolute path to the directory where to save the preview
      lvl (int): slide level taken
      divider=None (float): scale the preview by dividing the slide
      ext="png" (str): saved preview extension
      device=None (int): taken gpu
    '''
    _, preview, slide_ext = load_slice_preview_and_ext(src, lvl, divider, device)
    imsave(os.path.join(dstdir, f"{os.path.basename(src)[:-len(slide_ext)]}.{ext}"), 
                    gpu.cupy_to_numpy(preview), check_contrast=False)



def tmnt_save_segments_from_slide(src, dstdir, lvlpreview, lvlsegment, fpval, sigma, 
                                  do_harmonize=False, divider=None, ext="png", device=None):
    '''
    Find slices inside the slide and save them.
    \nPARAMETERS
      src (str): absolute path to the slide
      dstdir (str): absolute path to the directory where to save the preview
      lvlpreview (int): slide level taken for the preview
      lvlsegment (int): slide level taken for the segment
      fpval (int): value that is used to creates footprints for segmentation
      sigma (float): value for gaussian filter (applied on the slide before segmentation)
      do_harmonize=False (bool): harmonize slices using harmonize function
      divider=None (float): scale the preview by dividing the slide
      ext="png" (str): saved segments extension
      device=None (int): taken gpu
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
    \nPARAMETERS
      segment (numpy.array of int): slice to tile
      size=512 (int): size of each tile
      blank_tol=0.35 (float): percentage of white pixels tolerated for a tile
    \nRETURNS
      coordinates (generator of tuple of int): tiles coordinates (x,y)
      tiles generator of numpy.array of int): keeped tiles
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
    \nPARAMETERS
      src (str): absolute path to the slide
      dstdir (str): absolute path to the directory where to save the preview
      size=512 (int): size of each tile
      blank_tol=0.35 (float): percentage of white pixels tolerated for a tile
      ext="png" (str): saved tiles extension
    '''
    segment = np.array(imread(src))
    _, segment_ext = os.path.splitext(src)
    for i, (coords,tile) in enumerate(
      browse_tiles(segment, size=size, blank_tol=blank_tol)):
        imsave(os.path.join(dstdir, 
                  f"{os.path.basename(src)[:-len(segment_ext)]}"
                  f"_{i}_x{coords[0]}_y{coords[1]}.{ext}"), tile, 
                  check_contrast=False)