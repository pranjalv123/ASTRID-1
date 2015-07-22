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

import subprocess
import os


path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
phydstar_exec=path + '/distmethods/' + 'PhyDstar.jar'
fastme_exec=path + '/distmethods/' + 'fastme'


def phydstar(nj, fname):
    p = subprocess.Popen(['java',  '-jar', phydstar_exec, '-d', nj, '-i', fname])
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
    p = subprocess.Popen([fastme_exec, '-i', fname, '-o', fname + '_fastme.t'])
    p.wait()
    tree = open(fname + '_fastme.t').read()
    return tree
