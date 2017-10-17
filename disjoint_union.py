def unique(a):
    ''' return the list with duplicate elements removed '''
    return list(set(a))

def intersect(a, b):
    ''' return the intersection of two lists '''
    return list(set(a) & set(b))

def union(a, b):
    ''' return the union of two lists '''
    return list(set(a) | set(b))

    '''returns the disjoint_union of 2 lists'''
def disjoint_union(a, b):
    u = union (a, b)
    i = intersect (a, b)
    d_u = u

    for x in i:
        for y in u:
            if y == x:
                d_u.remove(x)
    return d_u
