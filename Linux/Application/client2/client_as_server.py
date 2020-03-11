import subprocess
import socket
import sys
import os

file_recv_size = 4096
cmd_recv_size = 3
PY_FILE = "EXEC_PYTHON_FILE.py"
OUTPUT_FILE = "OUTPUT_FILE.txt"

def recvFile(recv, send, filename):
    global file_recv_size, cmd_recv_size
    print("Receiving file:", filename)
    with open(filename, 'wb') as f:
        while True:
            data = recv(file_recv_size)
            send(bytes("OK", 'utf-8'))
            #print(data)
            if data == b'EOF':
                break
            f.write(data)
    print("File Received")
    return True

def sendFile(recv, send, filename):
    global file_recv_size, cmd_recv_size
    print("Sending file:", filename)
    with open(filename, 'rb') as f:
        line = f.read(file_recv_size)
        while(line):
            send(line)
            if(recv(cmd_recv_size) != bytes('OK', 'utf-8')):
                return False
            line = f.read(file_recv_size)
    send(bytes("EOF", 'utf-8'))
    if(recv(cmd_recv_size) != bytes('OK', 'utf-8')):
        return False
    print("File Sent")
    return True

def execFile():
    global PY_FILE, OUTPUT_FILE 
    print("Executing File")
    with open(OUTPUT_FILE, 'w') as f:
        process = subprocess.run(['python3', PY_FILE], stdout=f, universal_newlines=True)
    print("Execution Done")

def server_forever(server_ip, server_port):
    global file_recv_size, cmd_recv_size, PY_FILE, OUTPUT_FILE 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((server_ip, server_port))
        server.listen(1)
        while True:
            clientsock, clientaddress = server.accept()
            print("-----------------------------------------------------")
            print("Client {} Connected".format(clientaddress))
            first_recv = str(clientsock.recv(cmd_recv_size), 'utf-8')
            if(first_recv == "SDN"): #receiving server shutdown cmd
                clientsock.send(bytes("SSD", "utf-8")) #sending confirmation for server shutdown
                break
            if(first_recv == "EXF"):
                clientsock.send(bytes("GFD", "utf-8"))
                if(recvFile(clientsock.recv, clientsock.send, PY_FILE) == True):
                    clientsock.send(bytes("SCF", "utf-8"))
                    execFile()
                    clientsock.send(bytes("TOF", "utf-8"))
                    if(str(clientsock.recv(cmd_recv_size), 'utf-8') == "GOF"):
                        sendFile(clientsock.recv, clientsock.send, OUTPUT_FILE)
                        if(str(clientsock.recv(cmd_recv_size), 'utf-8') != "SCF"):
                            print("ERROR: Failed Transferring OUTPUT_FILE.txt")
                            
                        else:
                            print("EXECUTED FILE SUCCESSFULLY")
                else:
                    print("ERROR: Failed Receiving PY_FILE.py")
                    
            print("Client {} Disconnected".format(clientaddress))
            print("-----------------------------------------------------")

def start():
    server_ip, server_port = sys.argv[1:]
    server_forever(server_ip, int(server_port))

start()
