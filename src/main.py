from spreadsheet import convert_rop_col, create_graphs

def main():
    marina = create_graphs.Graph('title', ['H+O2+H2O<=>HO2+H2O', 'H+O2<=>O+OH'])
    marina.plot_bar_species('okafor_sens/Okafor_0.85_0.4sens.csv', 'H2O', 'legend', all_eq_list= True)
    marina.show_and_save('./output/graphs', 'test')

# ['H+O2+H2O<=>HO2+H2O', 'H+O2<=>O+OH']
if __name__ == "__main__":
    main()
