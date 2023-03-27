#!/bin/bash

for algo in "glouton" "progdyn" "approx"; do
    
    for n in {"5","10","15","20","25"}; do

        directory="./"
        filelist=$(find "$directory" -maxdepth 1 -type f -name "DP_N$n*" -print)
        declare -a times  # create an empty array to store execution times

        for file in $filelist; do
            
            # capture the execution time for each file and append it to the array
            time=$(python algo.py -a $algo -e $file -t)
            times+=($time)   
        done

        # calculate the mean execution time
        mean=$(echo "${times[@]}" | awk '{ total=0; for(i=1;i<=NF;i++) total+=$i; printf "%.5f\n", total/NF }')

        echo "Mean execution time: $mean ms for algo $algo size $n"
    done
   
done
