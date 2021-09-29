#!/bin/bash
# Correlate single fringe check scan with corq. Makes and cleanes up auxiliary files.
# $1: Experiment, $2: scan number
# Example run: fringe-check.sh s001a no0001

ssh observer@flexbuflke << EOF
    vsum -s /mnt/disk1/fringe/$1_cd_$2-slice > /home/observer/correlations2/$1/cd.filelist
    vsum -s /mnt/disk1/fringe/$1_ke_$2_c*-slice > /home/observer/correlations2/$1/keX.filelist
    vsum -s /mnt/disk1/fringe/$1_ke_$2_d*-slice > /home/observer/correlations2/$1/keY.filelist
    fusermount -u /mnt/ljh
    vbs_fs -I $1_hb* /mnt/ljh
    vsum -s /mnt/ljh/$1_hb_$2_c* > /home/observer/correlations2/$1/hbX.filelist
    vsum -s /mnt/ljh/$1_hb_$2_d* > /home/observer/correlations2/$1/hbY.filelist
    vsum -s /mnt/rd1/AUSTRAL/$1wa/$1_wa_$2*.vdif > /home/observer/correlations2/$1/wa.filelist
EOF

echo "Filelists created."

rm *.flag
rm *.calc
rm *.im
rm *.input
rm *.joblist
rm -r *.difx
vex2difx $1.v2d
calcif2 -a
corq submit $1_1 -p 9999 --description 'Fringe Check'
#difx2mark4 -d

echo "After finished,  do 'difx2mark4 -d, then plot file with fourfit -tx (-b ..) 1234/scan/ set pc_mode manual. Antennas in -b: L Hobart, i Katherine, c Ceduna, w Warkworth."
