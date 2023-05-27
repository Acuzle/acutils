import cv2
import os



# A function prefixed with "tmnt" is a treatment function and must have those parameters:
#  - src: absolute path to the file that will be processed (str)
#  - dstdir: absolute path to the directory that should contain new files (str)
# Also, it shouldn't return anything.



def tmnt_resize_file(src, dstdir, new_width=224, new_height=224):
    '''
    Load image file from src, resize, then save it into dstdir.
    \nPARAMETERS
      src (str): absolute path to the file that will be processed
      dstdir (str): absolute path to the directory that should contain new files
      new_width=224 (int): expected width resize
      new_height=224 (int): expected height resize
    '''
    img = cv2.imread(src)
    cv2.imwrite(os.path.join(dstdir, os.path.basename(src)), 
          cv2.resize(img, (new_height, new_width)))