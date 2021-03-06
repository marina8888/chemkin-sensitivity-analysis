import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np

# set a global style for all graphs:
plt.style.use('seaborn-notebook')


class Graph():
    def __init__(self, title: object, x_axis_label: object = 'Sensitivity', x_graph_size: object = 6,
                 y_graph_size: object = 6.5) -> object:
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

    @staticmethod
    def find_col_headers(df, eq_list=None, gas=None):
        """
        find 'gas + equation' (from equation list) in column headers and add to list_val the true column headers:

        Parameters
        ----------
        df : dataframe of all data
        eq_list : equations list (if user has selected equations, otherwise all will be extracted from df
        gas : gas of interest (if selected by user, otherwise assume laminar burning velocity is being extracted)

        Returns (filtered_eqs, inital_eqs) : A the startswith string (or sometimes full string) for col headers and a list of equations
        -------

        """
        filtered_eqs = []

        if gas is not None:
            i = 2
        else:
            i = 3

        # call this for species sensitivity with eq:
        if gas is not None and eq_list is not None:
            for eq in eq_list:
                column_header = gas + '_Sens_' + eq
                filtered_eqs += (list(filter(lambda x: column_header in x, df.columns.values)))

            filtered_eqs = [f for f in filtered_eqs if f.startswith(gas + '_')]
            inital_eqs = eq_list

        # call this for laminar burning velocity sensitivity with eq:
        elif gas is None and eq_list is not None:
            for eq in eq_list:
                column_header = 'Flow_rate_Sens_' + eq
                filtered_eqs += list(filter(lambda x: column_header in x, df.columns.values))
            inital_eqs = eq_list

        # find all the equations in the sheet:
        elif eq_list is None:
            for s in df.columns.values:
                try:
                    h = s.split('_')[i]
                    if '=' in h and h not in filtered_eqs:
                        filtered_eqs.append(s.split('_')[i])
                except IndexError:
                    print(s + ' not added to eq list because its not an equation')
            inital_eqs = filtered_eqs

            if gas is not None:
                string_to_add = gas + '_Sens_'
                filtered_eqs = list(map(string_to_add.__add__, filtered_eqs))
            elif gas is None:
                filtered_eqs = list(map('Flow_rate_Sens_'.__add__, filtered_eqs))

        if not filtered_eqs:
            print('No values for equations that contain the gas provided!')
            return None
        else:
            return (filtered_eqs, inital_eqs)

    @staticmethod
    def find_col_values(df, list, Xcm_val, gas, filter_above=None, filter_below=None):
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
        if gas is not None:
            i = 2
        else:
            i = 3
        d_name = []
        d_val = []

        mask1 = df['Distance_(cm)'] == Xcm_val
        data_df = df[mask1].copy(deep=True)
        if data_df.empty:
            raise ValueError('cannot find X value!')
        # add filter condition to df:
        if filter_above is not None and filter_below is not None:
            data_df1 = data_df.loc[:, (data_df > filter_above).any()].copy(deep=True)
            data_df2 = data_df.loc[:, (data_df < filter_below).any()].copy(deep=True)
            data_df = data_df1.join([data_df2])

        elif filter_above is not None:
            print("filtering above")
            data_df = data_df.loc[:, (data_df > filter_above).any()].copy(deep=True)

        elif filter_below is not None:
            print("filtering below")
            data_df = data_df.loc[:, (data_df < filter_below).any()].copy(deep=True)

        # filter and take relevant values from dataframe and add to list. Extract all values as a list of lists
        for l in list:
            for s in data_df.columns.values:
                if s.startswith(l):
                    d = pd.Series(data_df[s])
                    if d.name.split('_')[i] not in d_name:
                        d_name.append(d.name.split('_')[i])
                        try:
                            d_val.append(d.values[0])
                        except IndexError:
                            d_val.append(0)
                            print("ERROR: No value was found. Please check the X distance is specified correctly. ")
                    else:
                        print('ERROR : duplicate equation found and removed -> ' + s)

        return d_val, d_name

    def plot_bar(self, col_val, col_label, colour, gas_to_add=None, offset=0, sorting=False, list_of_eq=None,
                 legend=None):
        """
        Simple bar graph plot including setting ticks and correct axis locations.
        """
        col_val_loc = col_val
        col_label_loc = col_label
        if col_val is not None:

            if sorting is False and list_of_eq is None:
                # sort in order for x labels to match:
                col_label_loc, col_val_loc = zip(*sorted(zip(col_label, col_val)))

            elif sorting is False and list_of_eq is not None:
                slt = sorted(zip(col_label, col_val), key=lambda t: list_of_eq.index(t[0]))
                col_label_loc, col_val_loc = zip(*slt)

            elif sorting is True:
                l = sorted(zip(col_label, col_val), key=lambda x: x[1])
                col_label_loc, col_val_loc = zip(*l)

            bar_width = 0.15
            ind = np.arange(len(col_label_loc))

            if gas_to_add is None:
                self.ax.barh(ind + (offset * bar_width), col_val_loc, bar_width,
                             label='Sensitivity for laminar' + '\n' + '   burning velocity' if legend == None else legend,
                             align='edge',
                             tick_label=col_label_loc, zorder=10, color=colour)

            else:
                self.ax.barh(ind + (offset * bar_width), col_val_loc, bar_width,
                             label='Sensitivity for ' + gas_to_add if legend == None else legend, align='edge',
                             tick_label=col_label_loc, zorder=10, color=colour)
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

            self.ax.legend(bbox_to_anchor=(0.3, 0.3))
            return col_label_loc, col_val_loc

    def plot_sensitivity(self, path_to_sheet_or_df, gas_to_add: str = None, list_of_eq: list = None, multiplier: float = 1,
                         filter_above=None, filter_below=None, legend=None,
                         colour: str = 'b', X: float = 0.02, offset: float = 0, sorting=False, do_not_plot=False):

        """
        For REACTION SENSITIVITY plot: takes values from a spreadsheet at default distance X = 0.02 and plots them.
        For LAMINAR BURNING VELOCITY plot: takes values at distance X (default 0). Assume using Flowrate_sens columns from a CHEMKIN spreadsheet.

        The  user can modify this distance to better describe the point at which gases were samples, (which is usually the end point or inlet of the combustor).

        Parameters
        ----------
        path_to_sheet_or_df : path to file or df
        gas_to_add : select a gas of interest
        list_of_eq : optional list of equations to plot (if not included, will find all equations in file)
        multiplier : multiply all values by this constant
        filter_above : plot only the data above this value
        filter_below : plot only the data below this value
        colour : colour of bars
        X : X value from spreadsheet at which sensitivity should be measured
        offset : offset for bars in order to create a grouped plot. This should increase in increments of bar width (currently at 0.15)
        sorting : if True, sorts the data in order for plotting
        legend: custom legend added by user
        Returns equations used in plot (in correct order)
        -------

        """

        # check input for filepath or dataframe:
        if isinstance(path_to_sheet_or_df, pd.DataFrame):
            sens_df = path_to_sheet_or_df

        else:
            sens_df = pd.read_csv(path_to_sheet_or_df)

        # initalise x axis labels and x axis values:
        list_col_h = []
        col_val = []
        col_label = []

        (list_col_h, equation_list) = self.find_col_headers(sens_df, list_of_eq, gas_to_add)

        # find 'gas + equation' (from equation list) in column headers and add to list_col_h the true column headers:
        if list_col_h is not None:
            col_val, col_label = self.find_col_values(sens_df, list_col_h, Xcm_val=X, gas = gas_to_add, filter_above=filter_above,
                                                      filter_below=filter_below)

            # if column does not exist in col label, assign value = 0 to it and add label:
            if filter_below is None and filter_above is None:
                for eq in equation_list:
                    if eq not in col_label:
                        col_label.append(eq)
                        col_val.append(0)

            col_val = [x * multiplier for x in col_val]
            if col_val and do_not_plot is False:
                col_label, col_val = self.plot_bar(col_val, col_label, colour, gas_to_add=gas_to_add, offset=offset,
                                                   sorting=sorting, list_of_eq=list_of_eq, legend=legend)
            elif do_not_plot is True:
                print("DO NOT PLOT->TRUE : Returning an equation but not plotting it on a graph!")
            else:
                raise ValueError('Cannot find values')

        return col_label

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
