#!/bin/bash

cp $1.vex $1.vex.bak

n1=$(grep "\$MODE\;" $1.vex -n | cut -d ":" -f 1)
n2=$(grep "\$SOURCE\;" $1.vex -n | cut -d ":" -f 1)
n3=$(grep "\$FREQ\;" $1.vex -n | cut -d ":" -f 1)
n4=$(grep "\$SCHED\;" $1.vex -n | cut -d ":" -f 1)
nT=$(wc -l $1.vex | cut -d ' ' -f 1)

# mode upwards
head -$(expr $n1 - 1) $1.vex > $1.header

#isolate source section
head -$(expr $n4 - 1) $1.vex | tail -$(expr $n4 - $n2) > $1.sources
# isolate scans
tail -$(expr $nT - $n4 + 1) $1.vex > $1.sched

# put back together
cat $1.header > $1.vex.kludge
#echo "Using VDIF spirals 3 setups"
echo "Using VDIF spirals 4 setups"
cat ~/correlations2/corr_scripts/spirals4.setup >> $1.vex.kludge
cat $1.sources >> $1.vex.kludge
cat $1.sched >> $1.vex.kludge

sed -i "s/data_transfer/\*data_transfer/g" $1.vex.kludge


