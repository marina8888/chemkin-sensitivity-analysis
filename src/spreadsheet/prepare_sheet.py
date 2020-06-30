import os
import pandas as pd

def add_distance(path_to_sheet, total_distance):
    """
    Add a Distance (m) column to a sheet and return a dataframe.

    Parameters
    ----------
    path_to_sheet
    total_distance

    Returns
    -------

    """

    # convert data into df called sens_df:
    if isinstance(path_to_sheet, str):
        sens_df = pd.read_csv(path_to_sheet)
    else:
        sens_df = path_to_sheet

    sens_df['Distance (m)'] = None
    total_index = len(sens_df.index)
    for row in range(0, total_index, 1):
        sens_df.loc[row,'Distance (m)'] = round(float(total_distance/(total_index-1))*(row), 4)

    # returns a dataframe of all sheets joined together, which can be used as input for plotting functions:
    return sens_df

def join_files(path_to_folder):
    """
    Takes a folder of .csv sheets and returns one large dataframe including all sheets called sens_df (sensitivity data dataframe).

    Parameters
    ----------
    path_to_folder

    Returns
    -------

    """
    sens_df = pd.DataFrame()
    list=[]

    # check file ends in csv and not empty:
    for file in os.listdir(path_to_folder):
        if file.endswith(".csv"):
            path = os.path.join(path_to_folder, file)
            filesize = os.path.getsize(path)
            if filesize is not 0:
                list.append(os.path.join(path_to_folder, file))

    sens_df = pd.read_csv(list[0])
    for i in range(1,len(list),1):
        temp = pd.read_csv(list[i])
        sens_df = sens_df.merge(temp)

    # returns a dataframe of all sheets joined together, which can be used as input for plotting functions:
    return sens_df

def remove_spaces(df):
    """
    Add space to all columns. Required when export is done from task bar instead of analysis window.
    Parameters
    ----------
    df

    Returns
    -------

    """
    new_df = pd.DataFrame()
    if isinstance(df, str):
        new_df = pd.read_csv(df)
    else:
        new_df = df
    new_df.columns = df.columns.str.lstrip()

    return new_df
