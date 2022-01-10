#!/bin/bash

# usage exper_search.sh $exper $ant

if [[ -z $2 ]]; then 
	echo "No experiment specified"
	exit
fi

echo "$1$2"

ssh observer@flexbuflke << EOF
    echo "Checking raids"
    FILE=/mnt/rd1/AUSTRAL/$1$2
    if [ -d "$FILE" ]; then
        echo "$FILE exists"
    	du -h $FILE
    fi
    FILE=/mnt/rdsi/AUSTRAL/$1$2
    if [ -d "$FILE" ]; then
        echo "$FILE exists"
        du -h $FILE
    fi
    echo "Checking flexbuflke VBS"
	vbs_ls -lrthT "$1_$2*"
EOF

ssh flexbuflcd << EOF
	echo "Checking flexbuflcd VBS"
    vbs_ls -lrthT "$1_$2*"
EOF
