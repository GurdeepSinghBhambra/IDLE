import socket 
import subprocess

class Client:
    cmd_recv_size  = 3
    file_recv_size = 4096
    PY_FILE = "EXEC_PYTHON_FILE.py"
    OUTPUT_FILE = "OUTPUT_FILE.txt"
    CLIENT_AS_SERVER_FILEPATH ="client_as_server.py"

    def __init__(self, server_ipaddress, server_port):
        self.server_ip = server_ipaddress
        self.server_port = server_port
        self.client_as_server_ip = None
        self.client_as_server_port = None
        self.username = None
        self.server_proc = None

    def login(self, username, password):
        self.username = username
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockfd:
            sockfd.connect((self.server_ip, self.server_port))
            sockfd.send(bytes("LCS", "utf-8"))
            if(str(sockfd.recv(Client.cmd_recv_size), "utf-8") == "GID"):
                sockfd.send(bytes(username, "utf-8"))
                if(str(sockfd.recv(Client.cmd_recv_size), "utf-8") == "GPW"):
                    sockfd.send(bytes(password, "utf-8"))
                    if(str(sockfd.recv(Client.cmd_recv_size), "utf-8") == "SCF"):
                        return True
            return False

    def logout(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockfd:
            sockfd.connect((self.server_ip, self.server_port))
            sockfd.send(bytes("DCN", 'utf-8')) 
            if(str(sockfd.recv(Client.cmd_recv_size), 'utf-8') == "GID"):
                sockfd.send(bytes(self.username, 'utf-8'))
                if(str(sockfd.recv(Client.cmd_recv_size), 'utf-8') == "BYE"):
                    return True
        return False

    def runScript(self, filename):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.server_ip, self.server_port))
            sock.send(bytes("RSC", 'utf-8'))
            if(str(sock.recv(Client.cmd_recv_size), 'utf-8') == "GID"):
                sock.send(bytes(self.username, 'utf-8'))
                if(str(sock.recv(Client.cmd_recv_size), 'utf-8') == "GFD"):
                    self.sendFile(sock.recv, sock.send, filename)
                    if(str(sock.recv(Client.cmd_recv_size), 'utf-8') == "SCF"):
                        if(str(sock.recv(Client.cmd_recv_size), 'utf-8') == "TOF"):
                            sock.send(bytes("GOF", 'utf-8'))
                            self.recvFile(sock.recv, sock.send, Client.OUTPUT_FILE)    
                            sock.send(bytes("SCF", 'utf-8'))
                        else:
                            return None
                    else:
                        return None
                else:
                    return "No Available Lender(s)"
            else:
                return None

        file_contents = ""

        with open(Client.OUTPUT_FILE, 'rt') as f:
            for line in f.readlines():
                file_contents+=line
        return file_contents

    @staticmethod
    def recvFile(recv, send, filename):
        print("Receiving file:", filename)
        with open(filename, 'wb') as f:
            while True:
                data = recv(Client.file_recv_size)
                send(bytes("OK", 'utf-8'))
                if data == b'EOF':
                    break
                f.write(data)
        print("File Received")
        return True

    @staticmethod
    def sendFile(recv, send, filename):
        print("Sending file:", filename)
        with open(filename, 'rb') as f:
            line = f.read(Client.file_recv_size)
            while(line):
                send(line)
                if(recv(Client.cmd_recv_size) != bytes('OK', 'utf-8')):
                    return False
                line = f.read(Client.file_recv_size)
        send(bytes("EOF", 'utf-8'))
        if(recv(Client.cmd_recv_size) != bytes('OK', 'utf-8')):
            return False
        print("File Sent")
        return True

    @staticmethod
    def execFile():
        print("Executing File")
        with open(Client.OUTPUT_FILE, 'w') as f:
            process = subprocess.run(['python', Client.PY_FILE], stdout=f, universal_newlines=True)
        print("Execution Done")

    def declareMML(self, server_info):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.server_ip, self.server_port))
            sock.send(bytes("MML", 'utf-8'))
            if(str(sock.recv(Client.cmd_recv_size), 'utf-8') == "GID"):
                sock.send(bytes(self.username, 'utf-8'))
                if(str(sock.recv(Client.cmd_recv_size), 'utf-8') == "GIP"):
                    sock.send(bytes(str(server_info[0]), 'utf-8'))
                    if(str(sock.recv(Client.cmd_recv_size), 'utf-8') == "GPT"):
                        sock.send(bytes(str(server_info[1]), 'utf-8'))
                        if(str(sock.recv(Client.cmd_recv_size), 'utf-8') == "SCF"):
                            print("Declared MML")
                            sock.close()
                            return True
        return False
                    
    def withdrawMML(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.server_ip, self.server_port))
            sock.send(bytes("WBL", 'utf-8'))
            if(str(sock.recv(Client.cmd_recv_size), 'utf-8') == "GID"):
                sock.send(bytes(self.username, 'utf-8'))
                if(str(sock.recv(Client.cmd_recv_size), 'utf-8') == "SCF"):
                    print("Withdrawn Being MML")
                    return True
        return False

    def shutdownServer(self):
        if(self.client_as_server_ip == None):
            print("ERROR: Trying to Shutdown Non-Existent Server")
        else:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.client_as_server_ip, self.client_as_server_port))
                sock.send(bytes("SDN", 'utf-8'))
                if(str(sock.recv(Client.cmd_recv_size), "utf-8") == "SSD"):
                    return True
        return False
    
    def withdrawBeingIdler(self):
        if(self.client_as_server_ip == None):
            print("ERROR: Server Does not Exists")
            return False
        if(self.shutdownServer() == False):
            print("ERROR: Server Shutdown Failed")
            return False
        print("Server Dead")
        while(self.server_proc.poll() != None):
            self.server_proc.kill()
        print("Server Process Dead")
        if(self.withdrawMML() == False):
            print("ERROR: Failed To Request WBL")
            return False
        self.client_as_server_ip = self.client_as_server_port = self.server_proc = None
        return True


    def becomeIdler(self, server_ip, server_port):
        self.client_as_server_ip = server_ip
        self.client_as_server_port = int(server_port)
        self.declareMML((self.client_as_server_ip, self.client_as_server_port))
        self.server_proc = subprocess.Popen(["start", "/wait", "python", "{}".format(Client.CLIENT_AS_SERVER_FILEPATH),  "{}".format(self.client_as_server_ip), "{}".format(self.client_as_server_port)], shell=True)
        print("Server Started @", (self.client_as_server_ip, self.client_as_server_port))
        return True
