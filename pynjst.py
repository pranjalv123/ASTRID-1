from dendropy.interop import paup
import dendropy
import numpy as np
import sys

def nj(m):
    q = np.zeros(m.shape)
    n = m.shape[0]
    q = (n - 2)

def njst(tl):
    taxindices = dict([(j, i) for i, j in enumerate(tl.taxon_set)])
    countmat = np.zeros((len(tl.taxon_set), len(tl.taxon_set)))
    njmat = np.zeros((len(tl.taxon_set), len(tl.taxon_set)))
    for t in tl:
        for e in t.get_edge_set():
            e.length=1
        m = dendropy.treecalc.PatristicDistanceMatrix(t)
        for x in t.leaf_nodes():
            xi = taxindices[x.taxon]
            for y in t.leaf_nodes():
                yi = taxindices[y.taxon]
                countmat[xi, yi] += 1
                njmat[xi, yi] += m(x.taxon, y.taxon)
    njmat /= countmat
    print len(taxindices)
    for i in taxindices:
        print i, '     ',
        for j in taxindices:
            print njmat[taxindices[i], taxindices[j]],
        print
#    print njmat


if __name__ == '__main__':
    tl = dendropy.TreeList.get_from_path(sys.argv[1], 'newick')
    njst(tl)
