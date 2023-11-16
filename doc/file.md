# file

# copyfile


Copy a file from src to dst without checking anything.

PARAMETERS
----------
- src (str): absolute path to the file that will be copied.
- dst (str): absolute path to the future copied file.

RETURNS
-------
None

RAISES
------
None


# copyfile_with_safety


Copy a file from src to dst and check if src file and dst directory are existing.

PARAMETERS
----------
- src (str): absolute path to the file that will be copied.
- dst (str): absolute path to the future copied file.

RETURNS
-------
None

RAISES
------
None


# tmnt_copyfile_to_dir


Copy a file from src to a dst directory.

PARAMETERS
----------
- src (str): absolute path to the file that will be copied.
- dstdir (str): absolute path to the directory that should contain the copy.
- newfilename=None (str): filename expected, if None src filename is used.
- safecopy=True (bool): if True copyfile_with_safety is called, else copyfile is called.

RETURNS
-------
None

RAISES
------
None


# copyfiles_to_dir


Copy multiple files from srcs to a dst directory using "copyfile_to_dir" function.

PARAMETERS
----------
- srcs (iterable of str): absolute paths to the files that will be copied.
- dstdir (str): absolute path to the directory that should contain the copy.
- newfilename=None (str): filename expected, if None src filename is used.
- safecopy=True (bool): if True copyfile_with_safety is called, else copyfile is called.

RETURNS
-------
None

RAISES
------
None


# reset_directory


Delete directory if it exists, then create it again and fill it with
empty subdirecories named from subs argument.

PARAMETERS
----------
- dirpath (str): absolute path to the directory to reset.
- subs (list<str>): name of the subdirectories that should be in dirpath.

RETURNS
-------
None

RAISES
------
None


# tmnt_generate_documentation


Extract documentation inside python file and fill it into markdown file.

PARAMETERS
----------
- src (str): absolute path to the python file.
- dstdir (str): absolute path to the new markdown file.

RETURNS
-------
None

RAISES
------
None


