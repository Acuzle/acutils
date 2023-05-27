# multiprocess

## _process_func_on_multiple_files

```
Call "func" function for each "src"/"dstdir" from "srcs"/"dstdirs".
    "func" needs "src" and "dstdir" params (in acutils, those are prefixed with "tmnt").
    **kwargs should be addionnal arguments to pass to the "func" function.
    \nPARAMETERS
      srcs (array/list like of str): source file of each process
      dstdirs (array/list like of str): destination directory of each process
      func (function): treatment that will be applied on each source file 
                       it needs an absolute path to the source file "src" 
                       and absolute absolute path to destination files directory "dstdir"
                       in acutils, any function prefixed with "tmnt" is usable
      **kwargs: arguments to pass to the "func" function.
```

## run_processes_on_multiple_files

```
Run processes on the maximum amount of allowed cpus to apply "func" function to each
    source file.
    "func" needs "src" and "dstdir" params (in acutils, those are prefixed with "tmnt").
    **kwargs should be addionnal arguments to pass to the "func" function.
    \nPARAMETERS
      packed_srcs (list<list<str>>): source files absolute paths per process
      packed_dstdirs (list<list<str>>): destination directories absolute paths per process
      func (function): treatment that will be applied on each source file
                       it needs an absolute path to the source file "src" 
                       and absolute absolute path to destination files directory "dstdir"
                       in acutils, any function prefixed with "tmnt" is usable
      allowed_cpus=1 (int): maximum amount of cpus used to compute
      **kwargs: arguments to pass to the "func" function.
```

## distribute

```
Distribute files to process and split them between allowed cpus.
    The distribution is returned as 2 lists of lists of src or dstdir.
    \nPARAMETERS
      srcs (array/list like of str): source files
      dstdirs (array/list like of str): destination directories
      allowed_cpus=1 (int): maximum amount of cpus used to compute
      seed=871 (int): seed used to initialize numpy randomizer
    \nRETURNS
      packed_srcs (list<list<str>>): source files absolute paths per process
      packed_dstdirs (list<list<str>>): destination directories absolute paths per process
```

