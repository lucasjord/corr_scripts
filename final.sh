#!/bin/bash
#syntax ./bulk.sh exp
# Written by Lucas J. Hyland March 2019
#echo 'Remember to run vex2difx $1.v2d first'
vex2difx $1.v2d
sleep 1
rm *.im
calcif2 -a
sleep 1
ls /home/observer/correlations2/$1/$1*.im | cut -d '.' -f 1 > ./$1.joblist
sleep 1
/home/observer/correlations2/corr_scripts/Corr_Queue.sh ./$1.joblist ./machines
