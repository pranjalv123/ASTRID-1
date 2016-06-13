# ASTRID tutorial

ASTRID is a fast, highly scalable species tree estimation program that
is statistically consistent under the multi-species coalescent
model.

# Installing ASTRID

Download the appropriate binary for your system:

* [Mac OS X]()
* [Linux]()

Alternatively, clone the GitHub repository and build as described in
README.md.

To test if ASTRID works on your system, open a terminal window. On a
Mac, you can open the "Terminal" app in your Applications folder. Use
`cd` to go to the folder that contains ASTRID, then run

     ./ASTRID

You should see something that looks like

    usage: ASTRID [-h] -i INPUT [-b --bsfile BSFILE]
              [--bslist BSLIST [BSLIST ...]] [-r --bsreps BSREPS] [-o OUTPUT]
              [-m METHOD] [-c CACHE] [--taxon-cutoff TAXON_CUTOFF]
    ASTRID: error: argument -i/--input is required

To see the online help for ASTRID, you can run `./ASTRID -h`; you
should see

     usage: ASTRID [-h] -i INPUT [-b --bsfile BSFILE]
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

# Tutorial files

For this tutorial, please download the test data available at ().

# Running ASTRID

The simplest way to run ASTRID is:

    ./ASTRID -i <input file> 

We will run this on a dataset based on the [Song et
al.](http://www.pnas.org/content/109/37/14942.short) dataset with 37
mammalian species and 447 genes. 21 mislabeled genes and 2 outliers
have been removed, and gene trees were estimated with RAxML.

Try this now.

    ./ASTRID -i test/song_mammals.424.gene.tre

ASTRID will output some information as it is running, and then will
output the tree:

       {'cache': None, 'bsreps': 100, 'bsfile': None, 'output': None, 'input': 'song_mammals.424.gene.tre', 'bslist': None, 'taxon_cutoff': 0, 'method': 'auto'}
       generating matrix
       0.0776200294495 seconds
       inferring tree

	. This analysis will run on 4 threads.

       #  Analysing dataset 1

	. Computing tree...

	. Performing NNI...

	. Time used 0h00m00s
       0.0068039894104 seconds
       ASTRID tree:
       (((((Armadillos,Sloth),((Elephant,Hyrax),Lsr_Hdghg_Tnrc)),(((Shrew,Hedgehog),((((Dog,Cat),Horse),((Pig,(Cow,Dolphin)),Alpaca)),(Megabat,Microbat))),(((((((Mouse,Rat),Kangaroo_Rat),Guinea_Pig),Squirrel),(Rabbit,Pika)),Tree_Shrew),((Mouse_Lemur,Galagos),(((Macaque,(Orangutan,((Chimpanzee,Human),Gorilla))),Marmoset),Tarsier))))),(Platypus,Chicken)),Opossum,Wallaby);


The last line of this is the output; we can save this to a file by
running

    ./ASTRID -i test/song_mammals.424.gene.tre -o test/astrid_mammalian_tree

# Viewing the tree

Let's take a look at both the input and output. The input consists of
447 newick trees; these may contain polytomies and be rooted or
unrooted. The output is an arbitrarily rooted newick tree without
branch lengths or support values.

We can visualize the tree at
http://www.evolgenius.info/evolview/. Upload the tree and root it by
hovering over the "Chicken" branch and pressing "Reroot Here".

# Calculating branch support with MLBS

Multi-locus bootstrapping lets us estimate bootstrap support on edges
of our estimated tree. We calculate bootstrap replicates on each gene,
and estimate species trees for each set of bootstrap
replicates. Currently ASTRID supports site-only resampling ([Seo,
2008]()). We have supplied 100 bootstrap replicates for each of the
mammalian genes in the `424genes` folder. To get a list of all the
bootstrap files, run

	  find test/424genes -name *allbs > bslist

This will create a file called `bslist` with paths to all the
bootstrap gene trees. To get the ASTRID tree with bootstrap support,
run

	./ASTRID -b bs-files -i test/song_mammals.424.gene.tre -o test/astrid_mammalian_tree

This will run 100 bootstrap replicates and output two trees. The first
is a majority consensus tree of the replicates with branch support,
and the second 

This creates two files, `test/astrid_mammalian_tree.bs_tree`, which is
the ASTRID tree on the input data with branch support, and
`test/astrid_mammalian_tree.bs_consensus`, which is a majority
consensus tree of the bootstrap replicates with branch support.

Note that these two trees are different! The ASTRID tree puts tree
shrews with rodents with 47% support, while the majority consensus
tree puts tree shrews with primates with 53% support.

# Calculating branch support and branch lengths with ASTRAL

For this part of the tutorial you will need ASTRAL
(https://github.com/smirarab/ASTRAL/). 

Instead of using MLBS to calculate branch support, we can use ASTRAL
to annotate our trees with branch support and edge lengths based on
quartet frequencies in the input gene trees (see
(here)[http://mbe.oxfordjournals.org/content/early/2016/05/12/molbev.msw079.full]
for more info).

This is quite straightforward - we get our mammalian tree as before

     ./ASTRID -i test/song_mammals.424.gene.tre -o  test/astrid_mammalian_tree

Then we run ASTRAL as follows (substituting in whatever version of
ASTRAL you have):

     java -jar astral.4.10.2.jar -i test/song_mammals.424.gene.tre -q test/astrid_mammalian_tree -o annotated_mammalian_tree

Now we can visualize this, and we see that support values here are
substantially higher than in the MLBS case, with 91% support for the
placement of tree shrews. We also get edge lengths, which we do not
get from the MLBS process. 

# Running ASTRID on sparse datasets

ASTRID will run on datasets where the input gene trees are missing
taxa. If there is a pair of taxa that never occur in the same tree,
though, there will be a misisng entry in the distance matrix. In this
case, we need to use
(PhyD*)[http://www.atgc-montpellier.fr/phyd/binaries.php] instead of
FastME to estimate the tree. 

We will use a seabirds supertree dataset, from (). This dataset has 7
source trees and 121 taxa. If we run

       ASTRID -i seabirds.source_trees

we will see in the output

   Distance matrix has 5092 missing entries (out of  14641 )
   This may result in an inaccurate tree
   Using BioNJ*

Over a third of the entries in the distance matrix are unknown, so
it's not surprising that we might not get good results here. However,
if we have even a single source tree on all the taxa, ASTRID is likely
to give good results.

