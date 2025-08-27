#!/bin/env bash


function arg_parse() {
    all_args=($@)
    count=0

    for i in ${all_args[@]}; do
        count=$(($count+1))
        to_install=()
        if [[ $i == "--loops" ]]; then
            loop_count=${all_args[count]}
        fi
        if [[ $i == "--install" ]]; then 
            to_install+=${all_args[count]}
            echo ${to_install[@]}
        fi
    done
}
arg_parse $@
count=$loop_count
count_loop=0
cd ..

now=$(date +"%H%M%S%3N")

echo "started" ${to_install[@]}
while [ $count_loop != $count ]; do
    echo "loop: " $count_loop
    count_loop=$((count_loop+1))
    python main.py install ${to_install[@]}
done

end=$(date +"%H%M%S%3N")
result=$(($end - $now))
echo "milliseconds: " $result

if (( $result >= 5000 )); then
    echo "installing to long"
else
    echo "installing to fast"
fi