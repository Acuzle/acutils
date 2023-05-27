import pandas as pd



# A function prefixed with "tmnt" is a treatment function and must have those parameters:
#  - src: absolute path to the file that will be processed (str)
#  - dstdir: absolute path to the directory that should contain new files (str)
# Also, it shouldn't return anything.



def delete_clueless_rows(df, clueless_words=None, columns=None, inplace=False):
    '''
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
    '''
    if clueless_words is None:
        clueless_words = []
    
    if columns is None or len(columns) == 0:
        columns = df.columns

    # Create a mask that is True for rows that should be retained
    mask = df[columns].applymap(lambda x: x not in clueless_words and x is not None)

    # If inplace is True, update the DataFrame in place
    if inplace:
        df.drop(df[~mask].index, inplace=True)
    else:  # Otherwise, return a filtered copy of the DataFrame
        return df[mask]



def read_df_from_any_avalaible_extensions(sheetpath):
    '''
    Load a Pandas DataFrame from a file.
    Avalaible extensions: csv, txt, xls, xlsx, feather, parquet, hdf5, sas7bdat, stata, pickle.
    \nPARAMETERS
      sheetpath (str): absolute path of the file to load
    \nRETURNS
      df (pandas.DataFrame): The DataFrame loaded from the file.
    \nRAISES
      ValueError: If the file extension is not supported.
    '''
    # Determine the file extension
    _, file_extension = sheetpath.rsplit('.', 1)

    # Load the DataFrame using the appropriate reader based on the file extension
    if file_extension in ['csv', 'txt']:
        return pd.read_csv(sheetpath)
    elif file_extension in ['xls', 'xlsx']:
        return pd.read_excel(sheetpath)
    elif file_extension in ['feather', 'parquet', 'hdf5']:
        return pd.read_feather(sheetpath)
    elif file_extension == 'sas7bdat':
        return pd.read_sas(sheetpath)
    elif file_extension == 'stata':
        return pd.read_stata(sheetpath)
    elif file_extension == 'pickle':
        return pd.read_pickle(sheetpath)
    else:
        raise ValueError(f'Unsupported file extension: {file_extension}')



def add_suffix_to_cells_from_a_column(df, suffix, columns, inplace=False):
    '''
    Concatenate a string with the values in certain columns of a Pandas DataFrame.
    \nPARAMETERS
      df (pandas.DataFrame): The DataFrame to modify.
      suffix (str): The string to concatenate with the values in the specified columns.
      columns (list): A list of column names to concatenate with the string.
      inplace=False (bool): If True, the DataFrame will be modified in place, else it is returned
    \nRETURNS
      df=None (pandas.DataFrame): modified copy of passed df, if inplace==True returns None
    '''
    if inplace:
        for col in columns:
            df[col] = df[col].apply(lambda x: f'{x}{suffix}')
    else:
        df_modified = df.copy()
        for col in columns:
            df_modified[col] = df_modified[col].apply(lambda x: f'{x}{suffix}')
        return df_modified