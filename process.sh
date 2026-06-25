#!/bin/bash

#ctrl_c
function ctrl_c(){
    echo -e "Saliendo..."
    tput cnorm; exit 1
}


#trap
trap ctrl_c SIGINT


old_process=$(ps -eo user,command)

tput civis

while true; do
    new_process=$(ps -eo user,command)
    diff <(echo "$old_process") <(echo "$new_process") | grep "[\>\<]" | grep -vE "command|kworker|procmon"
    old_process=$new_process
done
