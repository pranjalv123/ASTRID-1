#! /usr/bin/env python

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


# DendroPy Phylogenetic Computing Library

# Copyright (c) 2014 Jeet Sukumaran and Mark T. Holder.
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * The names of its contributors may not be used to endorse or promote
#       products derived from this software without specific prior written
#       permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL JEET SUKUMARAN OR MARK T. HOLDER
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


# If you use this work or any portion thereof in published work,
# please cite it as:

#    Sukumaran, J. and M. T. Holder. 2010. DendroPy: a Python library
#    for phylogenetic computing. Bioinformatics 26: 1569-1571.


"""
Statistics, metrics, measurements, and values calculated on (single) trees.
"""

import math
import numpy as np

EULERS_CONSTANT = 0.5772156649015328606065120900824024310421

class PatristicDistanceMatrix_np(object):
    """
    Calculates and maintains patristic distance information of taxa on a tree.
    ``max_dist_taxa`` and ``max_dist_nodes`` will return a tuple of taxon objects
    and corresponding nodes, respectively, that span the greatest path distance
    in the tree. The mid-point between the two is *guaranteed* to be on the
    closer to the first item of each pair.
    """

    def __init__(self, tree=None, taxindices=None):
        self.tree = None
        self.taxon_namespace = None
        self.taxon_inds = {}
        self.taxindices = taxindices
        self._pat_dists = None
        self._path_steps = {}
        self.max_dist = None
        self.max_dist_taxa = None
        self.max_dist_nodes = None
        self._mrca = {}
        if tree is not None:
            self.tree = tree
            self.calc()

    def __call__(self, taxon1, taxon2):
        """
        Returns patristic distance between two taxon objects.
        """
        if taxon1 is taxon2:
            return 0.0
        return self._pat_dists[taxon1, taxon2]

    def mrca(self, taxon1, taxon2):
        """
        Returns MRCA of two taxon objects.
        """
        if taxon1 is taxon2:
            return taxon1
        try:
            return self._mrca[taxon1][taxon2]
        except KeyError:
            return self._mrca[taxon2][taxon1]

    def path_edge_count(self, taxon1, taxon2):
        """
        Returns the number of edges between two taxon objects.
        """
        if taxon1 is taxon2:
            return 0
        try:
            return self._path_steps[taxon1][taxon2]
        except KeyError:
            return self._path_steps[taxon2][taxon1]

    def calc(self, tree=None, create_midpoints=None, is_bipartitions_updated=False):
        """
        Calculates the distances. Note that the path length (in number of
        steps) between taxa that span the root will be off by one if
        the tree is unrooted.
        """
        if tree is not None:
            self.tree = tree
        assert self.tree is not None
        if not is_bipartitions_updated:
            self.tree.encode_bipartitions()
        self.taxon_namespace = self.tree.taxon_namespace
        self._pat_dists = np.zeros((len(self.taxon_namespace), len(self.taxon_namespace)))

        
        self._path_steps = {}
        for i1, t1 in enumerate(self.taxon_namespace):
            self._path_steps[t1] = {}
            self._mrca[t1] = {}
            self.max_dist = None
            self.max_dist_taxa = None
            self.max_dist_nodes = None

        for node in self.tree.postorder_node_iter():
            children = node.child_nodes()
            if len(children) == 0:
                node.desc_paths = {node : (0,0)}
            else:
                node.desc_paths = {}
                for cidx1, c1 in enumerate(children):
                    for desc1, (desc1_plen, desc1_psteps) in c1.desc_paths.items():
                        node.desc_paths[desc1] = (desc1_plen + c1.edge.length, desc1_psteps + 1)
                        for c2 in children[cidx1+1:]:
                            for desc2, (desc2_plen, desc2_psteps) in c2.desc_paths.items():
                                self._mrca[desc1.taxon][desc2.taxon] = c1.parent_node
                                pat_dist = node.desc_paths[desc1][0] + desc2_plen + c2.edge.length
                                t1i = self.taxindices[desc1.taxon]
                                t2i = self.taxindices[desc2.taxon]
                                self._pat_dists[t1i, t2i] = pat_dist
                                self._pat_dists[t2i, t1i] = pat_dist
                                path_steps = node.desc_paths[desc1][1] + desc2_psteps + 1
                                self._path_steps[desc1.taxon][desc2.taxon] = path_steps
                                if self.max_dist is None or pat_dist > self.max_dist:
                                    self.max_dist = pat_dist
                                    midpoint = float(pat_dist) / 2
                                    if midpoint - node.desc_paths[desc1][0] <= 0:
                                        self.max_dist_nodes = (desc1, desc2)
                                        self.max_dist_taxa = (desc1.taxon, desc2.taxon)
                                    else:
                                        self.max_dist_nodes = (desc2, desc1)
                                        self.max_dist_taxa = (desc2.taxon, desc1.taxon)
                    del(c1.desc_paths)

    def  distmat(self):
        """
        Returns list of patristic distances.
        """
        return self._pat_dists
        
    def sum_of_distances(self):
        """
        Returns sum of patristic distances on tree.
        """
        return sum(self.distances())
