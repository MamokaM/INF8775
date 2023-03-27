for algo in "approx"  ; do

    for n in {"15","20","25"}; do
        directory="./"
        file=$(find "$directory" -maxdepth 1 -type f -name "N${n}_0" -print)
        dis=0  
        dis=$(python algo.py -a $algo -e $file -t)
        echo "result: $dis for algo $algo size $n"
    done
   
done