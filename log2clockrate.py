#!/home/observer/anaconda2/bin/python

import numpy as np, argparse, subprocess, datetime
from astropy.time import Time as aTime
import matplotlib.pyplot as plt
from scipy.optimize import least_squares

import pdb

######################################

def splitt(old_list):
    #splits the list entries into sublists
    new_list=[]
    for i in old_list:
        new_list+=[i.split()]
    return np.array(new_list)

def linear_model(p,t):
    return p[0]*t+p[1]

def linear_model_res(p,t,y):
    return (y - linear_model(p,t))

######################################

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('log',help='Log file',type=str)
    args = parser.parse_args()

    p = subprocess.Popen("grep fmout-gps "+args.log+" | awk -F/ '{print $1,$3}' | grep -v 'delay\|maser\|clkoff'",shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    g = list(p.stdout)
    G = np.array(map(lambda s: s.strip(), g))

#    pdb.set_trace()
    t, d = splitt(G).T
    T = aTime([datetime.datetime.strptime(i,'%Y.%j.%H:%M:%S.%f') for i in t]).jyear
    dt = (T - T[0])*3600*365.25 #sec
    D  = d.astype(float)*1e6    #usec

    lsq = least_squares(linear_model_res,[1,1],args=(dt,D))
    print('')
    print('{0:>10s}  {1:>6s}'.format('Rate','Offs'))
    print('{0:>10s}  {1:>6s}'.format('us/s','usec'))
    print('------------------')
    print('{:<+10.2E}  {:>+6.2f}'.format(*lsq.x))
    print('')

######################################

if __name__=='__main__':
    main()
