# PLEASE SEE https://github.com/pranjalv123/ASTRID-2 FOR THE MOST RECENT VERSION OF ASTRID!

# ASTRID 1.4

Download [HERE](https://github.com/pranjalv123/ASTRID/releases)

Accurate Species TRee Reconstruction with Internode Distances

For more information, see http://pranjalv123.github.io/ASTRID/

Join the ASTRID user group at https://groups.google.com/forum/#!forum/astrid-users/

# Installation (binary)

ASTRID is available for Linux, Mac OS X, and Windows. 

Download the appropriate binary file for your operating system at https://github.com/pranjalv123/ASTRID/releases

You may need to run

    chmod +x ASTRID-osx 

in order to be able to execute it.

Also, you can either do

    mv ASTRID-osx ASTRID
    
or use `ASTRID-osx` when `ASTRID` is specified in the documentation. (replacing ASTRID-osx with ASTRID-linux on linux) 

# Installation (source)

YOU DO NOT NEED TO DO ANY OF THIS TO RUN ASTRID - THIS IS PRIMARILY FOR ASTRID DEVELOPERS 

## Dependencies:
   - CMake (https://cmake.org/)
   - Boost (http://www.boost.org/)
   - DendroPy version 4 or greater https://pythonhosted.org/DendroPy/
   - A recent C++ compiler
   
Clone the repository and enter the directory.

      git clone git@github.com:pranjalv123/ASTRID.git
      cd ASTRID

Create a build folder

      mkdir build && cd build

Configure and build

      cmake ../src/
      make

Make will automatically download and compile FastME 2, and place all
necessary files in `build/bin/`.

## Packaging

Get PyInstaller (http://www.pyinstaller.org/), and run `pyinstaller
ASTRID.spec` from the repository root. This will produce the `dist`
folder and an `ASTRID` executable in it.

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
    
    
