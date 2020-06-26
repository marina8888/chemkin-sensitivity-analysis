import os
import pandas as pd

def add_distance(path_to_sheet):

    # convert data into df called sens_df:
    sens_df = pd.read_csv(path_to_sheet)
    sens_df['Distance (m)'] = None
    total_index = len(sens_df.index)
    for row in range(0, total_index, 1):
        sens_df.loc[row,'Distance (m)'] = float(0.02/(total_index-1))*(row)

    print(sens_df)
    return sens_df

def join_files(path_to_folder):
    sens_df = pd.DataFrame()

    for file in os.listdir(path_to_folder):
        if file.endswith(".csv"):
            sens_df1 = pd.read_csv(file)
            sens_df.join(sens_df1)
    return sens_df