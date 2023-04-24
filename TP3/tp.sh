#!/bin/bash

while getopts "e:p" opt; do
    case $opt in 
        e)  PATH_EXAMPLE="$OPTARG"
            ;;    
        p)
            OPTION="-$opt"
            ;; 
        \?)
            echo "invalide option"             
        esac
done  


if [ -z "$PATH_EXAMPLE" ]; then
  echo " -e CHEMIN_EXEMPLAIRE [-p] "  
else 
    python algo_v3.py -e $PATH_EXAMPLE $OPTION
fi




        