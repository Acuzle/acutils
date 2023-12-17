# pathology

# update_ref_image


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


# harmonize


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


# tmnt_harmonize


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


# get_preview


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


# get_cleaned_binary


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


# mask_rgb


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


# browse_segments


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


# load_slice_preview_and_ext


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


# tmnt_save_preview_from_slide


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


# tmnt_save_segments_from_slide


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


# browse_tiles


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


# tmnt_save_tiles_from_segment


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


