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

# SIMPLIFIES ALL COHERENT FEED-FORWARD LOOPS
# READS IN EDGE LIST WITH THIRD COLUMN THAT SPECIFIES ACTIVATOR (1) OR REPRESSOR (-1)
# 'simplified' VERSION IN THAT WE NOW NO LONGER WORRY ABOUT CUTTING INDIRECT PATHS. THIS SHOULDN'T HAPPEN AS WE IDENTIFY ALL FEED-FORWARD LOOPS SIMULTANEOUSLY, AND THUS IF AN INDIRECT PATH IS CUT THEN AN EVEN MORE INDIRECT PATH MUST EXIST.
# NOTE: CURRENT SETTING HERE IS TO IGNORE SIGNIFICANCES (SEE remstrat BELOW)

f = open('final_datasets_initial_network.dat')
n = networkx.DiGraph()
for line in f:
    l = line.strip().split('\t')
    n.add_edge(l[0],l[1],{'type':float(l[2]),'sig':float(l[3]),'weight':float(l[4])})

remstrat = 2 # IGNORE SIGNIFICANCES
totalrm = 0
rmset = set([0]) # TO START LOOP
rmset2 = set([0]) # TO START LOOP
while len(rmset2) > 0 and len(rmset) > 0:
    rmset = set([])
    rmset2 = set([])
    indir = set([])
    indir2 = set([])
    indirdic = defaultdict(set)
    indirdic2 = defaultdict(set)
    for i in n.edges():
        incoh = -1
        coh = -1
        coh2 = -1
        s = set(n.successors(i[0])).intersection(set(n.predecessors(i[1])))
        if len(s) > 0:
            incoh = 0
            coh = 0
            coh2 = 0
        for j in s:
            r = n.get_edge_data(*i)['type']
            rr0 = n.get_edge_data(i[0],j)['type']
            rr1 = n.get_edge_data(j,i[1])['type']
            ss = n.get_edge_data(*i)['sig']
            ss0 = n.get_edge_data(i[0],j)['sig']
            ss1 = n.get_edge_data(j,i[1])['sig']
            incoh += int(r != rr0*rr1 or ss < ss0 or ss < ss1) 
            coh += int(r == rr0*rr1)*int(ss > ss0 and ss > ss1)
            if int(r == rr0*rr1)*int(ss > ss0 and ss > ss1) > 0:
                indir.add((i[0],j))
                indir.add((j,i[1]))
                indirdic[i].add((i[0],j))
                indirdic[i].add((j,i[1]))
            coh2 += int(r == rr0*rr1) # TO REMOVE ALL COHERENT DIRECT CONNECTIONS
            if int(r == rr0*rr1) > 0:
                indir2.add((i[0],j))
                indir2.add((j,i[1]))
                indirdic2[i].add((i[0],j))
                indirdic2[i].add((j,i[1]))
        if coh > 0:#incoh == 0:
            rmset.add(i)
            #print('@',i,j)
        if coh2 > 0:#incoh == 0:
            rmset2.add(i)
        #print(i,coh,incoh,len(s))

    #rmset -= indir # THIS IS CHANGE FOR 'simplified' VERSION
    #rmset2 -= indir2 # THIS IS CHANGE FOR 'simplified' VERSION

    if remstrat == 1:
        for i in rmset:
            print(i,indirdic[i])
            if n.in_degree(i[1]) > 1 and n.out_degree(i[0]) > 1: # SO WE DON'T CUT OFF NODES COMPLETELY, WHICH CAN HAPPEN IN CERTAIN CIRCUMSTANCES
                n.remove_edge(*i)
        totalrm += len(rmset)
        print(rmset,indir)

    if remstrat == 2:
        for i in rmset2:
            print(i,indirdic2[i])
            if n.in_degree(i[1]) > 1 and n.out_degree(i[0]) > 1: # SO WE DON'T CUT OFF NODES COMPLETELY, WHICH CAN HAPPEN IN CERTAIN CIRCUMSTANCES
                n.remove_edge(*i)
        totalrm += len(rmset2)
        print(rmset2,indir2)

print('Total edges:'+str(len(n.edges())+totalrm))
print('Edges removed:'+str(totalrm))
print('Edges remaining:'+str(len(n.edges())))

#for i in rmset:
#    n.remove_edge(*i)

ff = open('final_datasets_initial_par_enh_sim.dat','w')
fff = open('final_datasets_initial_weighted_par_enh_sim.dot','w')
fff.write('digraph melis\n{\n')
ffff = open('final_datasets_initial_par_enh_sim.dot','w')
ffff.write('digraph melis\n{\n')
for i in n.edges():
    repressor = n.get_edge_data(*i)['type']
    wt = n.get_edge_data(*i)['weight']
    ff.write(str(i[0])+'\t'+str(i[1])+'\t'+str(repressor)+'\n')
    if repressor == 1:
        fff.write('"'+str(i[0])+'" -> "'+str(i[1])+'" [style="setlinewidth('+str(wt)+')"];\n')
        ffff.write('"'+str(i[0])+'" -> "'+str(i[1])+'" ;\n')
    if repressor == -1:
        fff.write('"'+str(i[0])+'" -> "'+str(i[1])+'" [style="setlinewidth('+str(1.0/wt)+')",arrowhead="tee"];\n')
        ffff.write('"'+str(i[0])+'" -> "'+str(i[1])+'" [arrowhead="tee"];\n')
ff.close()
fff.write('\n}\n')
fff.close()
ffff.write('\n}\n')
ffff.close()
