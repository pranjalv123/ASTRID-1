import dendropy
import numpy as np
import sys
import subprocess

fnj_exec='fnj'

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
    
    lines = []

    
    for i in taxindices:
        vals = ' '.join([str(njmat[taxindices[i], taxindices[j]]) for j in taxindices])
        lines.append('     '.join([i.label, vals]))
    distmat = '\n'.join(lines)

    p = subprocess.Popen([fnj_exec, '-I', 'phylip'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.stdin.write(str(len(taxindices)))
    p.stdin.write('\n')
    p.stdin.write(distmat)
    p.stdin.close()
    tree = [i for i in p.stdout.readlines() if '<newick>' in i][0].strip().replace('<newick>', '').replace('</newick>', '')
    print tree
#    print njmat


if __name__ == '__main__':
    tl = dendropy.TreeList.get_from_path(sys.argv[1], 'newick')
    njst(tl)
