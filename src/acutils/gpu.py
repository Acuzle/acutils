import os



def cupy_to_numpy(arr):
    '''
    Return a numpy.array from a cupy.array or a numpy.array.

    PARAMETERS
    ----------    
	(numpy.array or cupy.array) arr:
		array to convert as numpy one 
    (if not already).

    RETURNS
    -------    
	(numpy.array) convarr:
		converted array.
    '''
    try:
        return arr.get() # if using GPU (cupy)
    except AttributeError:
        return arr



def set_gpu_computation(activate=True):
    '''
    Enable or disable GPU computation. To enable it, cupy and cucim modules
    are needed, it changes import as auski and aunp.

    PARAMETERS
    ----------    
	(bool) activate=False:
		activate or not GPU computation.

    RETURNS
    -------
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
    Select device used for some GPU computations of the current process.

    PARAMETERS
    ----------    
	(int or None) device:
		selected GPU (if None, does nothing).

    RETURNS
    -------
	None
    '''
    if device is not None:
        try:
            aunp.cuda.Device(device).use()
        except AttributeError:
            print(f"|WRN| Using CPU, can not select the device '{device}'")