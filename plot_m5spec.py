#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity",
                        action="count",default=0)
    parser.add_argument('-f','--file',
                        help='input file for satellites',
                        type=str, default=None)
    parser.add_argument('-x','--cross',
                        help='do cross polarisations',
                        action='count',default=0)
    parser.add_argument('-b','--bandwidth',
                        help='bandwidth per IF',
                        type=float, default=16.0)
    args = parser.parse_args()

    # load in file
    spec = np.array(splitt(get_file(args.file))).astype(float)
    # assign x and y's axes
    freq = spec[:,0]*dnu
    if args.cross==0: 
        amp  = spec[:,1:]
        nifs = spec.shape[1]-1
    else: 
        amp  = spec[:,1:]
        nifs = (spec.shape[1]-1)/2.0


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
