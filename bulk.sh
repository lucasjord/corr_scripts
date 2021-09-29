#!/bin/bash
#syntax ./bulk.sh exp
# Written by Lucas J. Hyland March 2019
#echo 'Remember to run vex2difx $1.v2d first'
vex2difx $1.v2d
sleep 1
rm $1*.im
rm -r *.difx
grep "SOURCE 0 NAME" *.calc | grep F > fringe.txt
calcif2 $(cat fringe.txt | cut -d ':' -f 1)
sleep 1
ls /home/observer/correlations/$1/$1*.im | cut -d '.' -f 1 > ./$1.joblist
sleep 1
~/correlations/corr_scripts/Corr_Queue.sh ./$1.joblist ./machines

sleep 1
cp -r 1234 old_1234
rm -r 1234
difx2mark4 *difx
