# Functions prefixed with "tmnt" are treatments and must have those parameters:
#  - src: absolute path to the file that will be processed (str)
#  - dstdir: absolute path to the directory that should contain new files (str)
# Also, nothing should be returned.

import os

try:
    import cv2
except ImportError:
    print("|WRN| You must install 'opencv-python' (cv2) to use image module. "
          "Leaving.")
    exit()



def tmnt_resize_file(src, dstdir, new_width=224, new_height=224):
    '''
    Load image file from src, resize, then save it into dstdir.
    
    PARAMETERS
    ----------    
	(str) src:
		Absolute path to the file that will be processed.
    
	(str) dstdir:
		Absolute path to the directory that should contain new files.
    
	(int) new_width=224:
		Expected width resize.
    
	(int) new_height=224:
		Expected height resize.
    
    RETURNS
    -------
	None    
    '''
    img = cv2.imread(src)
    cv2.imwrite(os.path.join(dstdir, os.path.basename(src)), 
          cv2.resize(img, (new_height, new_width)))