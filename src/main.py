from spreadsheet import convert_rop_col, create_graphs

def main():
    marina = create_graphs.Graph('title', 'list of eq')
    marina.plot_bar('okafor_sens/Okafor_0.85_0.4sens.csv', 'NO', 'legend')
    marina.show_and_save('./output/graphs', 'test')

if __name__ == "__main__":
    main()
