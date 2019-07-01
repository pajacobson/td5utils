# td5utils
Basic scripts for manipulating Land Rover Td5 engine maps.  

### map_split.py
Splits Nanocom .map file into component variant and fuel maps.

Fuel maps can be associated with more than variant map.  
To avoid potential confusion fuel map names include the variant name.

Requires Python 3.6 or higher due to use of f-string formating.

### bin_split.py
Splits NNN .bin and .ori files into component parts:   

- boot code
- variant map
- VIN block
- fuel map

The components are byte swapped to native byte order to facilitate programming using BDM or for use in .map files.
