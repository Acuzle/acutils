# sheet

# delete_clueless_rows


Delete rows of a Pandas DataFrame based on the values in clueless_words.
Delete each row that have any empty cell or any cell that contain a
clueless_word. If columns argument is specified, only those columns
will be concerned.

PARAMETERS
----------
- df (pandas.DataFrame): The DataFrame to filter.
- clueless_words=None (list<str>): Any cell containing a word of the list
is treated as empty.
- columns=None (list<str>): Columns considered for the deletion.
- inplace=False (bool): If True, the DataFrame will be modified in place,
else it is returned.

RETURNS
- df=None (pandas.DataFrame): Filtered copy of passed df,
if inplace==True returns None.

RAISES
------
None


# read_df_from_any_avalaible_extensions


Load a Pandas DataFrame from a file.
Avalaible extensions: csv, txt, xls, xlsx, feather, parquet,
hdf5, sas7bdat, stata, pickle.

PARAMETERS
----------
- sheetpath (str): Absolute path of the file to load.

RETURNS
-------
- df (pandas.DataFrame): The DataFrame loaded from the file.

RAISES
------
ValueError: If the file extension is not supported.


# add_suffix_to_cells_from_a_column


Concatenate a string with the values in certain columns of a Pandas DataFrame.

PARAMETERS
----------
- df (pandas.DataFrame): The DataFrame to modify.
- suffix (str): The string to concatenate with the values in the specified
columns.
- columns (list): A list of column names to concatenate with the string.
- inplace=False (bool): If True, the DataFrame will be modified in place,
else it is returned.

RETURNS
-------
- df=None (pandas.DataFrame): Modified copy of passed df, if inplace==True
returns None.

RAISES
------
None


