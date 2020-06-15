import pandas as pd
import os
import openpyxl

class Spreadsheet():
    def __init__(self, name_of_sensitivity_folder: str, name_of_mech_file):
        #format mech and spreadsheets to pandas:
        self.df_list = self.create_pd(name_of_sensitivity_folder)
        self.create_cols()
        self.convert_cm3_to_m3()
        self.mech_list = self.create_mech(name_of_mech_file)

        #convert spreadsheet column names:
        self.rename_col()
        self.print_excel()

    def create_pd(self, name_of_sensitivity_folder):
        """
        create list of dataframes from csv files
        """
        df_list = []
        self.file_list = []
        path = os.path.join('data', name_of_sensitivity_folder)
        for file in os.listdir(path):
            if file.endswith(".csv"):
                self.file_list.append(file)
                full_path = os.path.join(path, file)
                sens_df = pd.read_csv(full_path)
                df_list.append(sens_df)
        return df_list

    def create_mech(self, mech_file):
        """
        create a list of numbered
        """
        lines = []
        stripped_l = []
        full_path = os.path.join('mechanisms', mech_file)
        with open(full_path, 'r') as f:
            lines = f.readlines()
        for l in enumerate(filter(lambda l: "=" in l, lines)):
            ele_l = (l[1].split(' '))
            ele_l = [elem for elem in ele_l if elem.strip()]
            ele_l.insert(0, l[0])
            stripped_l.append(ele_l)
        return stripped_l


    def create_cols(self):
        for df in self.df_list:
            df['dI'] = None

    def convert_cm3_to_m3(self):
        for df in self.df_list:
            df.iloc[:, 2:] = df.iloc[:, 2:] .apply(lambda x: x * 1000000)

    def rename_col(self):
        for df in self.df_list:
            for col in df.columns.values:
                if 'GasRxn#' in col:
                    mech_num = col.split('#')[1]
                    mech_num = mech_num.split(' ')[0]
                    for m in self.mech_list:
                        if mech_num == str(m[0]):
                            col_gas = col.split('_')[0] + '_' + col.split('_')[1] + '_'
                            new_col = col_gas + str(m[1])
                            df.rename(columns={col: new_col}, inplace = True)

    def print_excel(self):
        for df, f in zip(self.df_list, self.file_list):
            df.to_excel('./output/' + f + '.xlsx',sheet_name='all_ROP')
