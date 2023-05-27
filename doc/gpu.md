# gpu

## cupy_to_numpy

```
Return a numpy.array from a cupy.array or a numpy.array.
    \nPARAMETERS
      arr (numpy.array or cupy.array): array to convert as numpy one (if not already)
    \nRETURNS
      convarr (numpy.array): converted array
```

## gpu_computation

```
Enable or disable gpu computation. To enable it, cupy and cucim modules are needed.
    It changes import as axskimg and axp.
    \nPARAMETERS
      activate=False (bool): activate or not gpu computation
```

## select_device

```
Select device used for some gpu computations of the current process.
    \nPARAMETERS
      device (int or None): selected gpu (if None, does nothing)
```

