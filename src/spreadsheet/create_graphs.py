import matplotlib.pyplot as plt
import os
import pandas as pd

# set a global style for all graphs:
plt.style.use('seaborn-notebook')

class Graph():
    def __init__(self, list_of_eq: str, title: str, x_axis_label: str = 'Sensitivity', x_graph_size: int = 6,
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
        self.y_axis_label = list_of_eq
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
        plt.ylabel(self.y_axis_label, figure=self.fig)

    def plot_bar(self, name_of_folder_n_sheet:str, gas_to_add:str, legend:str, multiplier:float = 1, colour:str = 'red'):
        # convert data into df:
        list_val = []
        full_path = os.path.join('./data/', name_of_folder_n_sheet)
        sens_df = pd.read_csv(full_path)

        for eq in self.list_of_eq:
            column_header = gas_to_add + '_Sens_' + eq
            res = list(filter(lambda x: column_header in x, sens_df.columns.values))
            list_val.append(tuple(res, eq))

    def show_and_save(self, path_of_save_folder: str, name: str):
        """
        shows and saves the figure - must be called to show the figure at the end of plotting
        :param self:
        :param path_of_save_folder: save figures to this folder
        :param name: save figures under this name
        :return:
        """
        full_path = os.path.join(path_of_save_folder, name)
        plt.savefig(full_path, dpi=300, bbox_inches = "tight")
        plt.close(self.fig)
