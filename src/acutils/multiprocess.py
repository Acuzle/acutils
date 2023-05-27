import numpy as np
from joblib import Parallel, delayed



def _process_func_on_multiple_files(srcs, dstdirs, func, **kwargs):
    '''
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
    '''
    for src, dstdir in zip(srcs, dstdirs):
        func(src, dstdir, **kwargs)



def run_processes_on_multiple_files(packed_srcs, packed_dstdirs, func, allowed_cpus=1, **kwargs):
    '''
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
    '''
    Parallel(n_jobs=allowed_cpus)(delayed(_process_func_on_multiple_files)(
                srcs = srcs,
                dstdirs = dstdirs,
                func = func,
                **kwargs)
    for srcs, dstdirs in zip(packed_srcs, packed_dstdirs))



def distribute(srcs, dstdirs, allowed_cpus=1, seed=871):
    '''
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
    '''
    # Use numpy arrays to select with indices
    if type(srcs) is not np.array:
        srcs = np.array(srcs)
    if type(dstdirs) is not np.array:
        dstdirs = np.array(dstdirs)

    # Split srcs and dstdirs between allowed cpus (to return this as lists)
    packed_srcs = []
    packed_dstdirs = []
    for ids in np.array_split(np.arange(srcs.size), int(allowed_cpus)):
        np.random.seed(seed)
        np.random.shuffle(ids)
        if ids.size > 0:
          packed_srcs.append(srcs[ids])
          packed_dstdirs.append(dstdirs[ids])
      
    return packed_srcs, packed_dstdirs