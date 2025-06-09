import socket
import sys
import os
from colorama import *

# colors
BLUE = Fore.LIGHTBLUE_EX
RED = Fore.LIGHTRED_EX
GREEN = Fore.LIGHTGREEN_EX
WHITE = Fore.WHITE
YELLOW = Fore.LIGHTYELLOW_EX
RESET = Style.RESET_ALL

# connection
HOST_NAME = socket.gethostname()
HOST = socket.gethostbyname(HOST_NAME)
PORT = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
	try:
		client.connect((HOST, PORT))
	except:
		print("NO CONNECTION !")
	else:
		print("CONNECTION !")
		break

while True:
	command = str(input("[+] Admin~$ "))
	
	# clear screen
	if command == 'clear':
		os.system('clear')

	# get directory list content
	elif command == 'ls':
		client.send(command.encode())
		print(client.recv(1024).decode())

	# get current work directory (getcwd)
	elif command == 'pwd':
		client.send(command.encode())
		print(client.recv(1024).decode())

	# shutdown the computer
	elif command == 'shutdown':
		client.send(command.encode())

	# reboot the computer
	elif command == 'reboot':
		client.send(command.encode())

	# get platform type
	elif command == 'platform':
		client.send(command.encode())
		print(client.recv(1024).decode())

	# exit remote
	elif command == 'exit':
		print("0:KILL TERMINAL")
		client.send('exit'.encode())
		break
	
	# Unkown command
	else:
		print(f'{RED}[!] unkown command{RESET}')

sys.exit()
