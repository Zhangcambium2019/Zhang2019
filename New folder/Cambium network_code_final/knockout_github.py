#!/usr/bin/env python                                                           
import sys
import os
import random
import networkx
import operator
import matplotlib
import pylab
import math
from collections import defaultdict

def cumulativeoutdegree(n,i):
    s = set(n.successors(i))
    sold = 0
    ss = s.copy()
    while len(s) > sold:
        sold = len(s)
        for i in s:
            ss.update(set(n.successors(i)))
            #print(ss)
        s = ss.copy()
    return len(s)

def numdirpath(n):
    dir = 0
    for i in n.nodes():
        dir += cumulativeoutdegree(n,i)
        print(i,cumulativeoutdegree(n,i))
    return 1.0*dir/(len(n.nodes())*len(n.nodes()))

f = open(sys.argv[1])
n = networkx.DiGraph()
for line in f:
    l = line.strip().split('\t')
    n.add_edge(l[0],l[1])

print(numdirpath(n))            

os.system('dot '+sys.argv[1].replace('.dat','.dot')+' -Tpdf -Goverlap=scale > '+sys.argv[1].replace('.dat','.pdf'))

ff = open(sys.argv[1]+'.knock','w')

print('Single mutant predictions:')

l = []
for i in n.nodes():
    ntmp = n.copy()
    ntmp.remove_node(i)
    ntmp.add_node(i) # JUST REMOVING LINKS
    print(i)
    l.append((i,numdirpath(ntmp)))    

l.sort(key=operator.itemgetter(1))
for i in l:
    print(i[0],i[1])
    ff.write(str(i[0])+'\t'+str(i[1])+'\n')

print('\nDouble mutant predictions:')
ff.write('\n\n')

l = []
for i in n.nodes():
    for j in n.nodes():
        if i < j:
            ntmp = n.copy()
            ntmp.remove_node(i)
            ntmp.add_node(i) # JUST REMOVING LINKS
            ntmp.remove_node(j)
            ntmp.add_node(j) # JUST REMOVING LINKS
            l.append((i,j,numdirpath(ntmp)))
l.sort(key=operator.itemgetter(2))
for i in l:
    print(i[0],i[1],i[2])
    ff.write(str(i[0])+'\t'+str(i[1])+'\t'+str(i[2])+'\n')

ff.close()

