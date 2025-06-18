#!/bin/env python3

'''
Script to get clock delays for a telescope over a certain time range from the influxdb
server running on frenkie 131.217.63.192, then fit with a linear model.

Probably will also do some outlier detection. Clock
jump detection might be difficult but I might try.

@Author Lucas Jordan Hyland
@Date 2024/02/27

basic values for the clock are:
station        rate (us/s)     offset (us)
ceduna     -3.83956759e-07 -4.95655224e+01
hobart     -4.24353389e-07 -1.36353416e+01
katherine  -3.73041856e-07 -1.30434082e+01
warkworh   -1.07250792e-06 -1.96171957e+01 !! Stuart retuned
yarragadee -2.13683580e-07 -8.35637799e+00

Added plotting: 17/12/2024

'''

import os, numpy as np, argparse, datetime, time, pdb
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

# lets first establish some global dictionaries
bucket = 'utas'
url    = '131.217.63.194:8086/api/v2/query'
# name of mesurement
measurement = {'cd':'clockdelays',
               'hb':'clockdelays',
               'ho':'clockdelays',
               'ke':'clockdelays',
               'wa':'wark30m',
               'yg':'clockdelays'}
# name of field
field  = {'cd':'fmout2gps',
          'hb':'dbbc3hb2gps',
          'ho':'dbbc2ho2gps',
          'ke':'fmout2gps',
          'wa':'gps_fmout',
          'yg':'fmout2gps'}
# any tags
tag    = {'cd':' and r.station == \"cd\"',
          'hb':' and r.station == \"hb\"',
          'ho':' and r.station == \"hb\"',
          'ke':' and r.station == \"ke\"',
          'wa':'',
          'yg':' and r.station == \"yg\"'}
# the scale of the clkoffs
scale  = {'cd':-1,
          'hb':-1,
          'ho':-1,
          'ke':-1,
          'wa':-1000000,
          'yg':-1}
# define some defaults if it does not work (or if you CBS)
# index 0 is rate in us/s and index 1 is delay in us
defaults = {'cd':[-5.9718e-07, -58.8155],
            'hb':[-5.6974e-07, -24.3217],
            'ho':[-5.6974e-07, -24.3217],
            'ke':[-3.730e-07, -14.30],
            #'wa':[-1.072e-06, -19.61],
            'wa':[-4.2921e-08, -16.1357],
            'yg':[-4.1813e-07,  -5.1364]}

# 31/01/2024 @ 14:00 UT
#default_unix = 1706670000

# 2024y252d03h00m00s aka 8/09/24 @ 03:00 UT
default_unix = 1725764400

def linear_model(p,x,x0):
    '''Simple linear model nothing fancy'''
    return p[0]*(x-x0) + p[1]


def res_lm(p,x,x0,y):
    '''Returns the difference between linear model and y'''
    return (y - linear_model(p,x,x0))


def YjHMS_to_YmdHMS(yjhms):
    ''' convert input YYYYyDDDdHHhMMmSSs format to YYYY-mm-ddTHH:MM:SSZ'''
    dt = datetime.datetime.strptime(yjhms,'%Yy%jd%Hh%Mm%Ss')
    return datetime.datetime.strftime(dt,'%Y-%m-%dT%H:%M:%SZ')


def calc_mid(istart,istop):
    dt1 = datetime.datetime.strptime(istart,'%Yy%jd%Hh%Mm%Ss')
    dt2 = datetime.datetime.strptime(istop,'%Yy%jd%Hh%Mm%Ss')
    dtm = datetime.datetime.strftime(dt1 + (dt2 - dt1)/2,'%Yy%jd%Hh%Mm%Ss')
    return dtm


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('start',
                        help='Start UT  YYYYyDDDdHHhMMmSSs',type=str)
    parser.add_argument('stop',
                        help='Stop UT',type=str)
    parser.add_argument('-s','--stations',nargs='+',required='True',
    	                 help='Space-separated list of telescopes to get clocks for i.e., cd hb ho ke wa yg')
    parser.add_argument('-f','--fit',action='store_true',default=False
                            ,help='Fit clock and rate, else will extrapolate from standard values. Good if clocks have been retuned.')
    parser.add_argument('-c','--clock',action='store_true',default=False
                            ,help='Only return fitted clock, use default rate')
    parser.add_argument('-p','--plot',action='store_true',default=False
                            ,help='Plot data and fit for each station')
    args = parser.parse_args()

    # re-format some times
    start_hms = YjHMS_to_YmdHMS(args.start)
    stop_hms  = YjHMS_to_YmdHMS(args.stop)
    mid_yjhms = calc_mid(args.start,args.stop)
    mid_u     = time.mktime(datetime.datetime.strptime(mid_yjhms,'%Yy%jd%Hh%Mm%Ss').timetuple())
    # loop over input stations
    for station in args.stations:
        print('#{}'.format(station))
        # fit or extrapolate?
        if args.clock==True:
            try:
                data = get_clocks(start_hms,stop_hms,station)
                foo, delay = fit_data(station,data,mid_u,args)
                rate = defaults[station][0]
            except IndexError:
                print('# IndexError in clocks for '+ station)
                delay,rate = extrapolate_clocks(station,mid_u)
        elif args.fit==True:
            try:
                data = get_clocks(start_hms,stop_hms,station)
                rate, delay = fit_data(station,data,mid_u,args)
            except IndexError:
                print('# IndexError in fit for '+ station)
                delay,rate = extrapolate_clocks(station,mid_u)
        else:
            delay,rate = extrapolate_clocks(station,mid_u)
        print(f' clockOffset = {delay:2.4f}')
        print(f' clockRate   = {rate:2.4e}')
        print(f' clockEpoch  = {mid_yjhms:s}')

def extrapolate_clocks(station,mid_u):
    dela  = defaults[station][0]*(mid_u - default_unix) + defaults[station][1]
    return dela,defaults[station][0]

def get_clocks(start,stop,station):
    '''Query influxdb for clocks'''
    # construct command string
    cmd = f"curl -XPOST {url:} -sS "\
          "-H 'Accept:application/csv' -H 'Content-type:application/vnd.flux' -d "
    # construct specific query
    query =f"'from(bucket:\"{bucket:}\") |> range(start:{start:},stop:{stop:})"\
           f" |> filter(fn:(r) => r._measurement == \"{measurement[station]:}\" and"\
           f" r._field == \"{field[station]:}\"{tag[station]:})'"
    # send query and get result
    stdout = os.popen(cmd + query).read().split('\n')
    return stdout


def fit_data(station,stdout,u0,args):
    # reformat and drop unimportant stuff (keeping time and delay)
    data   = np.array([np.array(s.split(','))[(5,6),] for s in stdout[4:-2]])

    # construct time array(s), 1 datetime and 1 unix time stamp
    dt,unix=[],[]
    for s in data[:,0]:
        dt  += [datetime.datetime.fromisoformat(s[:-1])]
        unix+= [time.mktime(dt[-1].timetuple())]

    # get clocks
    # all clock values are flipped relative to standard
    u      = np.array(unix)
    dela   = data[:,1].astype(float)*scale[station]
    # flag obvious outliers
    indx = abs(dela)<300 #= np.percentile(dela,50)
    #pdb.set_trace()
    # fit linear regression to clock values, first attempt
    lsq1 = least_squares(res_lm,[1,np.percentile(dela[indx],50)],args=(u[indx],u0,dela[indx]),loss='huber')
    R1   = linear_model(lsq1.x,u,u0) - dela
    indx = indx*(abs(R1)<10)
    # fit w/o bad residuals
    lsq2 = least_squares(res_lm,lsq1.x,args=(u[indx],u0,dela[indx]),loss='huber')
    R2   = linear_model(lsq1.x,u,u0) - dela
    indx = indx*(abs(R2)<2)
    #
    lsq = least_squares(res_lm,lsq2.x,args=(u[indx],u0,dela[indx]),loss='huber')

    if args.plot==True:
        # get model
        M = linear_model(lsq.x,u[(0,-1),],u0)
        fig, ax = plt.subplots(1,figsize=(7,7))
        ax.plot(u,dela,'k.')
        ax.plot(u[(0,-1),],M,'r')
        ax.set_ylim(min(M)-2,max(M)+2)
        ax.set_title('{:0}_{:1}_{:2}'.format(station,args.start,args.stop))
        fig.savefig('./clocks_{:0}_{:1}_{:2}.pdf'.format(station,args.start,args.stop))
    # return fit
    return lsq.x


###############################################################

if __name__=='__main__':
	main()

###############################################################
