#!/bin/bash
# Shell script for automatically
# reversing the line order of a csv file
# but keeping the header up top
# @param $1 file to reverse line order. note: must be a delimited file (ie: .csv) with headers
# @author Woo Jung
# @version 10/2/18

# the file to reverse
file=$1

# name of reversed file
r_name="reversed_$1"

# take the headers and and store it
headers=$(head -1 $1)

# save headers to new file
echo "$headers" > $r_name

# don't leave me hanging
echo "Reversing ordering for file: $file"
sleep .5
echo -n .
sleep .5
echo -n .

# take the rest of the data excluding headers to temp file xd.txt
tail -n +2 $1 > xd.txt

sleep .4
echo -n .

# reverse print
tac xd.txt >> $r_name

sleep .3
echo -n .

# remove temp file xd.txt
rm xd.txt

sleep .2
echo "done!!"


echo "New file: $r_name"
