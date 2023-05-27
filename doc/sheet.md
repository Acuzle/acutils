# sheet

## delete_clueless_rows

```
Delete rows of a Pandas DataFrame based on the values in clueless_words.
    Delete each row that have any empty cell or any cell that contain a clueless_word.
    If columns argument is specified, only those columns will be concerned.
    \nPARAMETERS
      df (pandas.DataFrame): The DataFrame to filter.
      clueless_words=None (list<str>): any cell containing a word of the list is treated as empty
      columns=None (list<str>): columns considered for the deletion
      inplace=False (bool): If True, the DataFrame will be modified in place, else it is returned
    \nRETURNS
      df=None (pandas.DataFrame): filtered copy of passed df, if inplace==True returns None
```

## read_df_from_any_avalaible_extensions

```
Load a Pandas DataFrame from a file.
    Avalaible extensions: csv, txt, xls, xlsx, feather, parquet, hdf5, sas7bdat, stata, pickle.
    \nPARAMETERS
      sheetpath (str): absolute path of the file to load
    \nRETURNS
      df (pandas.DataFrame): The DataFrame loaded from the file.
    \nRAISES
      ValueError: If the file extension is not supported.
```

## add_suffix_to_cells_from_a_column

```
Concatenate a string with the values in certain columns of a Pandas DataFrame.
    \nPARAMETERS
      df (pandas.DataFrame): The DataFrame to modify.
      suffix (str): The string to concatenate with the values in the specified columns.
      columns (list): A list of column names to concatenate with the string.
      inplace=False (bool): If True, the DataFrame will be modified in place, else it is returned
    \nRETURNS
      df=None (pandas.DataFrame): modified copy of passed df, if inplace==True returns None
```

