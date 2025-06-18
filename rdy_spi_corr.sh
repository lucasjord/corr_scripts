#!/bin/bash

#resetcor
mkdir -p cont
cp cd.filelist cont/
cp hb?.filelist cont/
cp ho.filelist cont/
cp ke?.filelist cont/
cp wa.filelist cont/
cp yg?.filelist cont/
cp $1.vex.kludge cont/
cp $1.v2d cont/
cp $1.kv2d cont/$1.v2d
sed -i "s/singleScan/\#singleScan/g" cont/$1.v2d

rm -r geo
rm -r line
cp -r cont/ geo/
cp -r cont/ line/
