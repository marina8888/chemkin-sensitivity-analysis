from spreadsheet import create_graphs, prepare_sheet

# SAMPLE SCRIPT BELOW:
def main():
    # prepare a new dataframe from prepare sheet functions:
    df = prepare_sheet.add_distance('data/okafor_stag_sens/okafor_stag_0.85_0.4.csv', 0.02)
    df_lam = prepare_sheet.add_distance('data/okafor_lam_sens/okafor_lam_0.85_0.4.csv', 0.02)
    # Create a new graph:
    fortyp_stoich = create_graphs.Graph('40% Heat Ratio, 0.85 Equivalence Ratio')

    #Add laminar burning velocity plot spreadsheet:
    fortyp_stoich.plot_bar_lam_burning_v(df_lam, filter_below=-0.005, filter_above=0.005, sorting = True)

    #Add species plots for NO and NO2, with an offset create grouped bars, X distance defining chamber end and sorting in descending order:
    # fortyp_stoich.plot_bar_species(df, 'NO',  filter_below= -0.02, filter_above= 0.02, X = 0.02, colour = 'g', sorting= True)


    #Save graphs to ./output/graphs folder (which user may need to create) under the name test.png:
    fortyp_stoich.show_and_save('./output/graphs', 'lam')

if __name__ == "__main__":
    main()
