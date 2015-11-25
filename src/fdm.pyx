import cython

import numpy as np
cimport numpy as np

import dendropy



@cython.boundscheck(True)
@cython.wraparound(False)
def getranks(np.ndarray[np.int_t, ndim=1] lchildren not None,
             np.ndarray[np.int_t, ndim=1] rchildren not None,
             np.ndarray[np.int_t, ndim=1] ranks not None,
             np.ndarray[np.int_t, ndim=1] leaves not None,
             np.int_t root,
             np.int_t nedges
           ):

    cdef np.ndarray[np.int_t, ndim=1] roots_s
    cdef np.ndarray[np.int_t, ndim=1] ranks_s

    cdef np.int pos, n
   
    roots_s = np.zeros(1+nedges, dtype=np.int)
    ranks_s = np.zeros(1+nedges, dtype=np.int)

    pos = 0

    roots_s[pos] = root
    ranks_s[pos] = 1
    pos += 1

    n = 0
    while pos > 0:
        pos -= 1
        root = roots_s[pos]
        rank = ranks_s[pos]

        if lchildren[root] == -1:
            leaves[n] = root
            ranks[n] = rank
            n += 1
        else:
            ranks_s[pos] = rank+1
            roots_s[pos] = lchildren[root]
            pos += 1

            ranks_s[pos] = rank+1
            roots_s[pos] = rchildren[root]
            pos += 1


    return n
        

@cython.boundscheck(True)
@cython.wraparound(False)
def getDM(np.ndarray[np.int_t, ndim=1] lchildren not None,
          np.ndarray[np.int_t, ndim=1] rchildren not None,
          np.int_t ninternal,
          np.int_t nleaves,
          np.int_t root,
          np.ndarray[np.int_t, ndim=2] dmat not None):

    cdef np.int_t i

    i = nleaves

    cdef np.ndarray[np.int_t, ndim=1] ranks_l, ranks_r, leaves_l, leaves_r

    cdef np.int_t r, l

    examined = set()
    
    while i < nleaves + ninternal:
        
        ranks_l = np.zeros(nleaves, dtype=np.int) - 1
        ranks_r = np.zeros(nleaves, dtype=np.int) - 1
        leaves_l = np.zeros(nleaves, dtype=np.int) - 1
        leaves_r = np.zeros(nleaves, dtype=np.int) - 1



        nl = getranks(lchildren, rchildren, ranks_l, leaves_l, lchildren[i], ninternal + nleaves)
        nr = getranks(lchildren, rchildren, ranks_r, leaves_r, rchildren[i], ninternal + nleaves)

        r = 0
        while r < nr:
            l = 0
            while l < nl:
                dmat[leaves_r[r], leaves_l[l]] = ranks_r[r] + ranks_l[l]
                dmat[leaves_l[l], leaves_r[r]] = ranks_r[r] + ranks_l[l]
                l += 1
            r += 1
        i += 1

    return dmat
def get_distmat(t, taxindices):
    ninternal = len(t.internal_nodes())
    nleaves = len(t.taxon_namespace)

    cdef np.ndarray[np.int_t, ndim=1] lchildren, rchildren
    
    lchildren = np.hstack([np.zeros(nleaves, dtype=np.int) - np.int(1), np.zeros(ninternal, dtype=np.int)])
    rchildren = np.hstack([np.zeros(nleaves, dtype=np.int) - np.int(1), np.zeros(ninternal, dtype=np.int)])

    indices = {}

    i = nleaves
    
    for n in t.internal_nodes():
        n.taxon = str(i) + '_i'
        indices[n.taxon] = i
        i += 1

    indices.update(taxindices)
        
    for n in t.internal_nodes():
        if len(n.child_nodes()) != 2:
            assert(False)
        lchildren[indices[n.taxon]] = indices[n.child_nodes()[0].taxon]
        rchildren[indices[n.taxon]] = indices[n.child_nodes()[1].taxon]

    s1 = set(lchildren)
    s2 = set(rchildren)


    dmat = np.zeros([nleaves, nleaves], dtype=np.int)

    root = indices[t.seed_node.taxon]

    return getDM(lchildren, rchildren, ninternal, nleaves, root, dmat)
