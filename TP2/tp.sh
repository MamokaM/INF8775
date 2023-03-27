#!/bin/bash

while getopts "a:e:pt" opt; do
    case $opt in 
        a)
            ALGO="$OPTARG"
            ;;
        e)  PATH="$OPTARG"
            ;;    
        p|t)
            RESULT+="-$opt "
            ;; 
        \?)
            echo "invalide option"             
        esac
done  
if [[ -z "$ALGO" || -z "$PATH" ]]; then
  echo " $0 -a {glouton, progdyn, approx} -e CHEMIN_EXEMPLAIRE [-p] [-t] "   
fi

python algo.py -a $ALGO -e $PATH $RESULT


        


