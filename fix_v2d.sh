#!/bin/bash

# Help function
show_help() {
    echo "Usage: $0 exper [options]"
    echo ""
    echo " exper   Experiment name. i.e., exper.vex"
    echo ""
    echo "Options:"
    echo "  -h     Show this help message"
    # Add more options here
}

# Check if there are no arguments or if -h is provided
if [ $# -eq 0 ] || [ "$1" = "-h" ]; then
    show_help
    exit 0
fi

export v2dpath=/home/observer/correlations2/corr_scripts

# get start/stop times, year and DOY
export START=$(grep exper_nominal_start $1.vex | cut -d '=' -f 2 | tr -d ";")
export STOP=$(grep exper_nominal_stop $1.vex | cut -d '=' -f 2 | tr -d ";")

export YEAR=$(echo $START | cut -d 'y' -f 1)
export DOY=$(echo $START | cut -d 'y' -f 2 | cut -d 'd' -f 1)

#get template .v2d, in this case the spirals.v2d
cp $v2dpath/spirals.tv2d $1.kv2d

# replace variables in template v2d file (kludged-v2d)
sed -i "s/FAKESTART/$START/g" $1.kv2d
sed -i "s/FAKESTOP/$STOP/g" $1.kv2d
sed -i "s/FAKEVEX/$1/g" $1.kv2d

# get fringe finders
ffsources=$(grep source= $1.vex|cut -d ';' -f3|sort -u|grep "0537-441\|1921-293\|3C279\|3C273")
replace_str=$(echo "$ffsources" | sed 's/$/\\n/g' | tr -d '\n')
sed -i "s/source=FAKEFF/$replace_str/" $1.kv2d

# get source list
sources="$(grep source= $1.vex | cut -d';' -f3|sort -u|grep 'J\|G\|F')"
replace_str=$(echo "$sources" | sed 's/$/\\n/g' | tr -d '\n')
sed -i "s/source=FAKESOURCE/$replace_str/" $1.kv2d

antennas=$(grep station= $1.vex|cut -d':' -f1|cut -d'=' -f2|sort -u|tr '[:upper:]' '[:lower:]')
#antennas=("cd" "hb" "ke" "wa" "yg")

for s in ${antennas[@]}; do
   clock=`$v2dpath/influxdb_clocks.py $START $STOP -s $s -c`
   replace_str=$(echo "$clock" | sed 's/$/\\n/g' | tr -d '\n')
   sed -i "s/FAKECLOCKS_$s/`echo $replace_str`/" $1.kv2d
done

$v2dpath/eop.sh $YEAR $DOY >> $1.kv2d
