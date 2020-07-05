from spreadsheet import create_graphs, prepare_sheet

# SAMPLE SCRIPT BELOW:

def main():

    # prepare a new dataframes from prepare_sheet functions:

    df2 = prepare_sheet.join_files('data/40%_0.85')
    df2 = prepare_sheet.remove_spaces(df2)

    # Create a new graph:
    graph = create_graphs.Graph('40% Heat Ratio, 0.85 Equivalence Ratio')

    # Find list of equations (eq) within the filter boundaries for species sensitivity NO, by using 'do_not_plot':
    eq = graph.plot_sensitivity(df2, 'NO', X = 2.0, filter_below=-0.03, filter_above=0.03, sorting=True, do_not_plot=True)

    # Add laminar burning velocity plot spreadsheet, using previously extracted equations, and sort them in order (ALWAYS SORT FIRST PLOT and return sorted equations):
    eq = graph.plot_sensitivity('data/okafor_laminar/40%_0.85.csv', list_of_eq=eq, offset=1, X=0, colour ='r', multiplier=1.5, legend ='Laminar burning velocity x 1.5', sorting = True)

    # Plot 'NO' species for the same list of equations:
    graph.plot_sensitivity(df2, 'NO', list_of_eq=eq, X=2.0, colour ='blue')

    #Save graphs to ./output/graphs folder (which user may need to create) under the name test.png:
    graph.show_and_save('./output/graphs', 'test.png')

if __name__ == "__main__":
    main()
