# sheet

# delete_clueless_rows


Delete rows of a Pandas DataFrame based on the values in clueless_words.
Delete each row that have any empty cell or any cell that contain a
clueless_word. If columns argument is specified, only those columns
will be concerned.

PARAMETERS
----------
(pandas.DataFrame) df:
The DataFrame to filter.

(list<str>) clueless_words=None:
Any cell containing a word of the list is treated as empty.

(list<str>) columns=None:
Columns considered for the deletion.

(bool) inplace=False:
If True, the DataFrame will be modified in place, else it is returned.

RETURNS
-------
(pandas.DataFrame) df=None:
Filtered copy of passed df, if inplace==True returns None.


# read_df_from_any_avalaible_extensions


Load a Pandas DataFrame from a file.
Avalaible extensions: csv, txt, xls, xlsx, feather, parquet,
hdf5, sas7bdat, stata, pickle.

PARAMETERS
----------
(str) sheetpath:
Absolute path of the file to load.

RETURNS
-------
(pandas.DataFrame) df:
The DataFrame loaded from the file.

RAISES
------
(ValueError) err:
If the file extension is not supported.


# add_suffix_to_cells_from_a_column


Concatenate a string with the values in certain columns of a Pandas DataFrame.

PARAMETERS
----------
(pandas.DataFrame) df:
The DataFrame to modify.

(str) suffix:
The string to concatenate with the values in the specified columns.

(list) columns:
A list of column names to concatenate with the string.

(bool) inplace=False:
If True, the DataFrame will be modified in place, else it is returned.

RETURNS
-------
(pandas.DataFrame) df=None:
Modified copy of passed df, if inplace==True returns None.


