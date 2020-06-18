import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np

# set a global style for all graphs:
plt.style.use('seaborn-notebook')


class Graph():
    def __init__(self, list_of_eq: list, title: str, x_axis_label: str = 'Sensitivity', x_graph_size: int = 6,
                 y_graph_size: int = 6.5):
        """
        Initialise a graph, based on object arguments. One figure is created per new graph object.
        :param x_axis_label:
        :param list_of_equations_considered:
        :param title: the title that will be set for the graph
        :param x_graph_size: default to almost square size 6 (increase number to change size ratio or increase resolution)
        :param y_graph_size: and default to almost square size 6.5 (increase number to change size ratio or increase resolution)
        """
        self.fig = plt.figure(figsize=(x_graph_size, y_graph_size))

        # get access to axies functions:
        self.ax = self.fig.gca()

        # set format variables and format the figure:
        self.x_axis_label = x_axis_label
        self.list_of_x = list_of_eq
        self.title = title

        self.add_format()

        self.list_of_eq = list_of_eq

    def add_format(self):
        """
        Format graph. Add title, axies, tight layout, padding and grid.
        :return:
        """
        # add title, names and layout:
        plt.title(self.title, pad=15, figure=self.fig)
        plt.xlabel(self.x_axis_label, figure=self.fig)
        self.ax.set_xticklabels(self.list_of_x, figure=self.fig)

    def find_col_headers(self, list_val, df, gas=None):
        '''
        find 'gas + equation' (from equation list) in column headers and add to list_val the true column headers:
        '''
        if gas is not None:
            # call this version for species sensitivity:
            for eq in self.list_of_x:
                column_header = gas + '_Sens_' + eq
                res = filter(lambda x: column_header in x, df.columns.values)
                if res.startswith(gas):
                    list_val.append(res)
                    print(list_val)
                else:
                    list_val.append(0)
                    print(list_val)
        else:
            # call this version for laminar burning velocity sensitivity:
            for eq in self.list_of_x:
                column_header = 'Flow_rate_Sens_' + eq
                res = filter(lambda x: column_header in x, df.columns.values)

                if res is None:
                    list_val.append(0)
                    print(list_val)
                else:
                    list_val.append(res)
                print(list_val)

        return list_val

    def find_col_values(self):
        pass

    def plot_bar_species(self, name_of_folder_n_sheet: str, gas_to_add: str, legend: str, multiplier: float = 1,
                         colour: str = 'red', X_cm: int = 2):
        '''
        this function takes REACTION SENSITIVITY values from a spreadsheet at default distance X(cm) = 2.0 and plots them.
        The  user can modify this distance to better describe the point at which gases were samples,
        (which is usually the end point of the combustor)
        '''
        # convert data into df called sens_df:
        list_val = []
        full_path = os.path.join('./data/', name_of_folder_n_sheet)
        sens_df = pd.read_csv(full_path)

        # find 'gas + equation' (from equation list) in column headers and add to list_val the true column headers:
        self.find_col_headers(list_val, sens_df, gas_to_add)

        # use the column headers in list_val to return a list of values located at X(cm)

        # bar chart settings:
        bar_width = 0.25
        ind = np.arange(len(list_val))

        self.ax.barh(ind, list_val, bar_width, align='center')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_xticks(ind + bar_width / 2)
        self.ax.legend()

    def plot_bar_lam_burning_v(self, name_of_folder_n_sheet: str, legend: str, multiplier: float = 1,
                               colour: str = 'green', X_cm: int = 0):
        '''
        this function takes LAMINAR BURNING VELOCITY SENSITIVITY and plots it on a bar chart at default distance = 0 cm.
        The  user can modify this distance to better describe where the unburnt mixture flowrate should be taken.
        '''
        pass

    def show_and_save(self, path_of_save_folder: str, name: str):
        """
        shows and saves the figure - must be called to show the figure at the end of plotting
        :param self:
        :param path_of_save_folder: save figures to this folder
        :param name: save figures under this name
        :return:
        """
        full_path = os.path.join(path_of_save_folder, name)
        plt.savefig(full_path, dpi=300, bbox_inches="tight")
        plt.close(self.fig)
