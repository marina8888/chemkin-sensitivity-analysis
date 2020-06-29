from spreadsheet import create_graphs, prepare_sheet

# SAMPLE SCRIPT BELOW:

def main():

    # prepare a new dataframes from prepare_sheet functions:
    df = prepare_sheet.add_distance('test_files/h1.csv', 0.1)
    df = prepare_sheet.add_space(df)
    df2 = prepare_sheet.add_distance('test_files/h2.csv', 0.1)
    df2 = prepare_sheet.add_space(df2)
    df3 = prepare_sheet.add_distance('test_files/stag.csv', 0.1)

    # Create a new graph:
    graph = create_graphs.Graph('20% Heat Ratio, 1.0 Equivalence Ratio')

    # # Add NO plot with an offset create grouped bars, X distance defining chamber end and sorting in descending order.

    # #Add laminar burning velocity plot spreadsheet, using equations filtered in the previous plot:
    eq = graph.plot_bar_lam_burning_v(df, X=0, filter_below=-0.01, filter_above=0.01, colour = 'g', sorting=True, offset = 0.15)
    graph.plot_bar_lam_burning_v(df2, list_of_eq=eq, X=0, filter_below=-0.01, filter_above=0.01, colour = 'r')
    graph.plot_bar_species(df3, 'NH3', list_of_eq = eq, X = 0.02, offset = 0.3, multiplier = 0.5)

    # #Save graphs to ./output/graphs folder (which user may need to create) under the name test.png:
    graph.show_and_save('./output/graphs', 'test3')



if __name__ == "__main__":
    main()
