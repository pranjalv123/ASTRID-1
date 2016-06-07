# This file is part of ASTRID.
#
# ASTRID is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ASTRID is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ASTRID.  If not, see <http://www.gnu.org/licenses/>.

import dendropy
import numpy as np
import sys
import subprocess
import tempfile
import os
from numpy import ma
import time
import argparse
from PatristicDistanceMatrix import PatristicDistanceMatrix_np
import DistanceMethods
import fastdm

class ASTRID:
    def __init__(self, genetrees, remap_names=True):
        self.genetrees = genetrees
        self.pct = 0.0
        self.state = "Initialized"
        self.remap_names=remap_names
        
    def read_trees(self, taxon_cutoff = 0):
        self.state = "Reading trees"
        if isinstance(self.genetrees, str):
            self.tl = dendropy.TreeList.get_from_string(self.genetrees, 'newick', rooting='force-rooted')
            
        else:
            self.tl = self.genetrees
        for t in self.tl:
            t.resolve_polytomies()
        self.tl = dendropy.TreeList([i for i in self.tl if len(i.leaf_nodes())> taxon_cutoff])
        print len(self.tl), "trees with", len(self.tl.taxon_namespace), "taxa"
    def generate_matrix(self):
        self.state = "Generating Matrix"
        self.taxindices = dict([(j, i) for i, j in enumerate(sorted(list(self.tl.taxon_namespace)))])
        self.taxindices_inv = dict([(i, j.label) for i, j in enumerate(sorted(list(self.tl.taxon_namespace)))])

        self.countmat = np.eye(len(self.tl.taxon_namespace))
        self.njmat = np.zeros((len(self.tl.taxon_namespace), len(self.tl.taxon_namespace)))
        for t in self.tl:
            for e in t.edges():
                e.length=1
            m = fastdm.get_distmat(t, self.taxindices)
            # mold = PatristicDistanceMatrix_np(t, self.taxindices).distmat()
            # if ((m == mold).all() == False):
            #     np.savetxt('/tmp/diff', (m - mold), fmt="%d")
            #     np.savetxt('/tmp/m', m, fmt="%d")
            #     np.savetxt('/tmp/mold', mold, fmt="%d")
            #     assert(False)
            self.countmat += (m > 0)
            self.njmat += m
            self.pct += 1.0/len(self.tl)
        self.has_missing = (self.countmat == 0).any()
        self.njmat = ma.array(self.njmat, mask = (self.countmat == 0))
        self.countmat = ma.array(self.countmat, mask = (self.countmat == 0))
        self.njmat /= self.countmat

    def write_matrix(self, fname=None, nanplaceholder='-99.0'):
        self.state = "Writing matrix"
        lines = []
        staxkeys = sorted(self.taxindices.keys())
        for i in staxkeys:
            vals = ' '.join(["%.3f" % (self.njmat[self.taxindices[i], self.taxindices[j]]) for j in staxkeys])
            if self.remap_names:
                lines.append('     '.join([str(self.taxindices[i]), vals]))
            else:
                lines.append('     '.join([i.label.replace(' ', '_'), vals]))
        distmat = '\n'.join([i.replace('--' ,nanplaceholder).replace('nan', nanplaceholder) for i in lines])

        tmp = None
        if fname == None:
            tmpfd, fname = tempfile.mkstemp()
            tmp = os.fdopen(tmpfd, 'w')
        tmp = open(fname, 'w')
        tmp.write(str(len(self.taxindices)))
        tmp.write('\n')
        tmp.write(distmat)
        tmp.write('\n')
        tmp.close()
        self.fname = fname

    def infer_tree(self, method):
        if method == "auto":
            if self.has_missing:
                method = "bionj"
            else:
                method = "fastme2"
        self.state = "Inferring tree with " + method
        method = getattr(DistanceMethods, method)
        self.tree = dendropy.Tree.get_from_string(method(self.fname), 'newick')
        if self.remap_names:
            for t in self.tree.taxon_namespace:
                t.label = self.taxindices_inv[int(t.label)]
        self.state = "Done"

    def write_tree(self, outputfile):
        open(outputfile, 'w').write(self.tree_str())

    def tree_str(self):
        return self.tree.as_string('newick', suppress_edge_lengths=True, suppress_internal_node_labels=True)
    def run(self, method, fname=None, taxon_cutoff = 0):
        print "reading trees"
        t = time.time()
        self.read_trees(taxon_cutoff)
        print time.time() - t, "seconds"
        print "generating matrix"
        t = time.time()
        self.generate_matrix()
        print time.time() - t, "seconds"
        print "writing matrix", fname
        t = time.time()
        self.write_matrix(fname)
        print time.time() - t, "seconds"
        print "inferring tree"
        t = time.time()
        self.infer_tree(method)
        print time.time() - t, "seconds"
        
