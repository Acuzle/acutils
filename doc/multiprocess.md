# multiprocess

# _process_func_on_multiple_files


Call "func" function for each "src"/"dstdir" from "srcs"/"dstdirs".
"func" needs "src" and "dstdir" params (in acutils, those are prefixed
with "tmnt").
**kwargs should be addionnal arguments to pass to the "func" function.

PARAMETERS
----------
(array/list like of str) srcs:
Source file of each process.

(array/list like of str) dstdirs:
Destination directory of each process.

(function) func:
Treatment that will be applied on each source file it needs an absolute
path to the source file "src" and absolute absolute path to destination files
directory "dstdir" in acutils, any function prefixed with "tmnt" is usable.

**kwargs: Arguments to pass to the "func" function.

RETURNS
-------
None


# run_processes_on_multiple_files


Run processes on the maximum amount of allowed CPUs to apply "func" function
to each source file.
"func" needs "src" and "dstdir" params (in acutils, those are prefixed with
"tmnt").
**kwargs should be addionnal arguments to pass to the "func" function.

PARAMETERS
----------
(list<list<str>>) packed_srcs:
Source files absolute paths per process.

(list<list<str>>) packed_dstdirs:
Destination directories absolute paths per process.

(function) func:
Treatment that will be applied on each source file it needs an absolute
path to the source file "src" and absolute absolute path to destination
files directory "dstdir" in acutils, any function prefixed with "tmnt"
is usable.

(int) allowed_cpus=1:
Maximum amount of CPUs used to compute.

**kwargs: Arguments to pass to the "func" function.

RETURNS
-------
None


# distribute


Distribute files to process and split them between allowed CPUs.
The distribution is returned as 2 lists of lists of src or dstdir.

PARAMETERS
----------
(array/list like of str) srcs:
Source files.

(array/list like of str) dstdirs:
Destination directories.

(int) allowed_cpus=1:
Maximum amount of CPUs used to compute.

(int) seed=871:
Seed used to initialize numpy randomizer.

RETURNS
-------
(list<list<str>>) packed_srcs:
Source files absolute paths per process.

(list<list<str>>) packed_dstdirs:
Destination directories absolute paths per process.


