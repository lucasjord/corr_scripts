#!/bin/bash
#Runs fourfit on correlated scans and outputs single-band delays and 
#their epochs for given baselines.

# Originally composed by Dr. Gabor Orosz

N=$#

if [ $# -eq 0 ]; then
    echo -e "Specify experiment code, reference antenna and baselines.\nUsage: ./clockfit.sh exper ref base1 base2 base3\nWhere exper=experiment code, ref=reference antenna, base#=baselines.\nAntenna codes: Hobart26=H, Katherine=i, Yarragadee=e, Ceduna=c\nExample: clockfit.sh mv024 e i H"
    exit
elif [ $# -eq 1 ]; then
    echo -e "Specify experiment code, reference antenna and baseline.\nRun clockfit.sh without arguments to see more help."
    exit
elif [ $# -eq 2 ]; then
    echo -e "No baselines specified.\nRun clockfit.sh without arguments to see more help. "
    exit
elif [ $# -eq 3 ]; then
cd ~/correlations2/$1/1234/
fourfit -t -b $3$2 -m 0 No* set pc_mode manual &> temp1.txt
elif [ $# -eq 4 ]; then
cd ~/correlations2/$1/1234/
fourfit -t -b $3$2 -m 0 No* set pc_mode manual &> temp1.txt
fourfit -t -b $4$2 -m 0 No* set pc_mode manual &> temp2.txt
cat temp2.txt >> temp1.txt
elif [ $# -eq 5 ]; then
cd ~/correlations2/$1/1234/
fourfit -t -b $3$2 -m 0 No* set pc_mode manual &> temp1.txt
fourfit -t -b $4$2 -m 0 No* set pc_mode manual &> temp2.txt
fourfit -t -b $5$2 -m 0 No* set pc_mode manual &> temp3.txt
cat temp2.txt >> temp1.txt
cat temp3.txt >> temp1.txt
else
    echo -e "Only supports Ho, Cd, Ke, Yg at the moment."
    exit
fi

grep 'Organizing' temp1.txt > sel1.txt
grep 'Baseline' temp1.txt > sel2.txt
grep 'ref. epoch' temp1.txt > sel3.txt
grep 'single band delay' temp1.txt > sel4.txt
awk 'NF>1{print $NF}' sel1.txt > col1.txt
awk '{print $3}' sel2.txt > col2.txt
awk 'NF>1{print $NF}' sel3.txt > col3.txt
awk 'NF>1{print $NF}' sel4.txt > col4.txt

echo -e 'Scan\tBase\tEpoch(MJD/sec)\tSBD(usec)' > delays.txt
paste col1.txt col2.txt col3.txt col4.txt >> delays.txt

rm temp*.txt && rm sel*.txt && rm col*.txt

