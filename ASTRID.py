import dendropy
import numpy as np
import sys
import subprocess
import tempfile
import os
from numpy import ma
import time
from PatristicDistanceMatrix import PatristicDistanceMatrix_np

nj_exec='phydstar'


def phydstar(nj, fname):
    p = subprocess.Popen(['bash', nj_exec, '-d', nj, '-i', fname])
    p.wait()
    tree = open(fname + '_' + nj.lower() + '.t').read()
    return tree

def bionj(fname):
    return phydstar('BioNJ', fname)
def mvr(fname):
    return phydstar('MVR', fname)
def nj(fname):
    return phydstar('NJ', fname)
def unj(fname):
    return phydstar('UNJ', fname)
def fastme(fname):
    print fname + '_fastme.t'
    p = subprocess.Popen(['fastme', '-i', fname, '-o', fname + '_fastme.t'])
    p.wait()
    tree = open(fname + '_fastme.t').read()
    return tree    
def ninja(fname):
    print open(fname).read()
    p = subprocess.Popen(['ninja', '--in_type', 'd', fname], stdout=subprocess.PIPE)
    tree = p.stdout.read()
    return tree

def njst(tl, method, fname = None):
    if fname:
        try: 
            if len(open(fname).read()):
                start = time.time()
                tree = method(fname)
                print "Time to generate tree", time.time() - start, fname
                return tree
        except IOError:
            pass


    start = time.time()
    tl = dendropy.TreeList.get_from_path(tl, 'newick')
    print "Time to read trees: ", time.time() - start, len(tl), len(tl.taxon_set)

        
    start = time.time()
    taxindices = dict([(j, i) for i, j in enumerate(sorted(list(tl.taxon_set)))])
    countmat = np.eye(len(tl.taxon_set))
    njmat = np.zeros((len(tl.taxon_set), len(tl.taxon_set)))
    for t in tl:
        for e in t.edges():
            e.length=1
        m = PatristicDistanceMatrix_np(t, taxindices).distmat()
        countmat += (m > 0)
        njmat += m

    njmat = ma.array(njmat, mask = (countmat == 0))
    countmat = ma.array(countmat, mask = (countmat == 0))

    njmat /= countmat
    print "Time to construct matrix", time.time() - start, len(tl), len(tl.taxon_set)
    lines = []
    start = time.time()

    staxkeys = sorted(taxindices.keys())
    
    for i in staxkeys:
        vals = ' '.join(["%.3f" % (njmat[taxindices[i], taxindices[j]]) for j in staxkeys])
        lines.append('     '.join([i.label, vals]))
    distmat = '\n'.join([i.replace('--' ,'-99.0') for i in lines])
    tmp = None
    if fname == None:
        tmpfd, fname = tempfile.mkstemp()
        tmp = os.fdopen(tmpfd, 'w')
    tmp = open(fname, 'w')
    tmp.write(str(len(taxindices)))
    tmp.write('\n')
    tmp.write(distmat)
    tmp.write('\n')
    tmp.close()    
    print "Time to write matrix", time.time() - start, len(tl), len(tl.taxon_set)

    start = time.time()
    
    tree = method(fname)
    print "Time to generate tree", time.time() - start, len(tl), len(tl.taxon_set)
    return tree

if __name__ == '__main__':
    method = globals()[sys.argv[1]]
    tl = sys.argv[2]
    fname = None
    if len(sys.argv) > 4:
        fname = sys.argv[4]
    tree = njst(tl, method, fname)
    open(sys.argv[3], 'w').write(tree)
