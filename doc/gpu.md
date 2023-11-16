# gpu

# cupy_to_numpy


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


# set_gpu_computation


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


# select_device


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


