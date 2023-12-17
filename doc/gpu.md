# gpu

# cupy_to_numpy


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


# set_gpu_computation


Enable or disable GPU computation. To enable it, cupy and cucim modules
are needed, it changes import as auski and aunp.

PARAMETERS
----------
(bool) activate=False:
activate or not GPU computation.

RETURNS
-------
None


# select_device


Select device used for some GPU computations of the current process.

PARAMETERS
----------
(int or None) device:
selected GPU (if None, does nothing).

RETURNS
-------
None


