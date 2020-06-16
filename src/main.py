from spreadsheet import convert_rop_col, create_graphs

def main():
    marina = create_graphs.Graph(['H+O2+H2O<=>HO2+H2O', 'H+O2<=>O+OH'], 'title')
    marina.plot_bar_species('okafor_sens/Okafor_0.85_0.4sens.csv', 'H2O', 'legend')
    marina.show_and_save('./output/graphs', 'test')

if __name__ == "__main__":
    main()
