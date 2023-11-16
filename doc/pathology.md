# pathology

# update_ref_image


Change reference image using when calling harmonize function.

PARAMETERS
----------
img_path=None (str): Absolute path to the image that will be the reference to harmonize.

RETURNS
-------
df (pandas.DataFrame): Formated dataframe.

RAISES
------
None


# harmonize


Harmonize the image through hed conversion, erase the color and keep the stains.
Then match the histogram with a reference image.
You can change the reference image calling update_ref_image function.

PARAMETERS
----------
- img (numpy.array or cupy.array of int): RGB image to harmonize.

RETURNS
-------
None

RAISES
------
None

REFERENCES
----------
- [1] A. C. Ruifrok and D. A. Johnston, "Quantification of histochemical
staining by color deconvolution.," Analytical and quantitative
cytology and histology / the International Academy of Cytology [and]
American Society of Cytology, vol. 23, no. 4, pp. 291-9, Aug. 2001.


# tmnt_harmonize


Read a segment, harmonize it calling harmonize function, then save it.

PARAMETERS
----------
- src (str): Absolute path to the file that will be processed.
- dstdir (str): Absolute path to the directory that should contain the new file.

RETURNS
-------
None

RAISES
------
None


# get_preview


Read the slide and returns it with low resolution.

PARAMETERS
----------
- slide (openslide.OpenSlide): The slide.
- lvl=-1 (int): Level taken.
- divider=None (float): Scale the preview by dividing the slide.

RETURNS
-------
- preview (numpy.array or cupy.array of int): Scaled loaded slide.

RAISES
------
None


# get_cleaned_binary


Split foreground (1) and background (0) using mathematic morphology.

PARAMETERS
----------
- preview (numpy.array of cupy.array of int): Fully loaded slide with low resolution.
- fpval=16 (int): Value that is used to creates footprints for segmentation.
- sigma=2 (float): Value for gaussian filter (applied on the slide before segmentation).

RETURNS
-------
- bw (numpy.array of cupy.array of bool): Binary image from the preview.

RAISES
------
None


# mask_rgb


Mask rgb image with a binary image.

PARAMETERS
----------
- rgb (numpy.array or cupy.array of int): RGB image.
- mask (numpy.array or cupy.array of bool): Binary image.

RETURNS
-------
- masked_rgb (numpy.array or cupy.array of uint8): RGB image masked with the binary image.

RAISES
------
None


# browse_segments


Find slices inside the preview and load it from de slide.

PARAMETERS
----------
- slide (openslide.OpenSlide): The slide.
- bw (numpy.array of cupy.array of bool): Binary image from the preview.
- lvl=0 (int): level taken.
- required_area=10000 (int): Minimum area (pixels) to keep the slice.
- do_harmonize=False (bool): Harmonize slices using harmonize function.

RETURNS
-------
- Segments (generator of numpy.array of uint8): Found slices.

RAISES
------
None


# load_slice_preview_and_ext


Load slide file and extract a preview of it using get_preview function.

PARAMETERS
----------
- src (str): Absolute path to the slide.
- lvl (int): Slide level taken.
- divider=None (float): Scale the preview by dividing the slide.
- device=None (int): Taken gpu.

RETURNS
-------
- slide (openslide.OpenSlide): The slide.
- preview (numpy.array of cupy.array of int): Fully loaded slide with low resolution.
- slide_ext (str): Slide extension.

RAISES
------
None


# tmnt_save_preview_from_slide


Load slide preview and save it.

PARAMETERS
----------
- src (str): Absolute path to the slide.
- dstdir (str): Absolute path to the directory where to save the preview.
- lvl (int): Slide level taken.
- divider=None (float): Scale the preview by dividing the slide.
- ext="png" (str): Saved preview extension.
- device=None (int): Taken gpu.

RETURNS
-------
None

RAISES
------
None


# tmnt_save_segments_from_slide


Find slices inside the slide and save them.

PARAMETERS
----------
- src (str): Absolute path to the slide.
- dstdir (str): Absolute path to the directory where to save the preview.
- lvlpreview (int): Slide level taken for the preview.
- lvlsegment (int): Slide level taken for the segment.
- fpval (int): Value that is used to creates footprints for segmentation.
- sigma (float): Value for gaussian filter (applied on the slide before segmentation).
- do_harmonize=False (bool): Harmonize slices using harmonize function.
- divider=None (float): Scale the preview by dividing the slide.
- ext="png" (str): Saved segments extension.
- device=None (int): Taken gpu.

RETURNS
-------
None

RAISES
------
None


# browse_tiles


Regulary crop a segment into multiple tiles of same size.

PARAMETERS
----------
- segment (numpy.array of int): Slice to tile.
- size=512 (int): Size of each tile.
- blank_tol=0.35 (float): Percentage of white pixels tolerated for a tile.

RETURNS
-------
- coordinates (generator of tuple of int): Tiles coordinates (x,y).
- tiles generator of numpy.array of int): Keeped tiles.

RAISES
------
None


# tmnt_save_tiles_from_segment


Find slices inside the slide and save them.

PARAMETERS
----------
- src (str): Absolute path to the slide.
- dstdir (str): Absolute path to the directory where to save the preview.
- size=512 (int): Size of each tile.
- blank_tol=0.35 (float): Percentage of white pixels tolerated for a tile.
- ext="png" (str): Saved tiles extension.

RETURNS
-------
None

RAISES
------
None


