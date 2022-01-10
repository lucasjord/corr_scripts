#!/usr/bin/python3
#Runs fourfit on correlated scans and outputs single-band delays and
#their epochs for given baselines.

# Originally composed by Dr. Gabor Orosz in bash/shell

# edited L.J. Hyland Feb 2020 for python3 and to include Ke, Hb and Wa as well as polarisation

import numpy as np, sys, os, subprocess, pdb
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

def linear_model(p,t):
    return p[0]*t+p[1]

def linear_model_res(p,t,y):
    return (y - linear_model(p,t))

N = len(sys.argv[1:])
if N==0:sys.exit("Specify experiment code, reference antenna polarisation and baselines.\n\
        Usage: ./clockfit.sh exper ref pol base1 base2 ... baseN\n\
        Antenna codes: Hobart26=H, Hobart12=L, Katherine=i, Yarragadee=e, Ceduna=c, Warkworth30=w\n\
        Polarisations: R or L \n\
        Example: clockfit.sh mv024 e R i H")
elif N==1:sys.exit("Specify experiment code, reference antenna and baseline.\n\
        Run clockfit.sh without arguments to see more help.")
elif N<=2:sys.exit("No polarisations specified.\n\
        Run clockfit.sh without arguments to see more help.")
elif N<=3:sys.exit("No baselines specified.\n\
        Run clockfit.sh without arguments to see more help.")

exper = sys.argv[1]
ref   = sys.argv[2]
pol   = sys.argv[3]
bl    = sys.argv[4:]
path  = '/home/observer/correlations2/{}/1234/'.format(exper)
if not os.path.exists(path): sys.exit('{} does not exist, did you run difx2mark4?'.format(path))
if not pol in ('R','L'): sys.exit('Polarisation must be either R or L, you had {}'.format(pol))

for b in bl:
    os.system('fourfit -t -b {0:} -m 0 -P {1:}{1:} {2:}No* set pc_mode manual > \
        temp.txt 2>&1'.format("".join(sorted(ref+b,key=str.casefold)),pol,path))
    try:
        p = subprocess.Popen('grep single temp.txt | cut -d ":" -f 3',shell=True,
             stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        delay = np.asarray(p.stdout.read().split(),float)
        p = subprocess.Popen('grep -A 160 single temp.txt | grep adjusted | cut -d " " -f 9',shell=True, 
       	    stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        epoch = np.asarray(p.stdout.read().split(),float)
    	#pdb.set_trace()
        model = least_squares(linear_model_res,[1,1],args=(epoch,delay),loss='cauchy')
    except ValueError:
        p = subprocess.Popen('grep adjusted temp.txt | cut -d " " -f 9',shell=True, 
       	     stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        epoch = np.asarray(p.stdout.read().split(),float)
        model = least_squares(linear_model_res,[1,1],args=(epoch,delay),loss='cauchy')
    print('Baseline {0:} with pol {1:}{1:} rate={2:>+10.4E} us/s'.format("".join(sorted(ref+b,key=str.casefold)),pol,model.x[0]))
    delay_m = epoch*model.x[0] + model.x[1]
    plt.close(1)
    fig = plt.figure(1,figsize=(5,10))
    ax1 = fig.add_subplot(211)
    ax1.plot(epoch,1000*delay,'k--.',lw=0.75)
    ax1.plot(epoch,1000*delay_m,'r-')
    ax1.set_xlabel('')
    ax1.set_ylim(np.percentile(delay,50)*1000-50,np.percentile(delay,50)*1000+50)
    ax1.set_ylabel('Delay (ns)')
    ax2 = fig.add_subplot(212)
    ax2.plot(epoch,1000*(delay-delay_m),'b--.')
    ax2.set_ylim(-25,25)
    ax2.set_xlabel('MJ Time (s)')
    ax2.set_ylabel('Delay residuals (ns)')
    fig.savefig('{0:}../clocks{1:}{2:}{2:}.pdf'.format(path,"".join(sorted(ref+b,key=str.casefold)),pol),bbox_inches='tight')

os.remove('temp.txt')

