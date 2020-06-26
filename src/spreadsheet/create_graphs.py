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

        Parameters
        ----------
        title : is the title of the graph
        x_axis_label : x label
        x_graph_size : width of graph with default value
        y_graph_size : height of graph with default value
        """
        # get access to axies functions:
        self.fig, self.ax = plt.subplots(figsize=(x_graph_size, y_graph_size))

        # set format variables and format the figure:
        plt.xlabel(x_axis_label)
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

    def find_col_values(self, df, list, Xcm_val, i : int = 2, filter_above = None, filter_below = None):
        """
        Find values based on input df and a list, such that a series of x and corresponding y values is filtered and generated.

        Parameters
        ----------
        df
        list
        Xcm_val
        i
        filter_above
        filter_below

        Returns
        -------

        """
        d_name = []
        d_val = []

        mask1 = df['Distance (m)'] == Xcm_val
        data_df = df[mask1].copy(deep = True)

        # add filter condition to df:
        if filter_above is not None and filter_below is not None:
            data_df1 = data_df.loc[:,(data_df > filter_above).any()].copy(deep = True)
            data_df2 = data_df.loc[:,(data_df < filter_below).any()].copy(deep = True)
            data_df = data_df1.join([data_df2])
            # data_df = data_df[(df > filter_above) & (df < filter_below)]
        elif filter_above is not None:
            print("filtering above")
            data_df = data_df.loc[:, (data_df > filter_above).any()].copy(deep = True)

        elif filter_below is not None:
            print("filtering below")
            data_df = data_df.loc[:, (data_df < filter_below).any()].copy(deep = True)

        for l in list:
            # filter and take relevant values from dataframe and add to list. Extract all values as a list of lists
            if l in data_df.columns.values:
                print(l)
                d = pd.Series(data_df[l])
                d_name.append(d.name.split('_')[i])
                print(d_name)
                # print(d_name)
                d_val.append(d.values[0])
        return d_val, d_name

    def plot_bar(self, col_val, col_label, colour, gas_to_add = None, offset = 0):
        """
        Simple bar graph plot including setting ticks and correct axis locations.
        """
        if col_val is not None:
            # sort in order for x labels to match:
            col_label, col_val = zip(*sorted(zip(col_label, col_val)))

            bar_width = 0.15
            ind = np.arange(len(col_label))

            if gas_to_add is None:
                self.ax.barh(ind+offset, col_val, bar_width, label='Sensitivity for laminar burning velocity', align='edge',
                             tick_label=col_label, zorder=10, color=colour)

            else:
                self.ax.barh(ind+offset, col_val, bar_width, label='Sensitivity for ' + gas_to_add, align='edge',
                         tick_label=col_label, zorder = 10, color = colour)
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

    def plot_bar_species(self, path_to_sheet_or_df, gas_to_add: str, list_of_eq: list = None, multiplier: float = 1, filter_above = None, filter_below= None,
                         colour: str = 'b', X: float = 0.02, offset: float = 0):
        """
        This function takes REACTION SENSITIVITY values from a spreadsheet at default distance X = 0.02 and plots them.
        The  user can modify this distance to better describe the point at which gases were samples,
        (which is usually the end point of the combustor).
        Parameters
        ----------
        path_to_sheet_or_df : path to file or df
        gas_to_add : select a gas of interest
        list_of_eq : optional list of equations to plot (if not included, will find all equations in file)
        multiplier : multiply all values by this constant
        filter_above : plot only the data above this value
        filter_below : plot only the data below this value
        colour : colour of bars
        X : X value frmo spreadsheet at which sensitivity should be measured
        offset : offset for bars in order to create a grouped plot. This should increase in increments of bar width (currently at 0.15)

        Returns None
        -------

        """
        #initialise the main dataframe:
        sens_df = pd.DataFrame()

        # check input for filepath or dataframe:
        if type(path_to_sheet_or_df) is pd.DataFrame:
            sens_df = path_to_sheet_or_df

        else:
            sens_df = pd.read_csv(path_to_sheet_or_df)

        # initalise x axis labels and x axis values:
        list_col_h = []
        col_val = []
        col_label = []
        # this is a list of all equations that must be considered for plotting:
        list_of_eq_local = list_of_eq

        # find 'gas + equation' (from equation list) in column headers and add to list_col_h the true column headers:
        if list_of_eq_local is not None:
            list_col_h = self.find_col_headers(sens_df, list_of_eq_local, gas_to_add)

        # plot gas match for all equations in df:
        else:
            full_eq_list_when_no_eq = []
            for s in sens_df.columns.values:
                try:
                    h = s.split('_')[2]
                    if '=' in h and h not in full_eq_list_when_no_eq:
                        full_eq_list_when_no_eq.append(s.split('_')[2])
                except IndexError:
                    print(s + ' not added to eq list because its not an equation')
            list_of_eq_local = full_eq_list_when_no_eq
            list_col_h = self.find_col_headers(sens_df, full_eq_list_when_no_eq, gas_to_add)

        if list_col_h is not None:
            col_val, col_label = self.find_col_values(sens_df, list_col_h, X, filter_above = filter_above, filter_below = filter_below)


            #if column does not exist in col label, assign value = 0 to it and add label:
            if filter_below is None and filter_above is None:
                for eq in list_of_eq_local:
                    if eq not in col_label:
                        col_label.append(eq)
                        col_val.append(0)

            col_val = [x * multiplier for x in col_val]

            if col_val:
                self.plot_bar(col_val, col_label, colour, gas_to_add, offset=offset)
            else:
                raise ValueError('Cannot find values')

    def plot_bar_lam_burning_v(self, path_to_sheet_or_df, list_of_eq=None, multiplier: float = 1, filter_above = None, filter_below= None,
                               colour: str = 'red', X: float = 0, offset: float = 0):
        """
        PLOT LAMINAR BURNING VELOCITY at distance X (default 0). Assume using Flowrate_sens columns frmo CHEMKIN spreadsheet.
        Parameters
        ----------
        path_to_sheet_or_df : path to file
        list_of_eq : if added, will only plot these chemical equations (otherwise will plot all equations available in spreadsheet).
        multiplier : multiply all sensitivity values by this constant
        filter_above : take all values above this one
        filter_below : take all values below this one
        colour : bar colour
        X : X distance
        offset : for bar graph spacing

        Returns None
        -------

        """
        # initialise the main dataframe:
        sens_df = pd.DataFrame()

        # check input for filepath or dataframe:
        if type(path_to_sheet_or_df) is pd.DataFrame:
            sens_df = path_to_sheet_or_df

        else:
            sens_df = pd.read_csv(path_to_sheet_or_df)

        # initalise x axis labels and x axis values:
        list_col_h = []
        col_val = []
        col_label = []
        list_of_eq_local = list_of_eq

        if list_of_eq is not None:
            list_col_h = self.find_col_headers(sens_df, list_of_eq)

        # plot gas match for all equations in df:
        else:
            full_eq_list_when_no_eq = []
            for s in sens_df.columns.values:
                try:
                    h = s.split('_')[2]
                    if '=' in h and h not in full_eq_list_when_no_eq:
                        full_eq_list_when_no_eq.append(s.split('_')[2])
                except IndexError:
                    print(s + ' not added to eq list because its not an equation')
            list_of_eq_local = full_eq_list_when_no_eq
            list_col_h = self.find_col_headers(sens_df, full_eq_list_when_no_eq)

        # find 'gas + equation' (from equation list) in column headers and add to list_col_h the true column headers:
        if list_col_h is not None:
            col_val, col_label = self.find_col_values(sens_df, list_col_h, X, 3, filter_above = filter_above, filter_below = filter_below)

            #if column does not exist in col label, assign value = 0 to it and add label:
            if filter_below is None and filter_above is None:
                for eq in list_of_eq_local:
                    if eq not in col_label:
                        col_label.append(eq)
                        col_val.append(0)

            col_val =  [x * multiplier for x in col_val]
            if col_val:
                self.plot_bar(col_val, col_label, colour, offset=offset)
            else:
                raise ValueError('Cannot find values')


    def show_and_save(self, path_of_save_folder: str, name: str):
        """

        Parameters
        ----------
        path_of_save_folder : where to save
        name : name under which picture should be saved

        Returns None
        -------

        """
        full_path = os.path.join(path_of_save_folder, name)
        plt.savefig(full_path, dpi=300, bbox_inches="tight")
        plt.close(self.fig)
