#!/usr/bin/env python3

import numpy as np, pdb
import os,sys,argparse

'''
Want to log in to the relevant flexbuf remotely, get a scan list
then compare to any local rd1 files
'''

def get_fb(tel):
    flexbuf = {'cd':'flexbuffcd','ke':'flexbuff-2ke','yg':'flexbuff-2yg'}
    try: fb = flexbuf[tel]
    except KeyError: sys.exit('No known telescope {}'.format(tel))
    return fb

def get_remote_scans(fb,exper,tel):
    # parse scans and sizes to python
    # first 7 entries are [Found, n, recordings, in, m, chunks, size]
    ret = os.popen('ssh {} \"vbs_ls -l {}_{}*\"'.format(fb,exper,tel)).read().split()
    if len(ret)==0:
        sys.exit('No remote scans for {} found on {}'.format(exper,fb))
    [tmp,n,tmp,tmp,tmp,tmp,tmp] = ret[:7]
    #print(ret)
    # old way before disks died and lost bytes
    # scans = np.reshape(ret[7:],(int(n),8))[:,(3,7)]
    scans = []
    roll_count = 0
    for i in range(int(n)): # iterate over scans
        if 'recovered' in ret[7:][roll_count:(roll_count+11)]:
            scans.append(ret[7:][roll_count:(roll_count+11)])
            roll_count += 11
        else: 
            scans.append(ret[7:][roll_count:(roll_count+7)])
            roll_count += 7
    scanss = np.reshape(ret[7:],(int(n),8))[:,(3,7)]
    #print(scanss)
    return scanss

def get_local_scans(exper,tel):
    ret = os.popen("ls -l /mnt/rd1/AUSTRAL/{0:}{1:}/{0:}_{1:}*".format(exper,tel)).read().split()
    if len(ret)==0:
        print('No local scans for {} found'.format(exper))
        return np.array([['0','']])
    scans = np.reshape(ret,(int(len(ret)/9.0),9))[:,(4,8)]
    return scans

def compare_scan_lists(rscans,lscans,tol):
    # iterate over remote scans and find matching scans
    # will not consider transferred then deleted scans
    missing    = []
    incomplete = []
    for i in range(len(rscans)):
        try:
            indx = [np.where(lscans[:,1]==s) for s in lscans[:,1] if rscans[i,1] in s][0]
        except IndexError:
            print('{:s} missing'.format(rscans[i,1]))
            missing.append(rscans[i,1])
            continue
        if len(indx)==0:
            print('{:s} missing'.format(rscans[i,1]))
            missing.append(rscans[i,1])
            continue
        dsize = -int(lscans[indx,0].squeeze()) + int(rscans[i,0])
        if dsize/float(rscans[i,0]) > tol:
             print('{:s} missing {:7.1f}MB ({:5.2f}%)'.format(rscans[i,1],dsize/1.e6,100*dsize/float(rscans[i,0])))
             incomplete.append(rscans[i,1])
    print('Remote {:15d} bytes'.format(rscans[:,0].astype(int).sum() ))
    print('Local  {:15d} bytes'.format(lscans[:,0].astype(int).sum() ))
    print('Missing {:4.2f}%'.format(100*(1-lscans[:,0].astype(float).sum()/rscans[:,0].astype(float).sum())))
    return incomplete, missing

def main():
    # args
    parser = argparse.ArgumentParser()
    parser.add_argument("exper",
                        help="Experiment code e.g. s006i",
                        type=str)
    parser.add_argument("telescope",
                        help="Telescope ID (i.e., cd, ke or yg)",
                        type=str)
    parser.add_argument("-t","--tol",
                        help="Print tolerance for missing data",
                        type=float,default=0.07)
    parser.add_argument("-r","--retransfer",
                        help="Print out command for retransfer",
                        action='store_true',default=False)
    args = parser.parse_args()
    # determine remote flexbuf
    rec = get_fb(args.telescope)
    # get local scans
    loc = get_local_scans(args.exper,args.telescope)
    # get remote scans
    rem = get_remote_scans(rec,args.exper,args.telescope)
    # compare the names and sizes of local/remote scans
    incomplete, missing = compare_scan_lists(rem,loc,args.tol)
    bad = incomplete + missing
    # define transfer port
    if args.retransfer==True:
        ports = {'cd':2637,'yg':2635,'ke':None}
        port  = ports[args.telescope]
        if True==True:
            print('')
            if port!=None:
                print('Command for (re-?)transfer:')
                array='{'+"".join( map( str,[ str(int(s.split('.')[0].split('_')[2].strip('no'))) +',' for s in bad] ))+'}'
                print('for i in {3:}; do m5copy vbs:///{0:}_{1:}_no0$(printf \'%03d\' $i)* file://131.217.172.183/mnt/rd1/AUSTRAL/{0:}{1:}/ --resume -udt -p {2:}; done'.format(args.exper,args.telescope,port,array))

if __name__=="__main__":
    main()
