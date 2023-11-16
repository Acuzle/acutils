# A function prefixed with "tmnt" is a treatment function and must have those parameters:
#  - src: absolute path to the file that will be processed (str)
#  - dstdir: absolute path to the directory that should contain new files (str)
# Also, it shouldn't return anything.



def cupy_to_numpy(arr):
    '''
    Return a numpy.array from a cupy.array or a numpy.array.

    PARAMETERS
    ----------
    - arr (numpy.array or cupy.array): array to convert as numpy one (if not already).

    RETURNS
    -------
    convarr (numpy.array): converted array.

    RAISES
    ------
    None
    '''
    try:
        return arr.get() # if using gpu (cupy)
    except AttributeError:
        return arr



def gpu_computation(activate=True):
    '''
    Enable or disable gpu computation. To enable it, cupy and cucim modules are needed.
    It changes import as axskimg and axp.

    PARAMETERS
    ----------
    - activate=False (bool): activate or not gpu computation.

    RETURNS
    -------
    None

    RAISES
    ------
    None
    '''
    global axskimg, axp # strange names to avoid conflicts
    if activate == True:
        try:
            import cucim.skimage as axskimg
            import cupy as axp
        except ImportError:
            import skimage as axskimg
            import numpy as axp
            print("|WRN| Using CPU, cucim or cupy not available.")
    else:
        import skimage as axskimg
        import numpy as axp



def select_device(device):
    '''
    Select device used for some gpu computations of the current process.

    PARAMETERS
    ----------
    - device (int or None): selected gpu (if None, does nothing).

    RETURNS
    -------
    None

    RAISES
    ------
    None
    '''
    if device is not None:
        try:
            axp.cuda.Device(device).use()
        except AttributeError:
            print("|WRN| Using CPU, for gpu computation call gpu_computation(activate=True).")