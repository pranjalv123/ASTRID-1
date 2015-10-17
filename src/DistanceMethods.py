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
import ASTRID

path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+ '/ASTRID'
print path 
phydstar_exec=path + '/distmethods/' + 'PhyDstar.jar'
fastme_exec=path + '/distmethods/' + 'fastme'
fastme2_exec=path + '/distmethods/' + 'fastme2'


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

def fastme2(fname, method=None, nni=False, spr=False):
    print fname + '_fastme.t'
    args = [fastme2_exec, '-i', fname, '-o', fname + '_fastme2.t']
    if nni:
        args.append('-n')
    if spr:
        args.append('-s')
    if method:
        args.append('-m')
        args.append(method)
    p = subprocess.Popen(args)
    p.wait()
    tree = open(fname + '_fastme2.t').read()
    return tree

def fastme2_bal(fname):
    return fastme2(fname, 'bal')
def fastme2_bionj(fname):
    return fastme2(fname, 'bionj')
def fastme2_olsme(fname):
    return fastme2(fname, 'olsme')
def fastme2_nj(fname):
    return fastme2(fname, 'nj')
def fastme2_unj(fname):
    return fastme2(fname, 'unj')

def fastme2_bal_nni(fname):
    return fastme2(fname, 'bal', nni=True)
def fastme2_bionj_nni(fname):
    return fastme2(fname, 'bionj', nni=True)
def fastme2_olsme_nni(fname):
    return fastme2(fname, 'olsme', nni=True)
def fastme2_nj_nni(fname):
    return fastme2(fname, 'nj', nni=True)
def fastme2_unj_nni(fname):
    return fastme2(fname, 'unj', nni=True)

def fastme2_bal_nni_spr(fname):
    return fastme2(fname, 'bal', nni=True, spr=True)
def fastme2_bionj_nni_spr(fname):
    return fastme2(fname, 'bionj', nni=True, spr=True)
def fastme2_olsme_nni_spr(fname):
    return fastme2(fname, 'olsme', nni=True, spr=True)
def fastme2_nj_nni_spr(fname):
    return fastme2(fname, 'nj', nni=True, spr=True)
def fastme2_unj_nni_spr(fname):
    return fastme2(fname, 'unj', nni=True, spr=True)
