# multiprocess

# _process_func_on_multiple_files


Call "func" function for each "src"/"dstdir" from "srcs"/"dstdirs".
"func" needs "src" and "dstdir" params (in acutils, those are prefixed
with "tmnt").
**kwargs should be addionnal arguments to pass to the "func" function.

PARAMETERS
----------
- srcs (array/list like of str): Source file of each process.
- dstdirs (array/list like of str): Destination directory of each process.
- func (function): Treatment that will be applied on each source file it
needs an absolute path to the source file "src" and absolute absolute path
to destination files directory "dstdir" in acutils, any function prefixed
with "tmnt" is usable.
- **kwargs: Arguments to pass to the "func" function.

RETURNS
-------
None

RAISES
------
None


# run_processes_on_multiple_files


Run processes on the maximum amount of allowed CPUs to apply "func" function
to each source file.
"func" needs "src" and "dstdir" params (in acutils, those are prefixed with
"tmnt").
**kwargs should be addionnal arguments to pass to the "func" function.

PARAMETERS
----------
- packed_srcs (list<list<str>>): Source files absolute paths per process.
- packed_dstdirs (list<list<str>>): Destination directories absolute paths
per process.
- func (function): Treatment that will be applied on each source file it
needs an absolute path to the source file "src" and absolute absolute path
to destination files directory "dstdir" in acutils, any function prefixed
with "tmnt" is usable.
- allowed_cpus=1 (int): Maximum amount of CPUs used to compute.
- **kwargs: Arguments to pass to the "func" function.

RETURNS
-------
None

RAISES
------
None


# distribute


Distribute files to process and split them between allowed CPUs.
The distribution is returned as 2 lists of lists of src or dstdir.

PARAMETERS
----------
- srcs (array/list like of str): Source files.
- dstdirs (array/list like of str): Destination directories.
- allowed_cpus=1 (int): Maximum amount of CPUs used to compute.
- seed=871 (int): Seed used to initialize numpy randomizer.

RETURNS
-------
- packed_srcs (list<list<str>>): Source files absolute paths per process.
- packed_dstdirs (list<list<str>>): Destination directories absolute paths
per process.

RAISES
------
None


