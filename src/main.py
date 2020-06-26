from spreadsheet import create_graphs, prepare_sheet

# SAMPLE SCRIPT BELOW:
def main():
    df = prepare_sheet.add_distance('data/okafor_stag_sens/okafor_stag_0.85_0.4.csv')
    # Create a new graph:
    fortyp_stoich = create_graphs.Graph('40% Heat Ratio, 0.85 Equivalence Ratio')

    #Add species plots for NO and NO2, with an offset create grouped bars, X distance defining chamber end and multiplier:
    # fortyp_stoich.plot_bar_species('data/okafor_stag_sens/okafor_stag_0.85_0.4.csv', 'NH3', X = 0.02, filter_below = -0.01, filter_above=0.01, offset=0.15)
    fortyp_stoich.plot_bar_species(df,'NO',  filter_below= -0.02, filter_above= 0.02, X = 0.02, colour = 'g', sorting= True)

    #Add laminar burning velocity plot using CHEMKIN generated export.csv spreadsheet:
    # fortyp_stoich.plot_bar_lam_burning_v('data/okafor_lam_sens/export.csv', filter_above = 0.02, filter_below=-0.02)

    #Save graphs to ./output/graphs folder (which user may need to create) under the name test.png:
    fortyp_stoich.show_and_save('./output/graphs', 'sort')

if __name__ == "__main__":
    main()
