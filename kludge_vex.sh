#!/bin/bash

cp $1.vex $1.vex.bak

n1=$(grep "\$MODE\;" $1.vex -n | cut -d ":" -f 1)
head -$(expr $n1 - 1) $1.vex > $1.header

n2=$(grep "\$SOURCE\;" $1.vex -n | cut -d ":" -f 1)
n3=$(grep "\$FREQ\;" $1.vex -n | cut -d ":" -f 1)
nT=$(wc -l $1.vex | cut -d ' ' -f 1)

head -$(expr $n3 - 1) $1.vex | tail -$(expr $n3 - $n2) > $1.sources
n4=$(grep "\$SCHED\;" $1.vex -n | cut -d ":" -f 1)
tail -$(expr $nT - $n4 + 1) $1.vex > $1.sched

cat $1.header > $1.vex.kludge
echo "Using VDIF setups"
cat ~/correlations2/corr_scripts/spirals.setup >> $1.vex.kludge
cat $1.sources >> $1.vex.kludge
cat $1.sched >> $1.vex.kludge

sed -i "s/data_transfer/\*data_transfer/g" $1.vex.kludge


