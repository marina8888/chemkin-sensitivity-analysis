from spreadsheet import create_graphs, prepare_sheet

# SAMPLE SCRIPT BELOW:

def main():

    # prepare a new dataframes from prepare_sheet functions:

    df2 = prepare_sheet.join_files('data/60%_0.85')
    df2 = prepare_sheet.remove_spaces(df2)

    # df = prepare_sheet.remove_spaces('data/okafor_laminar/40%_0.85.csv')

    # Create a new graph:
    graph = create_graphs.Graph('60% Heat Ratio, 0.85 Equivalence Ratio')

    # create species plot where eq = the x axis equations used for this plot:
    eq = graph.plot_bar_species(df2, 'NO', X = 2.0, offset = 1, filter_below=-0.03, filter_above=0.03, sorting=False)

    #Add laminar burning velocity plot spreadsheet, using equations extracted from the previous plot:
    # graph.plot_bar_species(df2, 'NH3', list_of_eq=eq, X=2.0, offset = 1, colour = 'orange', multiplier=0.5, legend = 'Sensitivity for NH3 x 0.5')
    graph.plot_bar_lam_burning_v('data/okafor_laminar/60%_0.85.csv', list_of_eq=eq, X=0, colour = 'r', multiplier=1.5, legend = 'Laminar burning velocity x 1.5', sorting = True)

    # #Save graphs to ./output/graphs folder (which user may need to create) under the name test.png:
    graph.show_and_save('./output/graphs', 'test3.png')

if __name__ == "__main__":
    main()
