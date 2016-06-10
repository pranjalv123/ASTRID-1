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
import sys
import subprocess
import tempfile
import os
import time
import argparse
import DistanceMethods


class ASTRID:
    def __init__(self, genetrees, remap_names=True):
        self.genetrees = genetrees
        self.pct = 0.0
        self.state = "Initialized"
        self.remap_names=remap_names
                
    def write_matrix(self, fname=None, nanplaceholder='-99.0', taxon_cutoff = 0):
        if getattr( sys, 'frozen', False ) :
            path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        else:
            path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/../../'
        
        self.state = "Writing matrix"

        tmp = None
        if fname == None:
            tmpfd, fname = tempfile.mkstemp()
            tmp = os.fdopen(tmpfd, 'w')
        tmp = open(fname, 'w')    
        
        args = [path + '/makemat', '--matrix', fname, '--taxlist', fname + '_taxlist', '--taxcutoff', str(taxon_cutoff), '--nanplaceholder', str(nanplaceholder), '--n_missing', fname + '_nmissing']

        subprocess.Popen(args, stdin = subprocess.PIPE).communicate(self.genetrees)
        
        self.fname = fname
        self.taxindices_inv = [i.strip() for i in open(fname + '_taxlist').readlines()]
        self.has_missing = int(open(fname + '_nmissing').read())
        

    def infer_tree(self, method):
        if method == "auto":
            if self.has_missing:
                method = "bionj"
            else:
                method = "fastme2_bal_nni"
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
        print "generating matrix"
        t = time.time()
        self.write_matrix(fname, taxon_cutoff)
        print time.time() - t, "seconds"
        print "inferring tree"
        t = time.time()
        self.infer_tree(method)
        print time.time() - t, "seconds"
        
