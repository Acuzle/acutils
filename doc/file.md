# file

# copyfile


Copy a file from src to dst without checking anything.

PARAMETERS
----------
(str) src:
absolute path to the file that will be copied.

(str) dst:
absolute path to the future copied file.

RETURNS
-------
None


# copyfile_with_safety


Copy a file from src to dst and check if src file and dst directory are existing.

PARAMETERS
----------
(str) src:
absolute path to the file that will be copied.

(str) dst:
absolute path to the future copied file.

RETURNS
-------
None


# tmnt_copyfile_to_dir


Copy a file from src to a dst directory.

PARAMETERS
----------
(str) src:
absolute path to the file that will be copied.

(str) dstdir:
absolute path to the directory that should contain the copy.

(str) newfilename=None:
filename expected, if None src filename is used.

(bool) safecopy=True:
if True copyfile_with_safety is called, else copyfile is called.

RETURNS
-------
None


# copyfiles_to_dir


Copy multiple files from srcs to a dst directory using "copyfile_to_dir" function.

PARAMETERS
----------
(iterable of str) srcs:
absolute paths to the files that will be copied.

(str) dstdir:
absolute path to the directory that should contain the copy.

(str) newfilename=None:
filename expected, if None src filename is used.

(bool) safecopy=True:
if True copyfile_with_safety is called, else copyfile is called.

RETURNS
-------
None


# reset_directory


Delete directory if it exists, then create it again and fill it with
empty subdirecories named from subs argument.

PARAMETERS
----------
(str) dirpath:
absolute path to the directory to reset.

(list<str>) subs:
name of the subdirectories that should be in dirpath.

RETURNS
-------
None


# tmnt_generate_documentation


Extract documentation inside python file and fill it into markdown file.

PARAMETERS
----------
(str) src:
absolute path to the python file.

(str) dstdir:
absolute path to the new markdown file.

RETURNS
-------
None


# save_dict_as_json


Save a dictionary as a json file.

PARAMETERS
----------
(str) dst:
absolute path to the new json file.

(dict<str;str>) data:
data dictionary to save.

RETURNS
-------
None


# load_dict_from_json


Load a dictionary from a json file.

PARAMETERS
----------
(str) src:
absolute path to the json file.

RETURNS
-------
(dict<str;str>) data:
loaded data dictionary.


