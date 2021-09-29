#!/usr/bin/env python

# Python script deigned to take the log files from Ke, Yg, Ho and Cd and generate st.antab files
# Written by Lucas J. Hyland March 2019

import numpy as np
import sys, os
import matplotlib.pyplot as plt

def main():
    exp=sys.argv[1]
    if os.path.exists(exp+'cd.log'):
        ceduna(exp)          
    if os.path.exists(exp+'yg.log'):
        #yarragadee(exp)
        yarragadee_tmp(exp)
    if os.path.exists(exp+'ke.log'):
        katherine_tmp(exp)
    if os.path.exists(exp+'ho.log'):
        hobart26m(exp)

def get_file(path):
    #opens and external file and makes it into a list
    fopen = path
    f=open(fopen, 'r+')
    g=list(f)
    g=map(lambda s: s.strip(), g)
    return g

def splitt(old_list):
    #splits the list entries into sublists
    new_list=[]
    for i in old_list:
        new_list+=[i.split()]
    return new_list

def splitt2(old_list,sym):
    #splits the list entries into sublists
    new_list=[]
    for i in old_list:
        new_list+=[i.split(sym)]
    return new_list

def make_vector(m, col):
    x=[]
    for i in m:
        x+=[i[col]]
    return x

def make_float(m):
    x=[]
    for i in m:
        x+=[float(i)]
    return x

def running_min(parameter, thinning):
    ###gets max of list into smaller list by thinning factor
    N = len(parameter)
    parameter = make_float(parameter)
    thin_paramater = range(len(parameter)/thinning)
    thin_paramater[0]=parameter[0]
    for i in range(len(parameter)/thinning-1):
        i=i+1
        thin_paramater[i]=min(parameter[(thinning*i-thinning/2):(thinning*i+thinning/2)])
    return thin_paramater

def thin(parameter,thinning):
    ###thins list without averaging by factor thinning
    N = len(parameter)
    thin_paramater = []
    for i in range(len(parameter)/thinning):
        thin_paramater+=[parameter[thinning*i]]
    return thin_paramater

def convertyyyydddhhmmsss2ddd_hhmmss(time_list):
    new_time_list = []
    for i in range(len(time_list)):
        [year,year_day,time,dummy] = time_list[i].split('.')
        new_time_list += [[year_day,time]]
    return new_time_list

def average(parameter,thinning):
    ###averages list into smaller list by thinning factor
    N = len(parameter)
    parameter = make_float(parameter)
    thin_paramater = range(len(parameter)/thinning)
    thin_paramater[0]=parameter[0]
    for i in range(len(parameter)/thinning-1):
        i=i+1
        thin_paramater[i]=sum(parameter[(thinning*i-thinning/2):(thinning*i+thinning/2)])/thinning
    return thin_paramater

def combine_lines(x,y):
    #specifc to this script
    new_x = []
    new_y = []
    for i in range(len(x)-1):
        if x[i]==x[i+1]:
            new_x+=[x[i]]
            y_el = []
            for j in range(len(y[i])):
                if not y[i][j]==None:
                    y_el+=[y[i][j]]
                elif not y[i+1][j]==None:
                    y_el+=[y[i+1][j]]
            new_y+=[y_el]
    return [new_x, new_y]

def ceduna(experiment):
    os.system('cat '+experiment+'cd.log | grep "/tsys" | grep -v rakbus > /tmp/tsys.tmp')
    f = np.matrix(splitt2(get_file('/tmp/tsys.tmp'),'/'))
    t1 = []
    x1 = []
    t2 = []
    x2 = []
    for i in range(len(f)):
        if f[i,1]=='tsys1':
            t1+=[float(f[i,2])]
            x1+=[f[i,0].strip("#tsys#")]
        elif f[i,1]=='tsys2':
            t2+=[float(f[i,2])]
            x2+=[f[i,0].strip("#tsys#")]
    X = thin(convertyyyydddhhmmsss2ddd_hhmmss(x1),5)
    # assume they are identical x1 == x2\
    # Ceduna seems to open 
    T1 = running_min(t1,5)
    T2 = running_min(t2,5)
    fout = './CD.antab'
    f = open(fout,'w+')
    print >> f, "! CD = Ceduna"
    f.close()
    f = open(fout,'a+')
    print >> f, "! "
    print >> f, "! Gain curve from R. Dodson - 15 June 1999"
    print >> f, "! guesstimate DFPU = 0.077 (scaled from Hart 26 m)"
    print >> f, "! but use 1.0 here since raw Tsys files are already SEFD/Jy not Tsys/K "
    print >> f, "!                                                                      PAJ"
    print >> f, "GAIN CD ELEV DPFU = 1.0 FREQ=1,25000"
    print >> f, "POLY=0.577490,0.0483611,-0.00224059,5.10738e-05,-5.46125e-07,2.18304e-09 \n /" 
    print >> f, "TSYS CD TIMEOFF=0.0 FT=1.0"
    print >> f, "INDEX='R1:8', 'R9:16' \n /"
    for j in range(len(X)):
        print >> f, X[j][0], X[j][1], T1[j], T2[j]
    print >> f, "/"
    print >> f, " "
    f.close()
    return

def hobart26m(experiment):
    os.system('cat '+experiment+'ho.log | grep "#/tsys" | grep -v rakbus > /tmp/tsys.tmp')
    f = np.matrix(splitt2(get_file('/tmp/tsys.tmp'),'/'))
    t1 = []
    x1 = []
    t2 = []
    x2 = []
    for i in range(len(f)):
        if f[i,1]=='tsys1':
            t1+=[float(f[i,2])]
            x1+=[f[i,0].strip("#tsys#")]
        elif f[i,1]=='tsys2':
            t2+=[float(f[i,2])]
            x2+=[f[i,0].strip("#tsys#")]
    X = thin(convertyyyydddhhmmsss2ddd_hhmmss(x1),5)
    # assume they are identical x1 == x2\
    T1 = running_min(t1,5)
    T2 = running_min(t2,5)
    fout = './HO.antab'
    f = open(fout,'w+')
    print >> f, "! HOB = Hobart "
    f.close()
    f = open(fout,'a+')
    print >> f,"!"
    print >> f,"! Fitted polynomial to X-band gain values from M. Costa (June 2000)"
    print >> f,"! (Added in 2 artificial values gain=1 at za=0,10 to flatten curve.)"
    print >> f,"!                                   HEB  Nov 2000"
    print >> f,"!"
    print >> f,"! Guesstimate DFPU = 0.058 from similar 26 m at Hart"
    print >> f,"! but use 1.0 here since raw Tsys files are already SEFD/Jy not Tsys/K   PAJ"
    print >> f,"!"
    print >> f,"GAIN HO  ALTAZ DPFU = 1.0, FREQ=1,25000"
    print >> f,"POLY=0.999405, 0.000335693, 6.67572e-06, -1.16229e-06, 3.11993e-08,-2.61934e-10"
    print >> f,"/"
    print >> f, "TSYS HO TIMEOFF=0.0 FT=1.0"
    print >> f, "INDEX='R1:8', 'R9:16' \n /"
    for j in range(len(X)):
        print >> f, X[j][0], X[j][1], T1[j], T2[j]
    print >> f, "/"
    print >> f, " "
    f.close()
    return

def yarragadee(experiment):
    os.system('cat '+experiment+'yg.log | grep "/tsys/" > /tmp/tsys.tmp')
    f = np.matrix(splitt2(get_file('/tmp/tsys.tmp'),'/'))
    x   = []
    t   = []
    for i in range(len(f)):
        [l1,u1,l2,u2,l3,u3,l4,u4,l5,u5,l6,u6,l7,u7,l8,u8]=[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
        if len(f[i,2].split(','))==18:
            if '1l' in f[i,2]:
                [d,l1,d,u1,d,l2,d,u2,d,l3,d,u3,d,l4,d,u4,d,ia] = f[i,2].split(',')
            elif '5l' in f[i,2]:
                [d,l5,d,u5,d,l6,d,u6,d,l7,d,u7,d,l8,d,u8,d,ib] = f[i,2].split(',')
                temps = f[i,2].split(',')[-1] 
            x   += [f[i,0].strip("#tsys#")]
            t   += [[l1,u1,l2,u2,l3,u3,l4,u4,l5,u5,l6,u6,l7,u7,l8,u8]]
    [time,temps] = combine_lines(x,t)
    T = np.matrix(temps)
    L1=running_min(T[:,0],5)
    U1=running_min(T[:,1],5)
    L2=running_min(T[:,2],5)
    U2=running_min(T[:,3],5)
    L3=running_min(T[:,4],5)
    U3=running_min(T[:,5],5)
    L4=running_min(T[:,6],5)
    U4=running_min(T[:,7],5)
    L5=running_min(T[:,8],5)
    U5=running_min(T[:,9],5)
    L6=running_min(T[:,10],5)
    U6=running_min(T[:,11],5)
    L7=running_min(T[:,12],5)
    U7=running_min(T[:,13],5)
    L8=running_min(T[:,14],5)
    U8=running_min(T[:,15],5)
    X = thin(convertyyyydddhhmmsss2ddd_hhmmss(time),5)
    T_final = (np.matrix([L1,U1,L2,U2,L3,U3,L4,U4,L5,U5,L6,U6,L7,U7,L8,U8]).T).tolist()
    fout = './YG.antab'
    f = open(fout,'w+')
    print >> f, "! YG = Yarragadee"
    f.close()
    f = open(fout,'a+')
    print >> f, "GAIN YG ELEV DPFU=1.0 FREQ=8000,10000 POLY=0.87,4.75E-3,-4.33E-5"
    print >> f, "/"
    print >> f, "GAIN YG ELEV DPFU=1.0 FREQ=2000,2500 POLY=1.0"
    print >> f, "/"
    print >> f, "TSYS YG FT=40.0 TIMEOFF=0.0"
    print >> f, "INDEX='R1','R2','R3','R4','R5','R6','R7','R8','R9','R10','R11','R12','R13','R14','R15','R16'"
    print >> f, "/"
    for j in range(len(X)):
        print >> f, X[j][0], X[j][1], T_final[j][0],T_final[j][1],T_final[j][2],T_final[j][3],T_final[j][4],T_final[j][5],T_final[j][6],T_final[j][7],T_final[j][8],T_final[j][9],T_final[j][10],T_final[j][11],T_final[j][12],T_final[j][13],T_final[j][14],T_final[j][15]
    print >> f, "/"
    print >> f, " "
    f.close()
    return   

def yarragadee_tmp(experiment):
    #tmp because at the moment of writing Katherine only has IF levels available
    os.system('cat '+experiment+'yg.log | grep "/tsys/" > /tmp/tsys.tmp')
    f = np.matrix(splitt2(get_file('/tmp/tsys.tmp'),'/'))
    x1   = []
    x2   = []
    ia   = []
    ib   = []
    for i in range(len(f)):
        if 'ia' in f[i,2]:
            ia  += [f[i,2].split(',')[-1].replace('$','9')]
            x1  += [f[i,0].strip("#tsys#")]
        elif 'ib' in f[i,2]:
            ib  += [f[i,2].split(',')[-1].replace('$','9')]
            x2  += [f[i,0].strip("#tsys#")]
    X = thin(convertyyyydddhhmmsss2ddd_hhmmss(x1),10)
    IA=average(ia,10)
    IB=average(ib,10)
    fout = './YG.antab'
    f = open(fout,'w+')
    print >> f, "! YG = Yarragadee"
    f.close()
    f = open(fout,'a+')
    print >> f, "GAIN YG ELEV DPFU=1.0 FREQ=8000,10000 POLY=0.87,4.75E-3,-4.33E-5"
    print >> f, "/"
    print >> f, "GAIN YG ELEV DPFU=1.0 FREQ=2000,2500 POLY=1.0"
    print >> f, "/"
    print >> f, "TSYS YG FT=40.0 TIMEOFF=0.0"
    print >> f, "INDEX='R1:8','R9:16'"
    print >> f, "/"
    for j in range(len(X)):
        print >> f, X[j][0], X[j][1], IA[j], IB[j]
    print >> f, "/"
    print >> f, " "
    f.close()
    return   

def katherine(experiment):
    os.system('cat '+experiment+'ke.log | grep "/tsys/" > /tmp/tsys.tmp')
    f = np.matrix(splitt2(get_file('/tmp/tsys.tmp'),'/'))
    x   = []
    t   = []
    for i in range(len(f)):
        [l1,u1,l2,u2,l3,u3,l4,u4,l5,u5,l6,u6,l7,u7,l8,u8]=[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
        if len(f[i,2].split(','))==18:
            if '1l' in f[i,2]:
                [d,l1,d,u1,d,l2,d,u2,d,l3,d,u3,d,l4,d,u4,d,ia] = f[i,2].split(',')
            elif '5l' in f[i,2]:
                [d,l5,d,u5,d,l6,d,u6,d,l7,d,u7,d,l8,d,u8,d,ib] = f[i,2].split(',')
                temps = f[i,2].split(',')[-1] 
            x   += [f[i,0].strip("#tsys#")]
            t   += [[l1,u1,l2,u2,l3,u3,l4,u4,l5,u5,l6,u6,l7,u7,l8,u8]]
    [time,temps] = combine_lines(x,t)
    T = np.matrix(temps)
    L1=running_min(T[:,0],5)
    U1=running_min(T[:,1],5)
    L2=running_min(T[:,2],5)
    U2=running_min(T[:,3],5)
    L3=running_min(T[:,4],5)
    U3=running_min(T[:,5],5)
    L4=running_min(T[:,6],5)
    U4=running_min(T[:,7],5)
    L5=running_min(T[:,8],5)
    U5=running_min(T[:,9],5)
    L6=running_min(T[:,10],5)
    U6=running_min(T[:,11],5)
    L7=running_min(T[:,12],5)
    U7=running_min(T[:,13],5)
    L8=running_min(T[:,14],5)
    U8=running_min(T[:,15],5)
    X = thin(convertyyyydddhhmmsss2ddd_hhmmss(time),5)
    T_final = (np.matrix([L1,U1,L2,U2,L3,U3,L4,U4,L5,U5,L6,U6,L7,U7,L8,U8]).T).tolist()
    fout = './KE.antab'
    f = open(fout,'w+')
    print >> f, "! Ke = Katherine"
    f.close()
    f = open(fout,'a+')
    print >> f, "GAIN YG ELEV DPFU=1.0 FREQ=8000,10000 POLY=0.87,4.75E-3,-4.33E-5"
    print >> f, "/"
    print >> f, "GAIN YG ELEV DPFU=1.0 FREQ=2000,2500 POLY=1.0"
    print >> f, "/"
    print >> f, "TSYS YG FT=40.0 TIMEOFF=0.0"
    print >> f, "INDEX='R1','R2','R3','R4','R5','R6','R7','R8','R9','R10','R11','R12','R13','R14','R15','R16'"
    print >> f, "/"
    for j in range(len(X)):
        print >> f, X[j][0], X[j][1], T_final[j][0],T_final[j][1],T_final[j][2],T_final[j][3],T_final[j][4],T_final[j][5],T_final[j][6],T_final[j][7],T_final[j][8],T_final[j][9],T_final[j][10],T_final[j][11],T_final[j][12],T_final[j][13],T_final[j][14],T_final[j][15]
    print >> f, "/"
    f.close()
    return  

def katherine_tmp(experiment):
    #tmp because at the moment of writing Katherine only has IF levels available
    os.system('cat '+experiment+'ke.log | grep "/tsys/" > /tmp/tsys.tmp')
    f = np.matrix(splitt2(get_file('/tmp/tsys.tmp'),'/'))
    x1   = []
    x2   = []
    ia   = []
    ib   = []
    for i in range(len(f)):
        if 'ia' in f[i,2]:
            ia  += [f[i,2].split(',')[-1].replace('$','9')]
            x1  += [f[i,0].strip("#tsys#")]
        elif 'ib' in f[i,2]:
            ib  += [f[i,2].split(',')[-1].replace('$','9')]
            x2  += [f[i,0].strip("#tsys#")]
    X = thin(convertyyyydddhhmmsss2ddd_hhmmss(x1),10)
    IA=average(ia,10)
    IB=average(ib,10)
    fout = './KE.antab'
    f = open(fout,'w+')
    print >> f, "! KE = Katherine"
    f.close()
    f = open(fout,'a+')
    print >> f, "GAIN KE ELEV DPFU=1.0 FREQ=8000,10000 POLY=0.87,4.75E-3,-4.33E-5"
    print >> f, "/"
    print >> f, "GAIN KE ELEV DPFU=1.0 FREQ=2000,2500 POLY=1.0"
    print >> f, "/"
    print >> f, "TSYS KE FT=40.0 TIMEOFF=0.0"
    print >> f, "INDEX='R1:8','R9:16'"
    print >> f, "/"
    for j in range(len(X)):
        print >> f, X[j][0], X[j][1], IA[j], IB[j]
    print >> f, "/"
    print >> f, " "
    f.close()
    return   

if __name__=='__main__':
    main()




