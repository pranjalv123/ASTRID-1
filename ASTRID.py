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
    def __init__(self, genetreefile):
        self.genetreefile = genetreefile
        self.pct = 0.0
        
    def read_trees(self):
        self.tl = dendropy.TreeList.get_from_path(self.genetreefile, 'newick')

    def generate_matrix(self):
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
        lines = []
        staxkeys = sorted(self.taxindices.keys())
    
        for i in staxkeys:
            vals = ' '.join(["%.3f" % (self.njmat[self.taxindices[i], self.taxindices[j]]) for j in staxkeys])
            lines.append('     '.join([i.label, vals]))
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
        method = getattr(DistanceMethods, method)
        self.tree = method(self.fname)

    def write_tree(self, outputfile):
        open(outputfile, 'w').write(self.tree)

if __name__ == '__main__':
#    parser = 

    
    method = sys.argv[1]
    fname = None
    if len(sys.argv) > 4:
        fname = sys.argv[4]

    a = ASTRID(sys.argv[2])
    a.read_trees()
    a.generate_matrix()
    a.write_matrix(fname)
    a.infer_tree(method)
    a.write_tree(sys.argv[3])
