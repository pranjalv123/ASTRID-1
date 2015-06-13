# ASTRID
Accurate Species TRee Reconstruction with Internode Distances

To use:

  python pynjst.py /path/to/gene/trees
  
and it will output the tree to the standard output.

Requires fnj installed, see http://fastphylo.sourceforge.net/

Algorithm described in Liu, L., & Yu, L. (2011). Estimating species trees from unrooted gene trees. Systematic Biology, 60(5), 661–667. doi:10.1093/sysbio/syr027

This is faster than the reference implementation and it works on incomplete gene trees.
