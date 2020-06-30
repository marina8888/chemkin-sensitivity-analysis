from spreadsheet import create_graphs, prepare_sheet

# SAMPLE SCRIPT BELOW:

def main():

    # prepare a new dataframes from prepare_sheet functions:


    df2 = prepare_sheet.add_distance('test_files/h2.csv', 0.1)
    df2 = prepare_sheet.add_space(df2)

    # Create a new graph:
    graph = create_graphs.Graph('20% Heat Ratio, 1.0 Equivalence Ratio', 'x axis')

    # create species plot where eq = the x axis equations used for this plot:
    # eq = graph.plot_bar_species(df3, 'OH', X = 0.02, offset = 0.3, filter_below=-0.01, filter_above=0.01, sorting=True)

    #Add laminar burning velocity plot spreadsheet, using equations extracted from the previous plot:
    eq = graph.plot_bar_lam_burning_v(df2, X=0, offset = 0.15, colour = 'g')
    graph.plot_bar_lam_burning_v(df2, list_of_eq=eq, X=0, colour = 'r')

    # #Save graphs to ./output/graphs folder (which user may need to create) under the name test.png:
    graph.show_and_save('./output/graphs', 'test3')



if __name__ == "__main__":
    main()
