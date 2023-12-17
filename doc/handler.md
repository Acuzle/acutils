# handler

# __init__


Initiate DataHandler instance to handle data on disk.

PARAMETERS
----------
(str) datapath:
Absolute path to the directory that contain source files.

(array/list like of str) file_extensions=None:
Source file allowed extensions.

(int) allowed_cpus=1:
Maximum amount of CPUs used to compute.

(int) seed=871:
Seed used to initialize numpy randomizer.

(str) str_ndarray_dtype="U256":
Data type used for any string numpy arrays. It defines the maximum
length of strings, especially those in sheet files, for loading
labels and groups.

RETURNS
-------
None

RAISES
------
(NotADirectoryError) err:
if the absolute path doesn't lead to an existing directory.


# _format_sheet


Format a dataframe by deleting rows with empty cell, also add extension
to filenames if filename doesn't contain it already, and if there is
only one extension.

PARAMETERS
----------
(pandas.DataFrame) df:
dataframe to format

(str) filecol=None:
Name of the column that contains filenames, not used there.

(str) labelcol=None:
Name of the column that contains labels, not used there.

(list<str>) othercols=None:
Name of the other columns, not used there.

(array/list like of str) clueless_words=None:
Strings considered as None.

RETURNS
-------
(pandas.DataFrame) df:
formated dataframe.

RAISES
------
None


# _load_sheet


Load a sheet file and keep indicated columns.

PARAMETERS
----------
(str) sheetpath:
Absolute path to the sheet which contain information about data.

(str) filecol=None:
Name of the column that contains filenames.

(str) labelcol=None:
Name of the column that contains labels, not used here.

(iterable of str) othercols=None:
Name of the other columns to keep.

RETURNS
-------
(pandas.DataFrame) df:
Loaded dataframe.

RAISES
------
(ValueError) err:
If the file extension is not supported.


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


# load_labels_fromsheet


Load data labels from a sheet file.
You must load files before calling this, you might call
"load_data_fromdatapath". The labels are stored as "labels" attribute
and their unique values are stored as "unique_labels" attribute.

PARAMETERS
----------
(str) sheetpath:
Absolute path to the sheet which contain information about data.

(str) idcol=None:
Name of the column that contains at least a part of the filename.

(str) labelcol=None:
Name of the column that contains labels, not used here.

(array/list like of str) othercols=None:
Name of the other columns to keep.

(array/list like of str) clueless_words=None:
Strings considered as None.

(bool) delete_unlabeled_files=True:
If True, delete each file without label.

(bool) require_full_filename_match=False:
If True, requires the value in the idcol to be exactly the filename,
otherwise, if the value in the idcol is included in the filename,
it is considered as a match. Note that if the idcol value is
included in multiple filenames, it will be associated with the
first one found, in descending length order.

RETURNS
-------
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


# load_groups_fromsheet


Load data groups from a sheet file.
You must load files before calling this, you might call
"load_data_fromdatapath". The groups are stored as "groups" attribute.

PARAMETERS
----------
(str) sheetpath:
Absolute path to the sheet which contain information about data.

(str) idcol=None:
Name of the column that contains at least a part of the filename.

(str) groupcol=None:
Name of the column that contains groups, not used here.

(array/list like of str) clueless_words=None:
Strings considered as None.

(bool) require_full_filename_match=False:
If True, requires the value in the idcol to be exactly the filename,
otherwise, if the value in the idcol is included in the filename,
it is considered as a match. Note that if the idcol value is
included in multiple filenames, it will be associated with the
first one found, in descending length order.

RETURNS
-------
None


# _balance_dataset


Balance dataset so the amount of data is equal for each label.

PARAMETERS
----------
(dict<str;str>) data:
Dictionary with filename as key and label as value.

RETURNS
-------
(dict<str;str>) balanced_data:
Data without superfluous files to balance it.


# balance_datasets


Balance datasets so the amount of data is equal for each label.
This is basically calling "_balance_dataset" method with tdata then vdata.

PARAMETERS
----------
(dict<str;str>) tdata:
Train dictionary with filename as key and label as value.

(dict<str;str>) vdata:
Val dictionary with filename as key and label as value.

RETURNS
-------
(dict<str;str>) balanced_tdata:
Train data without superfluous files to balance it.

(dict<str;str>) balanced_vdata:
Val data without superfluous files to balance it.


# _split_using_groups


Split labeled data into train and test datasets considering data groups.

PARAMETERS
----------
(float) train_percentage=0.7:
Percentage of data expected in train dataset.

(bool) balance=False:
Do call "balance_datasets" method before returning dictionaries.

RETURNS
-------
(dict<str;str>) tdata:
Train dictionary with filename as key and label as value.

(dict<str;str>) vdata:
Val dictionary with filename as key and label as value.


# split


Split labeled data into train and test datasets.

PARAMETERS
----------
(float) train_percentage=0.7:
Percentage of data expected in train dataset.

(bool) balance=False:
Do call "balance_datasets" method before returning dictionaries.

(bool) ignore_groups=False:
If True, ignore groups for the split, even though it is defined.
If the "groups" attribute is not define, then it is ignored anyway.
If it is defined and "ignore_groups" is False, then the split is done
calling "_split_using_groups" method.

RETURNS
-------
(dict<str;str>) tdata:
train dictionary with filename as key and label as value.

(dict<str;str>) vdata:
val dictionary with filename as key and label as value.


# _distribute_data


Distribute files to process and split them between allowed cpus.
The distribution is returned as 2 lists of lists of src or dstdir.

PARAMETERS
----------
(str) dirpath:
Absolute path to the directory for treated files.

RETURNS
-------
(list<list<str>>) packed_srcs:
Source files absolute paths per process.

(list<list<str>>) packed_dstdirs:
Destination directories absolute paths per process.


# _distribute_datasets


Distribute files to process and split them between allowed cpus.
The distribution is returned into collections.

PARAMETERS
----------
(str) tdstdir:
Absolute path to the destination files directory for train dataset.

(str) vdstdir:
Absolute path to the destination files directory for val dataset.

(dict<str;str>) tdata:
Train dictionary with filename as key and label as value.

(dict<str;str>) vdata:
Val dictionary with filename as key and label as value.

RETURNS
-------
(list<list<str>>) packed_srcs:
Src files absolute paths per process.

(list<list<str>>) packed_dstdirs:
Destination directories absolute paths per process.


# _run_processes


Run processes on the maximum amount of allowed CPUs to apply "func"
function to each source file.
"func" needs "src" and "dstdir" params (in acutils, those are
prefixed with "tmnt").
**kwargs should be addionnal arguments to pass to the "func" function.

PARAMETERS
----------
(array/list like of iterables of str) packed_srcs:
src files absolute paths per process.

(array/list like of iterables of str) packed_dstdirs:
dst dirs absolute paths per process.

(function) func:
Treatment that will be applied on each source file
it needs an absolute path to the source file "src" and absolute
path to destination files directory "dstdir". In acutils,
any function prefixed with "tmnt" is usable.

**kwargs:
Arguments to pass to the "func" function.

RETURNS
-------
None


# _reset_directory


Delete directory if it exists, then create it again and fill it with
empty subdirecories, named from unique labels (if defined and not empty).

PARAMETERS
----------
(str) dirpath:
Absolute path to the directory to reset.

RETURNS
-------
None


# process


Run processes on the maximum amount of allowed CPUs to apply "func"
function to each source file. If "func" is None, just copy the file.
"func" needs "src" and "dstdir" params (in acutils, those are
prefixed with "tmnt").
**kwargs should be addionnal arguments to pass to the "func" function.

PARAMETERS
----------
(str) dirpath:
Absolute path to treated files directory.

(function) func=None:
Treatment that will be applied on each source file it needs an
absolute path to the source file "src" and absolute path to
destination files directory "dstdir". In acutils, any
function prefixed with "tmnt" is usable.

(bool) empty_dir=True:
If True, reset destination directory and fill it with unique labels
as subdirectories if defined

**kwargs:
Arguments to pass to the "func" function.

RETURNS
-------
None


# make_datasets


Run processes on the maximum amount of allowed CPUs to apply "func"
function to each source file.
"func" needs "src" and "dstdir" params (in acutils, those are prefixed with "tmnt").
**kwargs should be addionnal arguments to pass to the "func" function.

PARAMETERS
----------
(str) trainpath:
Absolute path to the destination files train directory.

(str) valpath:
Absolute path to the destination files val directory.

(dict<str;str>) tdata:
Train dictionary with filename as key and label as value.

(dict<str;str>) vdata:
Val dictionary with filename as key and label as value.

(function) func=None:
Treatment that will be applied on each source file it needs an
absolute path to the source file "src" and absolute path to
destination files directory "dstdir". In acutils, any
function prefixed with "tmnt" is usable.

(bool) empty_dir=True:
If True, reset destination directories and fill it with unique labels
as subdirectories if defined.

**kwargs:
Arguments to pass to the "func" function.

RETURNS
-------
None


# save_split


Save a split (from "split" method) as a json file.

PARAMETERS
----------
(str) dst:
absolute path to the new json file.

(dict<str;str>) data:
data dictionary to save.

RETURNS
-------
None


# load_split


Load a dictionary from a json file.

PARAMETERS
----------
(str) src:
absolute path to the json file.

RETURNS
-------
(dict<str;str>) data:
loaded data dictionary.


