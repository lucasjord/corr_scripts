#!/bin/bash

# Usage Corr_Queue /tmp/joblist ./machines_odd/even
# Joblist should be generated with something like
# "ls /home/observer/correlations/aug030/aug030*im | cut -d '.' -f 1 > /tmp/joblist"
craig=1
while [ $craig == 1 ]; do 

if  [ $(cat $1 | wc -l) -gt 0 ] ; then
    nextjob=$(head -1 $1)
    cd ${nextjob%/*}
    NP=$(grep "ACTIVE DATA" $nextjob.input | cut -d ':' -f 2| tr -d ' ')
    rm -rf ${nextjob##*/}.difx 
    mpirun -np 26 -machinefile $2 /home/observer/DiFX-2.6.1/bin/mpifxcorr ${nextjob##*/}.input
    echo
    sed -i "s/${nextjob//\//\\/}//g" $1
    # REmove empty lines. 
    sed -i '/^$/d' $1
    echo $nextjob >> $1.complete
else
    craig=0
fi

done
