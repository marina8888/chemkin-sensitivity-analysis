import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np

# set a global style for all graphs:
plt.style.use('seaborn-notebook')


class Graph():
    def __init__(self, title: str, x_axis_label: str = 'Sensitivity', x_graph_size: int = 6,
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
        plt.title(title, pad=15, figure=self.fig)

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
            for eq in eq_list:
                column_header = 'Flow_rate_Sens_' + eq
                filtered_eqs += list(filter(lambda x: column_header in x, df.columns.values))

        if not filtered_eqs:
            print('no values for equations that contain the gas provided:')
            return None
        else:
            return filtered_eqs

    def find_col_values(self, df, list, Xcm_val, i : int = 2):
        d_name = []
        d_val = []

        for l in list:
            # filter and take relevant values from dataframe and add to list. Extract all values as a list of lists
            mask = df['Distance (m)'] == Xcm_val
            data_df = df[mask]
            d = pd.Series(data_df[l])
            d_name.append(d.name.split('_')[i])
            d_val.append(d.values[0])
        return d_val, d_name

    def plot_bar(self, col_val, col_label, colour, gas_to_add = None):
        if col_val is not None:
            # bar chart settings:
            bar_width = 0.25
            ind = np.arange(len(col_label))
            print(col_val)
            print(col_label)

            if gas_to_add is None:
                self.ax.barh(ind, col_val, bar_width, label='Sensitivity for laminar burning velocity', align='edge',
                             tick_label=col_label, zorder=10, color=colour)

            else:
                self.ax.barh(ind, col_val, bar_width, label='Sensitivity for ' + gas_to_add, align='edge',
                         tick_label=col_label, zorder = 10, colour = colour)
            # Move left y-axis and bottim x-axis to centre, passing through (0,0)
            self.ax.spines['left'].set_position('zero')
            self.ax.spines['bottom'].set_position('zero')

            # Eliminate upper and right axes
            self.ax.spines['right'].set_color('none')
            self.ax.spines['top'].set_color('none')

            # Show ticks in the left and lower axes only
            self.ax.xaxis.set_ticks_position('bottom')
            self.ax.yaxis.set_ticks_position('right')

            # Set ticks:
            self.ax.grid(b=True, which='major', linestyle='-', linewidth='1.0', color='gainsboro', zorder=0,
                         figure=self.fig)
            self.ax.grid(b=True, which='minor', linestyle=':', linewidth='0.5', color='silver', zorder=0,
                         figure=self.fig)
            self.ax.legend()

    def plot_bar_species(self, name_of_folder_n_sheet: str, gas_to_add: str, list_of_eq=None, multiplier: float = 1,
                         colour: str = 'red', X_cm: float = 0.02, offset: float = 0):
        '''
        this function takes REACTION SENSITIVITY values from a spreadsheet at default distance X(cm) = 2.0 and plots them.
        The  user can modify this distance to better describe the point at which gases were samples,
        (which is usually the end point of the combustor).
        '''
        # convert data into df called sens_df:
        full_path = os.path.join('./data/', name_of_folder_n_sheet)
        sens_df = pd.read_csv(full_path)

        # initalise x axis labels and x axis values:
        list_col_h = []
        col_val = []
        col_label = []

        # find 'gas + equation' (from equation list) in column headers and add to list_col_h the true column headers:
        if list_of_eq is not None:
            list_col_h = self.find_col_headers(sens_df, list_of_eq, gas_to_add)

        # plot gas match for all equations in df:
        else:
            print(sens_df.columns.values)
            all_eq_list = []
            for s in sens_df.columns.values:
                try:
                    h = s.split('_')[2]
                    if '=' in h and h not in all_eq_list:
                        all_eq_list.append(s.split('_')[2])
                except IndexError:
                    print(s + ' not added to eq list because its not an equation')
            list_col_h = self.find_col_headers(sens_df, all_eq_list, gas_to_add)

        if list_col_h is not None:
            col_val, col_label = self.find_col_values(sens_df, list_col_h, X_cm)
            self.plot_bar(col_val*multiplier, col_label, colour, gas_to_add)

    def plot_bar_lam_burning_v(self, name_of_folder_n_sheet: str, list_of_eq=None, multiplier: float = 1,
                         colour: str = 'red', X_cm: float = 0, offset: float = 0):
        '''
        this function takes LAMINAR BURNING VELOCITY SENSITIVITY and plots it on a bar chart at default distance = 0 cm.
        The  user can modify this distance to better describe where the unburnt mixture flowrate should be taken.
        '''
        # convert data into df called sens_df:
        full_path = os.path.join('./data/', name_of_folder_n_sheet)
        sens_df = pd.read_csv(full_path)
        # initalise x axis labels and x axis values:
        list_col_h = []
        col_val = []
        col_label = []

        # find 'gas + equation' (from equation list) in column headers and add to list_col_h the true column headers:
        list_col_h = self.find_col_headers(sens_df, list_of_eq)
        print(list_col_h)
        if list_col_h is not None:
            col_val, col_label = self.find_col_values(sens_df, list_col_h, X_cm, 3)
            self.plot_bar(col_val*multiplier, col_label, colour)


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
