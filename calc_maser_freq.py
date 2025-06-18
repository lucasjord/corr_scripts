#!/usr/bin/env python3

'''
Script to determine maser velocity shift due to Annual motion (~30km/s).
Does not take into account diural shift (~0.5km/s) or leap-years.

Good for helping determine rough maser velo at a particular day or experiment zoom bands.

@Author Lucas J. Hyland
@Date 11th April 2024
'''

import numpy as np, argparse
import astropy.units as u, astropy.time as aTime
from astropy.coordinates import SkyCoord
from datetime import datetime
from pyvexfile import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-V','--vex',default=None,type=str,
                         help='Input Vex file to figure out parms')
    parser.add_argument('-t','--time',default=datetime.now().strftime('%Yy%jd%Hh%Mm%Ss'),
                         help='Time at which to calculate, YYYYyDDDdHHhMMmSSs')
    parser.add_argument('-p','--position',type=str,
                         help='-p RA,DEC. Format HH:MM:SS DD:MM:SS')
    parser.add_argument('-f','--restfreq',
                         help='Rest frequency of spectral line',
                         default=6668.518,type=float)
    parser.add_argument('-l','--lsr',default=0.0,
                         help='Source velocity (if known)',type=float)
    parser.add_argument('-s','--source',
                         help='Specific source',type=str)
    args = parser.parse_args()
    maser = ''
    # if specifc sources, then use those and NOW
    if args.source!=None:
        time = args.time
        if args.source=='g009':
            maser = 'G009.621+0.196'
            sc = SkyCoord('18h06m14.67s -20d31m32.4s')
            velo = 1.3
        elif args.source=='g188':
            maser = 'G188.946+0.886'
            sc = SkyCoord('06h08m53.32s 21d38m29.1s')
            velo = 10.8
        elif args.source=='g323':
            maser = 'G323.740-0.263'
            sc = SkyCoord('15h31m45.45s -56d30m50.1s')
            velo = -50.5
        else: sys.exit('Only g009, g188 and g323 supported')
    elif args.vex!=None:
        # if vex is specified, overrule time, maser and position
        sc, velo, time, maser = parseVex(args)
    else:
        if args.position==None:
            sys.exit('Must specify Vex OR position')
        pos = args.position.split(',')
        sc = SkyCoord(ra=pos[0],dec=pos[1],unit=(u.hourangle,u.deg))
        time = args.time
        velo = args.lsr
    # convert time to fyear
    print(f"# Parms for {time:s} {maser:s}")
    print(f'# at position {sc.to_string("hmsdms"):s}')
    fyear  = time_to_fyr(time)
    # get annual LSR velocity
    v_alsr = radec_to_velo(sc,fyear)
    print(f'# Earth orbital+Sun LSR velocity {v_alsr:+5.2f} km/s')
    # calculate velocity difference
    dv     = -v_alsr-velo
    print(f'# LSR {velo:>+5.2f} km/s')
    #print(f'# Velocity difference {dv:>+5.2f} km/s')
    # calculate Doppler shift
    dnu    = args.restfreq*dv/(299798.458)
    print(f'# Rest frequency {args.restfreq:>10.4f} MHz')
    print(f'# Sky frequency {args.restfreq+dnu:>10.4f} MHz')
    calculate_zoom(args.restfreq+dnu)

def calculate_zoom(freq):
    '''For some reason zooms appear to have to be intervals of 0.25'''
    points = np.array([0,0.25,0.5,0.75])
    rem    = freq%1
    zfreq = freq - rem + points[abs(points - rem).argmin()]
    print(f'# 4MHz zoom start {zfreq-2.0:>8.2f}')

def parseVex(args):
    '''
    Open vexfile, parse with Benito's vex file reader (https://github.com/bmarcote/vex)
    assume maser starts with G to determine RA/DEC
    get velocity if it was specified in key
    get start time of experiment
    '''
    vex = Vex(args.vex)
    vex.from_file(args.vex)
    maser = [s for s in vex['SOURCE'] if "G" in s][0]
    try:
        lsr = [vex['SOURCE'][maser][s].value for s in vex['SOURCE'][maser].keys() if 'LSR' in vex['SOURCE'][maser][s].value]
        velo= float(lsr[0].split()[2])
    except (ValueError,KeyError,IndexError) as e:
        velo = args.lsr
    ra2000 = vex['SOURCE'][maser]['ra'].value.split()[0].strip(';')
    dc2000 = vex['SOURCE'][maser]['ra'].value.split()[3].strip(';')
    sc = SkyCoord(ra=ra2000,dec=dc2000)
    exper = vex['GLOBAL']['EXPER'].value
    start = vex['EXPER'][exper]['exper_nominal_start'].value
    return sc, velo, start, maser

def time_to_fyr(time_yjhms):
    return datetime.strptime(time_yjhms,'%Yy%jd%Hh%Mm%Ss').timetuple().tm_yday/365.

def radec_to_velo(sc,t):
    # velocity of Sun (20km/s towards ra=270,dec=30 deg) projected on source ra,dec
    vr_sun = 20*(np.cos(270/57.3)*np.cos(30/57.3)*np.cos(sc.ra.radian)*np.cos(sc.dec.radian)
               + np.sin(270/57.3)*np.cos(30/57.3)*np.sin(sc.ra.radian)*np.cos(sc.dec.radian)
               + np.sin(30/57.3)*np.sin(sc.dec.radian))
    # velocity of Earth towards Sun, projected towards source
    # velo is 30km/s around Sun. Sun lat is 0 at March Equinox (t=0.2179 yrs)
    vr_e   = 30*np.cos(sc.geocentricmeanecliptic.lat.radian)*np.sin(2*np.pi*(t-0.2179)-sc.geocentricmeanecliptic.lon.radian)
    return -(vr_sun+vr_e)

if __name__=='__main__':
    main()

