import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np

# set a global style for all graphs:
plt.style.use('seaborn-notebook')


class Graph():
    def __init__(self, title: str, list_of_eq:list, x_axis_label: str = 'Sensitivity', x_graph_size: int = 6,
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
        self.list_of_eq = list_of_eq
        self.title = title

        self.add_format()

    def add_format(self):
        """
        Format graph. Add title, axies, tight layout, padding and grid.
        :return:
        """
        # add title, names and layout:
        plt.title(self.title, pad=15, figure=self.fig)
        plt.xlabel(self.x_axis_label, figure=self.fig)
        self.ax.set_xticklabels(self.list_of_eq, figure=self.fig)

    def find_col_headers(self, df, eq_list, gas=None):
        '''
        find 'gas + equation' (from equation list) in column headers and add to list_val the true column headers:
        '''
        filtered_eqs = []
        # call this for species sensitivity:
        if gas is not None:
            for eq in eq_list:
                column_header = gas + '_Sens_' + eq
                filtered_eqs += (list(filter(lambda x: column_header in x, df.columns.values)))

            filtered_eqs = [f for f in filtered_eqs if f.startswith(gas + '_')]

        # call this for laminar burning velocity sensitivity:
        else:
            for eq in self.list_of_eq:
                column_header = 'Flow_rate_Sens_' + eq
                filtered_eqs = list(filter(lambda x: column_header in x, df.columns.values))

        if not filtered_eqs:
            print('no values for equations that contain the gas provided:')
            return None
        else:
            return filtered_eqs

    def find_col_values(self):
        pass

    def plot_bar_species(self, name_of_folder_n_sheet: str, gas_to_add: str, legend: str, multiplier: float = 1,
                         colour: str = 'red', X_cm: int = 2, all_eq: bool = False):
        '''
        this function takes REACTION SENSITIVITY values from a spreadsheet at default distance X(cm) = 2.0 and plots them.
        The  user can modify this distance to better describe the point at which gases were samples,
        (which is usually the end point of the combustor)
        '''
        # convert data into df called sens_df:
        full_path = os.path.join('./data/', name_of_folder_n_sheet)
        sens_df = pd.read_csv(full_path)
        # find 'gas + equation' (from equation list) in column headers and add to list_col_h the true column headers:
        if all_eq is False:
            list_col_h = self.find_col_headers(sens_df, self.list_of_eq, gas_to_add)

        elif all_eq is True:
            all_eq_list = []
            # plot gas match for all equations in df, not just those mentioned when Graph() object was initialised.
            for s in sens_df.columns.values:
                try:
                    h = s.split('_')[2]
                    if '=' in h and h not in all_eq_list:
                        all_eq_list.append(s.split('_')[2])
                except IndexError:
                    print(s + ' not added to eq list because its not an equation')
        # modify the x label so it now includes all equations, not just those added when a Graph object was initialised
            plt.xlabel(all_eq_list, figure=self.fig)
            list_col_h = self.find_col_headers(sens_df, all_eq_list, gas_to_add)

        if list_col_h is not None:

            # use the column headers in list_col_h to return a list of values located at X(cm)

            # bar chart settings:
            bar_width = 0.25
            ind = np.arange(len(list_col_h))

            self.ax.barh(ind, list_col_h, bar_width, align='center')

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
