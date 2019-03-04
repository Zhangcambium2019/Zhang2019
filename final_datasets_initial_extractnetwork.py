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

f = open('final_datasets_initial_network')
edges = {}
sig = {}
read = 1
row = set([])
col = set([])
header = f.readline().strip().replace('-OE','').split('\t')
for line in f:
    l = line.strip().split('\t')

    if l[0] == 'Genes/Lines':
        read = 2

    else:
        c = 1
        for i in l[1:]:
            if i != 'X':
                if read == 1:
                    edges[(l[0],header[c])] = float(i)
                    if l[0] != header[c]:
                        row.add(l[0])
                        col.add(header[c])
                if read == 2:
                    sig[(l[0],header[c])] = float(i)
            c += 1

ff = open('final_datasets_initial_network.dat','w')
fff = open('final_datasets_initial_network.dot','w')
fff.write('digraph finaldatasetsinitial\n{\n')
sigthresh = 0.05 # SIGNIFICANCE THRESHOLD OF P-VALUE
for i in edges:
    if i[0] != i[1] and sig[i] < sigthresh:
        repressor = 1.0-2.0*int(edges[i] < 1.0)
        ff.write(str(i[1])+'\t'+str(i[0])+'\t'+str(repressor)+'\t'+str(sig[i])+'\t'+str(edges[i])+'\n')
        if repressor == 1:
            fff.write('"'+str(i[1])+'" -> "'+str(i[0])+'" [style="setlinewidth('+str(edges[i])+')"];\n')
        if repressor == -1:
            fff.write('"'+str(i[1])+'" -> "'+str(i[0])+'" [style="setlinewidth('+str(1.0/edges[i])+')",arrowhead="tee"];\n')
ff.close()
fff.write('\n}\n')
fff.close()

ff = open('final_datasets_initial_network_high.dat','w')
fff = open('final_datasets_initial_network_high.dot','w')
fff.write('digraph finaldatasetsinitialhigh\n{\n')
sigthresh = 0.01 # SIGNIFICANCE THRESHOLD OF P-VALUE
for i in edges:
    if i[0] != i[1] and sig[i] < sigthresh:
        repressor = 1.0-2.0*int(edges[i] < 1.0)
        ff.write(str(i[1])+'\t'+str(i[0])+'\t'+str(repressor)+'\t'+str(sig[i])+'\t'+str(edges[i])+'\n')
        if repressor == 1:
            fff.write('"'+str(i[1])+'" -> "'+str(i[0])+'" [style="setlinewidth('+str(edges[i])+')"];\n')
        if repressor == -1:
            fff.write('"'+str(i[1])+'" -> "'+str(i[0])+'" [style="setlinewidth('+str(1.0/edges[i])+')",arrowhead="tee"];\n')
ff.close()
fff.write('\n}\n')
fff.close()

ff = open('final_datasets_initial_network_bonf.dat','w')
fff = open('final_datasets_initial_network_bonf.dot','w')
fff.write('digraph finaldatasetsinitialbonf\n{\n')
sigthresh = 0.05/(len(header)*(len(header)-1)) # SIGNIFICANCE THRESHOLD OF P-VALUE
for i in edges:
    if i[0] != i[1] and sig[i] < sigthresh:
        repressor = 1.0-2.0*int(edges[i] < 1.0)
        ff.write(str(i[1])+'\t'+str(i[0])+'\t'+str(repressor)+'\t'+str(sig[i])+'\t'+str(edges[i])+'\n')
        if repressor == 1:
            fff.write('"'+str(i[1])+'" -> "'+str(i[0])+'" [style="setlinewidth('+str(edges[i])+')"];\n')
        if repressor == -1:
            fff.write('"'+str(i[1])+'" -> "'+str(i[0])+'" [style="setlinewidth('+str(1.0/edges[i])+')",arrowhead="tee"];\n')
ff.close()
fff.write('\n}\n')
fff.close()
