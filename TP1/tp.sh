#!/bin/bash

while getopts "a:e:1:2:pt" opt; do
    case $opt in 
        a)
            ALGO="$OPTARG"
            ;;
        e)
            case $OPTARG in
            1)
                PATH1="$4"
                shift
                ;;
            2)
                PATH2="$5"
                shift
                ;;
            esac
            ;;    
        p|t)
            RESULT+="-$opt "
            
            ;; 
        \?)
            echo "invalide option"             
        esac
done  
if [[ -z "$ALGO" || -z "$PATH1" || -z "$PATH2" ]]; then
  echo " $0 -a {conv, strassen, strassenSeuil} -e1 PATH_VERS_EX_1 -e2 PATH_VERS_EX_2 [-p] [-t] "   
fi

python multi.py -a $ALGO -e1 $PATH1 -e2 $PATH2 $RESULT


        


