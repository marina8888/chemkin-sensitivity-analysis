from spreadsheet import create_graphs, prepare_sheet

# SAMPLE SCRIPT BELOW:

def main():

    # prepare a new dataframes from prepare_sheet functions:

    df2 = prepare_sheet.join_files('data/okafor_stag_60%_1.15')
    df2 = prepare_sheet.remove_spaces(df2)

    print(df2['Distance_(cm)'])
    # Create a new graph:
    graph = create_graphs.Graph('20% Heat Ratio, 1.0 Equivalence Ratio', 'x axis')

    # create species plot where eq = the x axis equations used for this plot:
    # eq = graph.plot_bar_species(df3, 'OH', X = 0.02, offset = 0.3, filter_below=-0.01, filter_above=0.01, sorting=True)

    #Add laminar burning velocity plot spreadsheet, using equations extracted from the previous plot:
    eq = graph.plot_bar_species(df2, 'C', X=0.02, filter_above=0.001, filter_below=-0.001, offset = 0.15, colour = 'g')
    graph.plot_bar_species(df2, 'H2O2', list_of_eq=eq, X=0.02, colour = 'r')

    # #Save graphs to ./output/graphs folder (which user may need to create) under the name test.png:
    graph.show_and_save('./output/graphs', 'test3')



if __name__ == "__main__":
    main()
