# file

## copyfile

```
Copy a file from src to dst without checking anything.
    \nPARAMETERS
      src (str): absolute path to the file that will be copied
      dst (str): absolute path to the future copied file
```

## copyfile_with_safety

```
Copy a file from src to dst and check if src file and dst directory are existing.
    \nPARAMETERS
      src (str): absolute path to the file that will be copied
      dst (str): absolute path to the future copied file
```

## tmnt_copyfile_to_dir

```
Copy a file from src to a dst directory.
    \nPARAMETERS
      src (str): absolute path to the file that will be copied
      dstdir (str): absolute path to the directory that should contain the copy
      newfilename=None (str): filename expected, if None src filename is used
      safecopy=True (bool): if True copyfile_with_safety is called, else copyfile is called
```

## copyfiles_to_dir

```
Copy multiple files from srcs to a dst directory using "copyfile_to_dir" function.
    \nPARAMETERS
      srcs (iterable of str): absolute paths to the files that will be copied
      dstdir (str): absolute path to the directory that should contain the copy
      newfilename=None (str): filename expected, if None src filename is used
      safecopy=True (bool): if True copyfile_with_safety is called, else copyfile is called
```

## reset_directory

```
Delete directory if it exists, then create it again and fill it with
    empty subdirecories named from subs argument.
    \nPARAMETERS
      dirpath (str): absolute path to the directory to reset
      subs (list<str>): name of the subdirectories that should be in dirpath
```

## tmnt_generate_documentation

```
Extract documentation inside python file and fill it into markdown file.
    \nPARAMETERS
      src (str): absolute path to the python file
      dstdir (str): absolute path to the new markdown file
```

