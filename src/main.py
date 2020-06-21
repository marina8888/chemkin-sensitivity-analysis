from spreadsheet import convert_rop_col, create_graphs

def main():
    marina = create_graphs.Graph('title')
    # marina.plot_bar_lam_burning_v('okafor_lam_sens/export.csv', ['H+C2H4(+M)<=>C2H5(+M)', 'OH+CH3(+M)<=>CH3OH(+M)', 'OH+CO<=>H+CO2'])
    marina.plot_bar_species('./okafor_sens/Okafor_0.85_0.4sens.csv', ['H+C2H4(+M)<=>C2H5(+M)', 'OH+CH3(+M)<=>CH3OH(+M)', 'OH+CO<=>H+CO2'])
    marina.show_and_save('./output/graphs', 'test')

# ['H+O2+H2O<=>HO2+H2O', 'H+O2<=>O+OH']
if __name__ == "__main__":
    main()
