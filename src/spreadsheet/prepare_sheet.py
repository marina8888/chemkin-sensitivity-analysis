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
    tfr = pd.read_csv(path_to_sheet, chunksize=100000, iterator=True)
    sens_df = pd.concat(tfr, ignore_index=True)
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

    for file in os.listdir(path_to_folder):
        if file.endswith(".csv"):
            sens_df1 = pd.read_csv(file)
            sens_df.join(sens_df1)

    # returns a dataframe of all sheets joined together, which can be used as input for plotting functions:
    return sens_df