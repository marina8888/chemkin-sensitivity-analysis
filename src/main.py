from spreadsheet import create_graphs

def main():
    # Create a new graph:
    marina = create_graphs.Graph('Add My Title Here')

    #Add laminar burning velocity plot using CHEMKIN generated export.csv spreadsheet:
    marina.plot_bar_lam_burning_v('okafor_lam_sens/export.csv', ['NH2+O<=>NH+OH', 'NH2+NO<=>NNH+OH','H+NO+M<=>HNO+M', 'HNO+H<=>H2+NO', 'H+O2<=>O+OH'])

    #Add species plots for NO and NO2, with an offset create grouped bars:
    marina.plot_bar_species('./okafor_sens/Okafor_0.85_0.4sens.csv', 'NO', ['NH2+O<=>NH+OH', 'NH2+NO<=>NNH+OH','H+NO+M<=>HNO+M', 'HNO+H<=>H2+NO', 'H+O2<=>O+OH'], offset=0.15)
    marina.plot_bar_species('./okafor_sens/Okafor_0.85_0.4sens.csv', 'NO2', ['NH2+O<=>NH+OH', 'NH2+NO<=>NNH+OH','H+NO+M<=>HNO+M', 'HNO+H<=>H2+NO', 'H+O2<=>O+OH'], colour = 'g', offset=0.3)

    #Save graphs to ./output/graphs folder (which user may need to create) under the name test.png:
    marina.show_and_save('./output/graphs', 'test')

if __name__ == "__main__":
    main()
