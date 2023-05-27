# pathology

## update_ref_image

```
Change reference image using when calling harmonize function.
    \nPARAMETERS
      img_path=None (str): absolute path to the image that will be the reference to harmonize
    \nRETURNS
      df (pandas.DataFrame): formated dataframe
```

## harmonize

```
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
```

## tmnt_harmonize

```
Read a segment, harmonize it calling harmonize function, then save it.
    \nPARAMETERS
      src (str): absolute path to the file that will be processed
      dstdir (str): absolute path to the directory that should contain the new file
```

## get_preview

```
Read the slide and returns it with low resolution.
    \nPARAMETERS
      slide (openslide.OpenSlide): the slide
      lvl=-1 (int): level taken
      divider=None (float): scale the preview by dividing the slide
    \nRETURNS
      preview (numpy.array or cupy.array of int): scaled loaded slide
```

## get_cleaned_binary

```
Split foreground (1) and background (0) using mathematic morphology.
    \nPARAMETERS
      preview (numpy.array of cupy.array of int): fully loaded slide with low resolution
      fpval=16 (int): value that is used to creates footprints for segmentation
      sigma=2 (float): value for gaussian filter (applied on the slide before segmentation)
    \nRETURNS
      bw (numpy.array of cupy.array of bool): binary image from the preview
```

## mask_rgb

```
Mask rgb image with a binary image.
    \nParameters
      rgb (numpy.array or cupy.array of int): rgb image
      mask (numpy.array or cupy.array of bool): binary image
    \nReturns
      masked_rgb (numpy.array or cupy.array of uint8): rgb image masked with the binary image
```

## browse_segments

```
Find slices inside the preview and load it from de slide.
    \nPARAMETERS
      slide (openslide.OpenSlide): the slide
      bw (numpy.array of cupy.array of bool): binary image from the preview
      lvl=0 (int): level taken
      required_area=10000 (int): minimum area (pixels) to keep the slice
      do_harmonize=False (bool): harmonize slices using harmonize function
    \nRETURNS
      segments (generator of numpy.array of uint8): found slices
```

## load_slice_preview_and_ext

```
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
```

## tmnt_save_preview_from_slide

```
Load slide preview and save it.
    \nPARAMETERS
      src (str): absolute path to the slide
      dstdir (str): absolute path to the directory where to save the preview
      lvl (int): slide level taken
      divider=None (float): scale the preview by dividing the slide
      ext="png" (str): saved preview extension
      device=None (int): taken gpu
```

## tmnt_save_segments_from_slide

```
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
```

## browse_tiles

```
Regulary crop a segment into multiple tiles of same size.
    \nPARAMETERS
      segment (numpy.array of int): slice to tile
      size=512 (int): size of each tile
      blank_tol=0.35 (float): percentage of white pixels tolerated for a tile
    \nRETURNS
      coordinates (generator of tuple of int): tiles coordinates (x,y)
      tiles generator of numpy.array of int): keeped tiles
```

## tmnt_save_tiles_from_segment

```
Find slices inside the slide and save them.
    \nPARAMETERS
      src (str): absolute path to the slide
      dstdir (str): absolute path to the directory where to save the preview
      size=512 (int): size of each tile
      blank_tol=0.35 (float): percentage of white pixels tolerated for a tile
      ext="png" (str): saved tiles extension
```

