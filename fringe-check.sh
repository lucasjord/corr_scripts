#!/bin/bash
# Correlate single fringe check scan with corq. Makes and cleanes up auxiliary files.
# $1: Experiment, $2: scan number
# Example run: fringe-check.sh s001a no0001

ssh observer@flexbuflke << EOF
    vsum -s /mnt/rd1/AUSTRAL/$1cd/$1_cd_$2* > /home/observer/correlations2/$1/cd.filelist
    #vsum -s /mnt/disk1/fringe/$1_cd_$2* >> /home/observer/correlations2/$1/cd.filelist
#
#    vsum -s /mnt/disk1/fringe/$1_hb_$2_d* > /home/observer/correlations2/$1/hbX.filelist
#    vsum -s /mnt/disk1/fringe/$1_hb_$2_e* > /home/observer/correlations2/$1/hbY.filelist
    vsum -s /mnt/disk1/fringe/$1_hb_$2_*d* > /home/observer/correlations2/$1/hbX.filelist
    vsum -s /mnt/disk1/fringe/$1_hb_$2_*e* > /home/observer/correlations2/$1/hbY.filelist
#
    vsum -s /mnt/disk1/fringe/$1_ke_$2_*e* > /home/observer/correlations2/$1/keX.filelist
    vsum -s /mnt/disk1/fringe/$1_ke_$2_*f* > /home/observer/correlations2/$1/keY.filelist
#
#    vsum -s /mnt/disk1/fringe/$1_yg_$2_e* > /home/observer/correlations2/$1/ygX.filelist
#    vsum -s /mnt/disk1/fringe/$1_yg_$2_f* > /home/observer/correlations2/$1/ygY.filelist
#    vsum -s /mnt/rd1/AUSTRAL/$1yg/$1_yg_$2_x* > /home/observer/correlations2/$1/ygX.filelist
#    vsum -s /mnt/rd1/AUSTRAL/$1yg/$1_yg_$2_y* > /home/observer/correlations2/$1/ygY.filelist
    vsum -s /mnt/rd1/AUSTRAL/$1yg/$1_yg_$2_*x* > /home/observer/correlations2/$1/ygX.filelist
    vsum -s /mnt/rd1/AUSTRAL/$1yg/$1_yg_$2_*y* > /home/observer/correlations2/$1/ygY.filelist
#    fusermount -u /mnt/corlke/fringe/
#    vbs_fs -I $1_ho* /mnt/corlke/fringe/
#    vsum -s /mnt/corlke/fringe/$1_ho_$2* > /home/observer/correlations2/$1/ho.filelist
#    vsum -s /mnt/ljh/$1_hb_$2_e > /home/observer/correlations2/$1/hbX.filelist
#    vsum -s /mnt/ljh/$1_hb_$2_f > /home/observer/correlations2/$1/hbY.filelist
    vsum -s /mnt/rd1/AUSTRAL/$1wa/$1_wa_$2.vdif > /home/observer/correlations2/$1/wa.filelist
EOF

echo "Filelists created."

rm *.flag
rm *.calc
rm *.im
rm *.input
rm *.joblist
rm -r *.difx
rm ~/baseline_*
mkdir -p fringe
rm fringe/baseline_*

#awk -F' ' '{ printf "mjdStart=%10.9f\nmjdStop =%10.9f\n", $2,$3}' cd.filelist >>  $.v2d

#vex2difx $1.v2d && calcif2 -a && genmachines *.input && corq submit $1_1 -p 9999 --description 'Fringe Check'
vex2difx $1.v2d && difxcalc *.calc && genmachines *.input && corq submit $1_1 -p 9999 --description 'Fringe Check'


