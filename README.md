# chemkin-sensitivity-analysis
  
## src/spreadsheet/convert_rop_col:

This script finds csv file column headers named in the format: `<GAS>_ROP_GasRxn#<number> (mole/cm3-sec)`, where <GAS> is the sensitivity of a considered gas, ROP stands for rate of production, and <number> is a reaction number from a mechanism. 
  It proceeds to rename the column headers with the relevant equations from the mechanisms, e.g: 
  `CH4_ROP_H+HCO(+M)<=>CH2O(+M)`

## src/spreadsheet/create_graphs:
Uses matplotlib library to plot sensitivity data as bar charts.
