# ASTRID
Accurate Species TRee Reconstruction with Internode Distances

For more information, see http://pranjalv123.github.io/ASTRID/

Join the ASTRID user group at https://groups.google.com/forum/#!forum/astrid-users/

# Installation

To install the most recent stable version of ASTRID, run (as root)

      pip install astrid-phylo
      
or, to install the development version from Git, run

      pip install git+https://github.com/pranjalv123/ASTRID/

(you should have installed setuptools, numpy, dendropy, and a C++ compiler)

You can also install the most recent version from github by cloning the repository, then running (as root)

      python setup.py install 
      
To install locally (for example, if you're running on a server where you don't have root access), you can do

      pip install astrid-phylo --user
      
or 

      python setup.py install --user
      

# Usage
ASTRID [-h] -i INPUT [-b --bsfile BSFILE]
              [--bslist BSLIST [BSLIST ...]] [-r --bsreps BSREPS] [-o OUTPUT]
              [-m METHOD] [-c CACHE] [--taxon-cutoff TAXON_CUTOFF]

ASTRID: Accurate Species TRees from Internode Distances.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        File containing gene trees as newick strings
  -b --bsfile BSFILE    File containing a list of bootstrap replicate files,
                        one file per gene
  --bslist BSLIST [BSLIST ...]
                        List of bootstrap files
  -r --bsreps BSREPS    Number of bootstrap replicates
  -o OUTPUT, --output OUTPUT
                        Output file for species tree
  -m METHOD, --method METHOD
                        Distance-based method to use (default: fastme if the
                        distance matrix is complete, bionj otherwise
  -c CACHE, --cache CACHE
                        Save distance matrix in PHYLIP format, or use cached
                        matrix if it exists (useful for trying multiple
                        distance-based methods)
  --taxon-cutoff TAXON_CUTOFF
                        Only take trees with at least this many taxa

ASTRID is also easy to use from within Python:

    import dendropy
    import ASTRID
    tl = dendropy.TreeList.get_from_path('test/song_mammals.424.gene.tre', 'newick')
    a = ASTRID.ASTRID(tl)
    a.run('auto')
    print str(a.tree)
    
    
