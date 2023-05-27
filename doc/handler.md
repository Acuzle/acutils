# handler

## __init__

```
Initiate DataHandler instance to handle data on disk.
        \nPARAMETERS
          datapath (str): absolute path to the directory that contain source files
          file_extensions=None (array/list like of str): source file allowed extensions
          allowed_cpus=1 (int): maximum amount of cpus used to compute
          seed=871 (int): seed used to initialize numpy randomizer
        \nRAISES
          NotADirectoryError: if the absolute path doesn't lead to an existing directory
```

## _format_sheet

```
Format a dataframe by deleting rows with empty cell, also add extension to filenames
        if filename doesn't contain it already, and if there is only one extension.
        \nPARAMETERS
          df (pandas.DataFrame): dataframe to format
          filecol=None (str): name of the column that contains filenames, not used there
          labelcol=None (str): name of the column that contains labels, not used there
          othercols=None (list<str>): name of the other columns, not used there
          clueless_words=None (array/list like of str): strings considered as None
        \nRETURNS
          df (pandas.DataFrame): formated dataframe
```

## _load_sheet

```
Load a sheet file and keep indicated columns.
        \nPARAMETERS
          sheetpath (str): absolute path to the sheet which contain information about data
          filecol=None (str): name of the column that contains filenames
          labelcol=None (str): name of the column that contains labels, not used here
          othercols=None (iterable of str): name of the other columns to keep
        \nRETURNS
          df: (pandas.DataFrame) loaded dataframe
        \nRAISES
          ValueError: If the file extension is not supported.
```

## load_data_fromdatapath

```
Load data files from data directory.
        Assuming that those files are directly inside the data directory.
```

## load_labels_fromsheet

```
Load data labels from a sheet file. 
        You must load files before calling this, you might call "load_data_fromdatapath".
        \nPARAMETERS
          sheetpath (str): absolute path to the sheet which contain information about data
          idcol=None (str): name of the column that contains at least a part of the filename
          labelcol=None (str): name of the column that contains labels, not used here
          othercols=None (array/list like of str): name of the other columns to keep
          clueless_words=None (array/list like of str): strings considered as None
          delete_unlabeled_files=True (bool): if True, delete each file without label
```

## load_labeled_data_fromdatapath

```
Load data files and labels from data directory.
        Assuming that those files are inside subdirectories (named with unique labels).
```

## load_groups_fromsheet

```
Load data groups from a sheet file. 
        You must load files before calling this, you might call "load_data_fromdatapath".
        \nPARAMETERS
          sheetpath (str): absolute path to the sheet which contain information about data
          idcol=None (str): name of the column that contains at least a part of the filename
          groupcol=None (str): name of the column that contains groups, not used here
          clueless_words=None (array/list like of str): strings considered as None
```

## _balance_dataset

```
Balance dataset so the amount of data is equal for each label.
        \nPARAMETERS
          data (dict<str,str>): dictionary with filename as key and label as value
        \nRETURNS
          balanced_data (dict<str,str>): data without superfluous files to balance it
```

## balance_datasets

```
Balance datasets so the amount of data is equal for each label.
        This is basically calling "_balance_dataset" method with tdata then vdata.
        \nPARAMETERS
          tdata (dict<str,str>): train dictionary with filename as key and label as value
          vdata (dict<str,str>): val dictionary with filename as key and label as value
        \nRETURNS
          balanced_tdata (dict<str,str>): train data without superfluous files to balance it
          balanced_vdata (dict<str,str>): val data without superfluous files to balance it
```

## split

```
Split labeled data into train and test datasets.
        \nPARAMETERS
          train_percentage=0.7 (float): percentage of data expected in train dataset
          balance=False (bool): do call "balance_datasets" method before returning dictionaries
        \nRETURNS
          tdata (dict<str,str>): train dictionary with filename as key and label as value
          vdata (dict<str,str>): val dictionary with filename as key and label as value
```

## split_using_groups

```
Split labeled data into train and test datasets considering data groups.
        \nPARAMETERS
          train_percentage=0.7 (float): percentage of data expected in train dataset
          balance=False (bool): do call "balance_datasets" method before returning dictionaries
        \nRETURNS
          tdata (dict<str,str>): train dictionary with filename as key and label as value
          vdata (dict<str,str>): val dictionary with filename as key and label as value
```

## _distribute_data

```
Distribute files to process and split them between allowed cpus.
        The distribution is returned as 2 lists of lists of src or dstdir.
        \nPARAMETERS
          dirpath (str): absolute path to the directory for treated files
        \nRETURNS
          packed_srcs (list<list<str>>): source files absolute paths per process
          packed_dstdirs (list<list<str>>): destination directories absolute paths per process
```

## _distribute_datasets

```
Distribute files to process and split them between allowed cpus.
        The distribution is returned into collections.
        \nPARAMETERS
          tdstdir (str): absolute path to the destination files directory for train dataset
          vdstdir (str): absolute path to the destination files directory for val dataset
          tdata (dict<str,str>): train dictionary with filename as key and label as value
          vdata (dict<str,str>): val dictionary with filename as key and label as value
        \nRETURNS
          packed_srcs (list<list<str>>): src files absolute paths per process
          packed_dstdirs (list<list<str>>): destination directories absolute paths per process
```

## _run_processes

```
Run processes on the maximum amount of allowed cpus to apply "func" function to each
        source file.
        "func" needs "src" and "dstdir" params (in acutils, those are prefixed with "tmnt").
        **kwargs should be addionnal arguments to pass to the "func" function.
        \nPARAMETERS
          packed_srcs (array/list like of iterables of str): src files absolute paths per process
          packed_dstdirs (array/list like of iterables of str): dst dirs absolute paths per process
          func (function): treatment that will be applied on each source file
                           it needs an absolute path to the source file "src" 
                           and absolute absolute path to destination files directory "dstdir"
                           in acutils, any function prefixed with "tmnt" is usable
                           **kwargs: arguments to pass to the "func" function
```

## _reset_directory

```
Delete directory if it exists, then create it again and fill it with
        empty subdirecories, named from unique labels (if defined and not empty).
        \nPARAMETERS
          dirpath (str): absolute path to the directory to reset
```

## process

```
Run processes on the maximum amount of allowed cpus to apply "func" function to each
        source file.
        "func" needs "src" and "dstdir" params (in acutils, those are prefixed with "tmnt").
        **kwargs should be addionnal arguments to pass to the "func" function.
        \nPARAMETERS
          dirpath (str): absolute path to treated files directory
          func=None (function): treatment that will be applied on each source file
                                it needs an absolute path to the source file "src" 
                                and absolute absolute path to destination files directory "dstdir"
                                if None, source files will be copied to the destination directory
                                in acutils, any function prefixed with "tmnt" is usable
          empty_dir=True (bool): if True, reset destination directory and fill it with unique labels
                          as subdirectories if defined
          **kwargs: arguments to pass to the "func" function
```

## make_datasets

```
Run processes on the maximum amount of allowed cpus to apply "func" function to each
        source file.
        "func" needs "src" and "dstdir" params (in acutils, those are prefixed with "tmnt").
        **kwargs should be addionnal arguments to pass to the "func" function.
        \nPARAMETERS
          trainpath (str): absolute path to the destination files train directory
          valpath (str): absolute path to the destination files val directory
          tdata (dict<str,str>): train dictionary with filename as key and label as value
          vdata (dict<str,str>): val dictionary with filename as key and label as value
          func=None (function): treatment that will be applied on each source file
                                it needs an absolute path to the source file "src" 
                                and absolute absolute path to destination files directory "dstdir"
                                if None, source files will be copied to the destination directory
                                in acutils, any function prefixed with "tmnt" is usable
          empty_dir=True (bool): if True, reset destination directories and fill it with unique labels
                                 as subdirectories if defined
          **kwargs: arguments to pass to the "func" function
```

