#!/bin/bash

while getopts "a:e:pt" opt; do
    case $opt in 
        e)  PATH_EXAMPLE="$OPTARG"
            ;;    
        p|t)
            RESULT+="-$opt "
            ;; 
        \?)
            echo "invalide option"             
        esac
done  
if [[ -z "$ALGO" || -z "$PATH_EXAMPLE" ]]; then
  echo " -e CHEMIN_EXEMPLAIRE [-p] [-t] "   
fi

python algo_v3.py -e $PATH_EXAMPLE $RESULT


        