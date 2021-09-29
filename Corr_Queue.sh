#!/bin/bash

# Usage Corr_Queue /tmp/joblist ./machines_odd/even
# Joblist should be generated with something like
# "ls /home/observer/correlations/aug030/aug030*im | cut -d '.' -f 1 > /tmp/joblist"

# 2020 Sep 29: Added new hostfile mapping option to mpirun with -mca. Gabor

while [ 1 ]; do 

if  [ $(cat $1 | wc -l) -gt 0 ] ; then
    nextjob=$(head -1 $1)
    cd ${nextjob%/*}
    NP=$(grep "ACTIVE DATA" $nextjob.input | cut -d ':' -f 2| tr -d ' ')
    rm -rf ${nextjob##*/}.difx
    #mpirun -np 47 -mca rmaps seq -machinefile $2 mpifxcorr ${nextjob##*/}.input
    #mpirun -np 41 -machinefile $2 mpifxcorr ${nextjob##*/}.input
    REQ_SPACK_ENV=spiralsdifx mpirun --tag-output --mca plm_rsh_agent /home/observer/ssh_wrapper --mca btl_tcp_if_include 131.217.63.0/24 --machinefile $2 --mca rmaps seq mpifxcorr ${nextjob##*/}.input

    echo
    sed -i "s/${nextjob//\//\\/}//g" $1
    # REmove empty lines. 
    sed -i '/^$/d' $1
    echo $nextjob >> $1.complete
else
    echo "The joblist ($1) is empty! Sleeping 30 seconds."
    sleep 30 
fi

done
