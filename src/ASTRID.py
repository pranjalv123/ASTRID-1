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


class ASTRID:
    def __init__(self, genetrees):
        self.genetrees = genetrees
        self.pct = 0.0
        self.state = "Initialized"
        
    def read_trees(self):
        self.state = "Reading trees"
        self.tl = dendropy.TreeList.get_from_string(self.genetrees, 'newick')

    def generate_matrix(self):
        self.state = "Generating Matrix"
        self.taxindices = dict([(j, i) for i, j in enumerate(sorted(list(self.tl.taxon_namespace)))])
        self.countmat = np.eye(len(self.tl.taxon_namespace))
        self.njmat = np.zeros((len(self.tl.taxon_namespace), len(self.tl.taxon_namespace)))
        for t in self.tl:
            for e in t.edges():
                e.length=1
            m = PatristicDistanceMatrix_np(t, self.taxindices).distmat()
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
            lines.append('     '.join([i.label.replace(' ', '_'), vals]))
        distmat = '\n'.join([i.replace('--' ,nanplaceholder) for i in lines])

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
                method = "fastme"
        self.state = "Inferring tree with " + method
        method = getattr(DistanceMethods, method)
        self.tree = dendropy.Tree.get_from_string(method(self.fname), 'newick')
        self.state = "Done"

    def write_tree(self, outputfile):
        open(outputfile, 'w').write(self.tree_str())

    def tree_str(self):
        return self.tree.as_string('newick', suppress_edge_lengths=True, suppress_internal_node_labels=True)
    def run(self, method, fname=None):
        print "reading trees"
        self.read_trees()
        print "generating matrix"
        self.generate_matrix()
        print "writing matrix", fname
        self.write_matrix(fname)
        print "inferring tree"
        self.infer_tree(method)
        print self.tree_str()
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= "ASTRID: Accurate Species TRees from Internode Distances.")

    parser.add_argument('-i', '--input', required=True, dest='input',
                        help="File containing gene trees as newick strings")
    parser.add_argument('-o', '--output', dest='output',
                        help="Output file for species tree")
    parser.add_argument('-m', '--method', default='auto', dest='method',
                        help="Distance-based method to use (default: fastme if the distance matrix is complete, bionj otherwise")
    parser.add_argument('-c', '--cache', dest='cache',
                        help="Save distance matrix in PHYLIP format, or use cached matrix if it exists (useful for trying multiple distance-based methods)")
    
    args = parser.parse_args()

    
    method = args.method

    if 'cache' in vars(args):
        fname = args.cache
    else:
        fname = None
        
    a = ASTRID(open(args.input).read())
    a.run(method, fname)
    print a.tree_str()
    if 'output' in vars(args):
        a.write_tree(args.output)
