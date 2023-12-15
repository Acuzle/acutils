# A function prefixed with "tmnt" is a treatment function and must have those parameters:
#  - src: absolute path to the file that will be processed (str)
#  - dstdir: absolute path to the directory that should contain new files (str)
# Also, it shouldn't return anything.



import os



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



def set_gpu_computation(activate=True):
    '''
    Enable or disable gpu computation. To enable it, cupy and cucim modules
    are needed, it changes import as auski and aunp.

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
    global auski, aunp # strange names to avoid conflicts
    if activate == True:
        try:
            cuda_visible_devices = os.environ.get("CUDA_VISIBLE_DEVICES", "")
            if not cuda_visible_devices:
                raise LookupError("CUDA_VISIBLE_DEVICES is not set."
                            "Valid example: export CUDA_VISIBLE_DEVICES=1,3,0")

            visible_devices_list = cuda_visible_devices.split(',')
            if (len(visible_devices_list) <= 0):
                raise LookupError("CUDA_VISIBLE_DEVICES value is not valid. "
                            "Valid example: export CUDA_VISIBLE_DEVICES=1,3,0")
            import cucim.skimage as auski
            import cupy as aunp
            aunp.cuda.Device(visible_devices_list[0]).use()
            print(f"Device '{visible_devices_list[0]}' selected for "
                  "GPU computation.")

        except Exception as err:
            print(err)
            print("|WRN| Using CPU, cucim or cupy not available.")
            import skimage as auski
            import numpy as aunp
    else:
        import skimage as auski
        import numpy as aunp



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
            aunp.cuda.Device(device).use()
        except AttributeError:
            print("|WRN| Using CPU, for gpu computation call set_gpu_computation(activate=True).")