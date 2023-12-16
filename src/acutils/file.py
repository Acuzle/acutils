# Functions prefixed with "tmnt" are treatments and must have those parameters:
#  - src: absolute path to the file that will be processed (str)
#  - dstdir: absolute path to the directory that should contain new files (str)
# Also, nothing should be returned.

import json
import os
import re
import shutil



def copyfile(src, dst):
    '''
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
    '''
    shutil.copyfile(src, dst)



def copyfile_with_safety(src, dst):
    '''
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
    '''
    if os.path.isfile(src):
        if os.path.isdir(os.path.dirname(dst)):
            copyfile(src, dst)
        else:
            print(f"|WRN| dir not found {os.path.dirname(dst)}")
    else:
        print(f"|WRN| file not found {src}")



def tmnt_copyfile_to_dir(src, dstdir, newfilename=None, safecopy=True):
    '''
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
    '''
    if newfilename is str:
        dst = os.path.join(dstdir, newfilename)
    else:
        dst = os.path.join(dstdir, os.path.basename(src))
        if newfilename is not None:
            print(f"|WRN| newfilename should be str, not {type(newfilename)}, src filename used")
    
    if safecopy:
        copyfile_with_safety(src, dst)
    else:
        copyfile(src, dst)



def copyfiles_to_dir(srcs, dstdir, newfilename=None, safecopy=True):
    '''
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
    '''
    for src in srcs:
        tmnt_copyfile_to_dir(src, dstdir, newfilename, safecopy)



def reset_directory(dirpath, subs=[]):
    '''
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
    '''
    if os.path.isdir(dirpath): shutil.rmtree(dirpath) # remove existing files
    os.mkdir(dirpath) # create the new empty directory
    for subdir in subs: # fill it with new empty subdirectories
        os.mkdir(os.path.join(dirpath, subdir))



def tmnt_generate_documentation(src, dstdir):
    '''
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
    '''
    # Read the source file into a string
    with open(src, 'r') as f:
        source = f.read()

    # Extract the documentation for each function in the source file
    lines = source.split('\n')
    functions = []
    docstrings = []
    in_function = False
    docstring = ''
    in_doc = False
    for line in lines:
        if line.strip().startswith('def'):
            if len(functions) > 0: docstrings.append(docstring)
            in_function = True
            in_doc = False
            match = re.match(r'def (\w+)\(', line.strip())
            if match is not None:
                function_name = match.group(1)
                functions.append(function_name)
                docstring = ''
        elif (in_function or in_doc) and line.strip().startswith("'''"):
            in_function = False
            if in_doc:
                in_doc = False
            else:
                in_doc = True
        elif in_doc:
            docstring += '\n' + line.strip()
    docstrings.append(docstring)

    # Write the documentation to the target file
    target_file = os.path.join(dstdir, f"{os.path.basename(src)[:-2]}md")
    with open(target_file, 'w') as f:
        f.write(f'# {os.path.basename(target_file)[:-3]}\n\n')
        for function, docstring in zip(functions, docstrings):
            f.write(f'# {function}\n\n\n')
            f.write(docstring.strip())
            f.write('\n\n\n')



def save_dict_as_json(dst, data):
    '''
    Save a dictionary as a json file.

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
    '''
    with open(dst, "w") as json_file:
        json.dump(data, json_file)



def load_dict_from_json(src):
    '''
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
    '''
    with open(src, "r") as json_file:
        return json.load(json_file)