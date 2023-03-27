#!/bin/bash

for algo in  "glouton" "approx"  ; do
    
    for n in {"1000","5000","10000","50000"}; do

        directory="./"
        filelist=$(find "$directory" -maxdepth 1 -type f -name "N${n}_0" -print)
        total_time=0  # create an empty array to store execution times

        for file in $filelist; do
            
            # capture the execution time for each file and add it to the total time
            time=$(python algo.py -a $algo -e $file -t)
            total_time=$(echo "$total_time + $time" | bc)
        done

        # calculate the mean execution time for this file list
        num_files=$(echo "$filelist" | wc -w)
        mean=$(echo "$total_time / $num_files" | bc -l)

        echo "Mean time is: $mean ms for algo $algo size $n"
    done
   
done
