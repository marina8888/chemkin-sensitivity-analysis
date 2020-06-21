# chemkin-sensitivity-analysis

## src/spreadsheet/create_graphs:
Uses matplotlib library to plot sensitivity data as bar charts. Sensitivity data must be generated using CHEMKIN postprocessing GUI.

### Sample code: 
```
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
```

### Example graph: 
[Sample code graph](src/output/graphs/test.png)


## src/spreadsheet/convert_rop_col:
WARNING - THIS SCRIPT IS HERE FOR REFERENCE ONLY. PLEASE PRE-PROCESS CHEMKIN CHEMISTRY IN THE GUI GENERATE WELL-FORMATED COLUMN HEADERS INSTEAD OF USING THIS SCRIPT. 

This script finds csv file column headers named in the format: `<GAS>_ROP_GasRxn#<number> (mole/cm3-sec)`, where <GAS> is the sensitivity of a considered gas, ROP stands for rate of production, and <number> is a reaction number from a mechanism. 
  It proceeds to rename the column headers with the relevant equations from the mechanisms, e.g: 
  `CH4_ROP_H+HCO(+M)<=>CH2O(+M)`
