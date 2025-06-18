#!/bin/bash 

uniq cd.filelist > cd.tmp
mv cd.tmp cd.filelist
uniq wa.filelist > wa.tmp
mv wa.tmp wa.filelist
grep _d hb.filelist|sort -u > hbX.filelist
grep _e hb.filelist|sort -u > hbY.filelist
grep _e ke.filelist|sort -u > keX.filelist
grep _f ke.filelist|sort -u > keY.filelist
grep _e yg.filelist|sort -u > ygX.filelist
grep _f yg.filelist|sort -u > ygY.filelist
