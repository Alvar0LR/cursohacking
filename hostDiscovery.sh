#!/bin/bash

function ctrl_c(){
    echo -e "\n\n [!] Saliendo..."
    tput cnorm
    exit 1
}

tput civis

# control c
trap ctrl_c SIGINT

# puertos
array=(21 22 23 25 80 139 443 445 8080)

for i in $(seq 1 254); do
    for port in "${array[@]}"; do
        timeout 1 bash -c "echo '' > /dev/tcp/192.168.1.$i/$port" &>/dev/null && echo "[+] El Host 192.168.1.$i - ACTIVE <--> PORT: $port [OPEN]" &
    done
done
wait

tput cnorm


