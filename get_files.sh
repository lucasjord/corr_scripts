#!/bin/bash

scp observer@newsmerd:/vlbobs/lba/$1/$1.vex ./
scp oper@hobart:/usr2/log/$1'ho.log' ./
scp oper@pcfshb:/usr2/log/$1'hb.log' ./
scp oper@pcfske:/usr2/log/$1'ke.log' ./
scp oper@pcfsyg:/usr2/log/$1'yg.log' ./
scp oper@pcfscd:/usr2/log/$1'cd.log' ./

