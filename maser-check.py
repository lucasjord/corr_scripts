#!/usr/bin/bash
# $1: Experiment, $2: scan number
# Example run: maser-check.sh s001a no0001

# Ceduna
ssh observer@flexbuffcd << EOF
    fusermount -u /mnt/ljh
    vbs_fs -I $1_cd* /mnt/ljh
    rm /home/observer/cd.tspec
    /usr/local/bin/m5spec -nopol /mnt/ljh/$1_cd_$2 vdif_8000-1024-4-2 8192 100000 /home/observer/cd.tspec && scp /home/observer/cd.tspec observer@hex6.phys.utas.edu.au:/home/observer/correlations2/$1/
EOF

#Warkworth
ssh observer@flexbuflke << EOF
    rm /home/observer/wa.tspec
    m5spec -nopol /mnt/rd1/AUSTRAL/$1wa/$1_wa_$2* vdif_8000-1024-4-2 8192 100000 /home/observer/correlations2/$1/wa.tspec
EOF

#Katherine
#ssh observer@flexbuffke << EOF
#    fusermount -u /mnt/ljh
#    vbs_fs -I $1_ke* /mnt/ljh
#    rm /home/observer/ke*.tspec
#    m5spec -nopol /mnt/ljh/$1_ke_$2_c vdif_8000-512-4-2 4096 100000 /home/observer/keY.tspec
#    m5spec -nopol /mnt/ljh/$1_ke_$2_d vdif_8000-512-4-2 4096 100000 /home/observer/keX.tspec
#    scp /home/observer/ke*.tspec observer@hex6.phys.utas.edu.au:/home/observer/correlations2/$1/
#EOF

#Hobart
#ssh observer@flexbuflke << EOF
#    fusermount -u /mnt/ljh
#    vbs_fs -I $1_hb* /mnt/ljh
#    rm /home/observer/hb*.tspec
#    m5spec -nopol /mnt/ljh/$1_hb_$2_e vdif_8000-512-4-2 4096 100000 /home/observer/correlations2/$1/hbX.tspec
#    m5spec -nopol /mnt/ljh/$1_hb_$2_f vdif_8000-512-4-2 4096 100000 /home/observer/correlations2/$1/hbY.tspec
#EOF

cd /home/observer/correlations2/$1/ && ../corr_scripts/maser-plot.m

