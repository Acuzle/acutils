# handler

# __init__


Initiate DataHandler instance to handle data on disk.

PARAMETERS
----------
- datapath (str): Absolute path to the directory that contain source
files.
- file_extensions=None (array/list like of str): Source file allowed
extensions.
- allowed_cpus=1 (int): Maximum amount of CPUs used to compute.
- seed=871 (int): Seed used to initialize numpy randomizer.
- seed=str_ndarray_dtype="U256" (str): Data type used for any string
numpy arrays. It defines the maximum length of strings, especially
those in sheet files, for loading labels and groups.

RETURNS
-------
None

RAISES
------
- NotADirectoryError: if the absolute path doesn't lead to an existing
directory.


# _format_sheet


Format a dataframe by deleting rows with empty cell, also add extension
to filenames if filename doesn't contain it already, and if there is
only one extension.

PARAMETERS
----------
- df (pandas.DataFrame): dataframe to format
- filecol=None (str): Name of the column that contains filenames, not
used there.
- labelcol=None (str): Name of the column that contains labels, not
used there.
- othercols=None (list<str>): Name of the other columns, not used there.
- clueless_words=None (array/list like of str): Strings considered as
None.

RETURNS
-------
- df (pandas.DataFrame): formated dataframe.

RAISES
------
None


# _load_sheet


Load a sheet file and keep indicated columns.

PARAMETERS
----------
- sheetpath (str): Absolute path to the sheet which contain information
about data.
- filecol=None (str): Name of the column that contains filenames.
- labelcol=None (str): Name of the column that contains labels, not used
here.
- othercols=None (iterable of str): Name of the other columns to keep.

RETURNS
-------
- df (pandas.DataFrame): Loaded dataframe.

RAISES
------
- ValueError: If the file extension is not supported.


# load_data_fromdatapath


Load data files from data directory.
Assuming that those files are directly inside the data directory.
The filenames are stored as "files" attribute.

PARAMETERS
----------
None

RETURNS
-------
None

RAISES
------
None


# load_labels_fromsheet


Load data labels from a sheet file.
You must load files before calling this, you might call
"load_data_fromdatapath". The labels are stored as "labels" attribute
and their unique values are stored as "unique_labels" attribute.

PARAMETERS
----------
- sheetpath (str): Absolute path to the sheet which contain information
about data.
- idcol=None (str): Name of the column that contains at least a part of
the filename.
- labelcol=None (str): Name of the column that contains labels, not used
here.
- othercols=None (array/list like of str): Name of the other columns to
keep.
- clueless_words=None (array/list like
of str): Strings considered as
None.
- delete_unlabeled_files=True (bool): If True, delete each file without
label.
- require_full_filename_match=False (bool): If True, requires the value
in the idcol to be exactly the filename, otherwise, if the value in the
idcol is included in the filename, it is considered as a match. Note
that if the idcol value is included in multiple filenames, it will be
associated with the first one found (in descending length order).

RETURNS
-------
None

RAISES
------
None


# load_labeled_data_fromdatapath


Load data files and labels from data directory.
Assuming that those files are inside subdirectories (named with unique
labels). The filenames are stored as "files" attribute. The labels are
stored as "labels" attribute and their unique values are stored as
"unique_labels" attribute.

PARAMETERS
----------
None

RETURNS
-------
None

RAISES
------
None


# load_groups_fromsheet


Load data groups from a sheet file.
You must load files before calling this, you might call
"load_data_fromdatapath". The groups are stored as "groups" attribute.

PARAMETERS
----------
- sheetpath (str): Absolute path to the sheet which contain information
about data.
- idcol=None (str): Name of the column that contains at least a part of
the filename.
- groupcol=None (str): Name of the column that contains groups, not used
here.
- clueless_words=None (array/list like of str): Strings considered as
None.
- require_full_filename_match=False (bool): If True, requires the value
in the idcol to be exactly the filename, otherwise, if the value in the
idcol is included in the filename, it is considered as a match. Note
that if the idcol value is included in multiple filenames, it will be
associated with the first one found (in descending length order).

RETURNS
-------
None

RAISES
------
None


# _balance_dataset


Balance dataset so the amount of data is equal for each label.

PARAMETERS
----------
- data (dict<str,str>): Dictionary with filename as key and label as
value.

RETURNS
-------
- balanced_data (dict<str,str>): Data without superfluous files to
balance it.

RAISES
------
None


# balance_datasets


Balance datasets so the amount of data is equal for each label.
This is basically calling "_balance_dataset" method with tdata then vdata.

PARAMETERS
----------
- tdata (dict<str,str>): Train dictionary with filename as key and label
as value.
- vdata (dict<str,str>): Val dictionary with filename as key and label
as value.

RETURNS
-------
- balanced_tdata (dict<str,str>): Train data without superfluous files
to balance it.
- balanced_vdata (dict<str,str>): Val data without superfluous files to
balance it.

RAISES
------
None


# _split_using_groups


Split labeled data into train and test datasets considering data groups.

PARAMETERS
----------
- train_percentage=0.7 (float): Percentage of data expected in train
dataset.
- balance=False (bool): Do call "balance_datasets" method before
returning dictionaries.

RETURNS
-------
- tdata (dict<str,str>): Train dictionary with filename as key and label
as value.
- vdata (dict<str,str>): Val dictionary with filename as key and label as
value.

RAISES
------
None


# split


Split labeled data into train and test datasets.

PARAMETERS
----------
- train_percentage=0.7 (float): Percentage of data expected in train
dataset.
- balance=False (bool): Do call "balance_datasets" method before
returning dictionaries.
- ignore_groups=False (bool): If True, ignore groups for the split,
even though it is defined. If the "groups" attribute is not define,
then it is ignored anyway. If it is defined and "ignore_groups" is
False, then the split is done calling "_split_using_groups" method.

RETURNS
-------
- tdata (dict<str,str>): train dictionary with filename as key and label
as value.
- vdata (dict<str,str>): val dictionary with filename as key and label
as value.

RAISES
------
None


# _distribute_data


Distribute files to process and split them between allowed cpus.
The distribution is returned as 2 lists of lists of src or dstdir.

PARAMETERS
----------
- dirpath (str): Absolute path to the directory for treated files.

RETURNS
-------
- packed_srcs (list<list<str>>): Source files absolute paths per
process.
- packed_dstdirs (list<list<str>>): Destination directories absolute
paths per process.

RAISES
------
None


# _distribute_datasets


Distribute files to process and split them between allowed cpus.
The distribution is returned into collections.

PARAMETERS
----------
- tdstdir (str): Absolute path to the destination files directory for
train dataset.
- vdstdir (str): Absolute path to the destination files directory for
val dataset.
- tdata (dict<str,str>): Train dictionary with filename as key and label
as value.
- vdata (dict<str,str>): Val dictionary with filename as key and label
as value.

RETURNS
-------
- packed_srcs (list<list<str>>): Src files absolute paths per process.
- packed_dstdirs (list<list<str>>): Destination directories absolute
paths per process.

RAISES
------
None


# _run_processes


Run processes on the maximum amount of allowed CPUs to apply "func"
function to each source file.
"func" needs "src" and "dstdir" params (in acutils, those are
prefixed with "tmnt").
**kwargs should be addionnal arguments to pass to the "func" function.

PARAMETERS
----------
- packed_srcs (array/list like of iterables of str): src files absolute
paths per process.
- packed_dstdirs (array/list like of iterables of str): dst dirs
absolute paths per process.
- func (function): Treatment that will be applied on each source file
it needs an absolute path to the source file "src" and absolute
absolute path to destination files directory "dstdir" in acutils,
any function prefixed with "tmnt" is usable.
- **kwargs: Arguments to pass to the "func" function.

RETURNS
-------
None

RAISES
------
None


# _reset_directory


Delete directory if it exists, then create it again and fill it with
empty subdirecories, named from unique labels (if defined and not empty).

PARAMETERS
----------
- dirpath (str): Absolute path to the directory to reset.

RETURNS
-------
None

RAISES
------
None


# process


Run processes on the maximum amount of allowed CPUs to apply "func"
function to each source file. If "func" is None, just copy the file.
"func" needs "src" and "dstdir" params (in acutils, those are
prefixed with "tmnt").
**kwargs should be addionnal arguments to pass to the "func" function.

PARAMETERS
----------
- dirpath (str): Absolute path to treated files directory.
- func=None (function): Treatment that will be applied on each source
file it needs an absolute path to the source file "src" and absolute
absolute path to destination files directory "dstdir" in acutils,any
function prefixed with "tmnt" is usable.
- empty_dir=True (bool): If True, reset destination directory and fill it with unique labels
as subdirectories if defined
- **kwargs: Arguments to pass to the "func" function.

RETURNS
-------
None

RAISES
------
None


# make_datasets


Run processes on the maximum amount of allowed CPUs to apply "func"
function to each source file.
"func" needs "src" and "dstdir" params (in acutils, those are prefixed with "tmnt").
**kwargs should be addionnal arguments to pass to the "func" function.

PARAMETERS
----------
- trainpath (str): Absolute path to the destination files train directory.
- valpath (str): Absolute path to the destination files val directory.
- tdata (dict<str,str>): Train dictionary with filename as key and label
as value.
- vdata (dict<str,str>): Val dictionary with filename as key and label
as value.
- func=None (function): Treatment that will be applied on each source
file it needs an absolute path to the source file "src" and absolute
absolute path to destination files directory "dstdir" in acutils,any
function prefixed with "tmnt" is usable.
- empty_dir=True (bool): If True, reset destination directories and fill
it with unique labels as subdirectories if defined.
- **kwargs: Arguments to pass to the "func" function.

RETURNS
-------
None

RAISES
------
None


# save_split


Save a split (from "split" method) as a json file.

PARAMETERS
----------
- dst (str): absolute path to the new json file.
- data (dict<str,str>): data dictionary to save.

RETURNS
-------
None

RAISES
------
None


# load_split


Load a dictionary from a json file.

PARAMETERS
----------
- src (str): absolute path to the json file.

RETURNS
-------
- data (dict<str,str>): loaded data dictionary.

RAISES
------
None


