# A function prefixed with "tmnt" is a treatment function and must have those parameters:
#  - src: absolute path to the file that will be processed (str)
#  - dstdir: absolute path to the directory that should contain new files (str)
# Also, it shouldn't return anything.



def cupy_to_numpy(arr):
    '''
    Return a numpy.array from a cupy.array or a numpy.array.
    \nPARAMETERS
      arr (numpy.array or cupy.array): array to convert as numpy one (if not already)
    \nRETURNS
      convarr (numpy.array): converted array
    '''
    try:
        return arr.get() # if using gpu (cupy)
    except AttributeError:
        return arr



def gpu_computation(activate=False):
    '''
    Enable or disable gpu computation. To enable it, cupy and cucim modules are needed.
    It changes import as axskimg and axp.
    \nPARAMETERS
      activate=False (bool): activate or not gpu computation
    '''
    global axskimg, axp # strange names to avoid conflicts
    if activate == True:
        try:
            import cucim.skimage as axskimg
            import cupy as axp
        except ImportError:
            import skimage as axskimg
            import numpy as axp
            print("|WRN| using cpu, cucim or cupy not available")
    else:
        import skimage as axskimg
        import numpy as axp



def select_device(device):
    '''
    Select device used for some gpu computations of the current process.
    \nPARAMETERS
      device (int or None): selected gpu (if None, does nothing)
    '''
    if device is not None:
        try:
            axp.cuda.Device(device).use()
        except AttributeError:
            print("|WRN| using cpu, for gpu computation call _gpu_computation(activate=True)")