from spreadsheet import create_graphs, prepare_sheet

# SAMPLE SCRIPT BELOW:

def main():

    # prepare a new dataframes from prepare_sheet functions:
    df = prepare_sheet.add_distance('data/okafor_stag_sens/okafor_stag_0.85_0.4.csv', 0.02)
    df_lam = prepare_sheet.add_distance('data/okafor_lam_sens/okafor_lam_0.85_0.4.csv', 0.02)

    # Create a new graph:
    graph = create_graphs.Graph('40% Heat Ratio, 0.85 Equivalence Ratio')

    # Add NO plot with an offset create grouped bars, X distance defining chamber end and sorting in descending order.
    # The plot functions return the equations used in this plot:
    NO_equations = graph.plot_bar_species(df, 'NO', X = 0.02, colour = 'g', filter_above=0.03, filter_below=-0.03, offset = 0.15, sorting = True)

    #Add laminar burning velocity plot spreadsheet, using equations filtered in the previous plot:
    graph.plot_bar_species(df, 'NH3', list_of_eq = NO_equations, X = 0.02, multiplier=0.5)
    graph.plot_bar_lam_burning_v(df_lam, list_of_eq = NO_equations, X = 0,  offset = -0.15)

    #Save graphs to ./output/graphs folder (which user may need to create) under the name test.png:
    graph.show_and_save('./output/graphs', 'me')

if __name__ == "__main__":
    main()
