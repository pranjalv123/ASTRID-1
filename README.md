# ASTRID
Accurate Species TRee Reconstruction with Internode Distances

For more information, see http://pranjalv123.github.io/ASTRID/

# Usage

        ASTRID.py [-h] -i INPUT -o OUTPUT [-m METHOD] [-c CACHE]

ASTRID: Accurate Species TRees from Internode Distances.

optional arguments:

  -h, --help            show this help message and exit
  
  -i INPUT, --input INPUT:
                        File containing gene trees as newick strings
                        
  -o OUTPUT, --output OUTPUT:
                        Output file for species tree
                        
  -m METHOD, --method METHOD:
                        Distance-based method to use (default: fastme if the
                        distance matrix is complete, bionj otherwise
                        
  -c CACHE, --cache CACHE:
                        Save distance matrix in PHYLIP format, or use cached
                        matrix if it exists (useful for trying multiple
                        distance-based methods)
