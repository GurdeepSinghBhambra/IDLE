import socket
import threading
import json
import os

class SharedContainer:
    online_user_list = list()
    lender_dict = dict()
    MAX_LENDER_SIZE = 5

    def __init__(self):
        pass

    @classmethod
    def update_online_users(cls, username, optype):
        # appends element
        with threading.Lock():
            if(optype == 0 and username not in cls.online_user_list): 
                cls.online_user_list.append(username)
                return True
            # deletes element
            elif(optype == 1 and int(len(cls.online_user_list)) > 0):
                cls.online_user_list.remove(username)
                return True
            return False

    @classmethod
    def update_lender_dict(cls, optype, username, user_host_info=None):
        with threading.Lock():
            # appends element
            if(optype == 0 and int(len(cls.lender_dict)) <= cls.MAX_LENDER_SIZE):
                cls.lender_dict[username] = user_host_info
                return True
            # deletes element
            elif(optype == 1 and int(len(cls.lender_dict)) > 0):
                return cls.lender_dict.pop(username)
            return False

    @classmethod
    def check_lender_list(cls):
        with threading.Lock():
            if(int(len(cls.lender_dict)) > 0):
                return True
            return False


class ClientThread(threading.Thread, SharedContainer):
    cmd_recv_size  = 3
    str_recv_size = 128
    file_recv_size = 4096

    def __init__(self, client_address, client_sock):
        self.client_address = client_address
        self.client_recv = client_sock.recv
        self.client_send = client_sock.send
        self.username = None
        threading.Thread.__init__(self)

    def send_cmd(self, cmd):
        print("Sending Request:", cmd)
        self.client_send(bytes(str(cmd), 'utf-8'))

    def recv_cmd(self):
        recvd = str(self.client_recv(ClientThread.cmd_recv_size), 'utf-8')
        print("Receiving Request:", recvd)
        return recvd

    def recv_str(self):
        return str(self.client_recv(ClientThread.str_recv_size), 'utf-8')

    @staticmethod
    def checkCredentials(username, password):
        creds = json.load(open("user_credentials.json", 'r'))
        if(username in creds.keys() and password == creds[username]):
            return True
        else:
            return False

    def checkIfOnlineUser(self, recvd_msg):
        for user in SharedContainer.online_user_list[:]:
            if recvd_msg == user:
                return True
        return False

    @staticmethod
    def transferFile(client1_recv, client1_send, client2_recv, client2_send):
        print("Transferring File")
        while True:
            file_chunk = client1_recv(ClientThread.file_recv_size)
            client1_send(bytes("OK", 'utf-8'))
            print("Bytes Transfered:", len(file_chunk))
            client2_send(file_chunk)
            client2_recv(ClientThread.cmd_recv_size)
            if file_chunk == b'EOF':
                break
        print("File Transfer Complete")
        return True

    def LCS(self):
        self.send_cmd('GID')
        self.username = self.recv_str()
        self.send_cmd('GPW')
        password = self.recv_str()
        if(self.checkCredentials(self.username, password) == True and SharedContainer.update_online_users(self.username, 0) == True):
            self.send_cmd("SCF")
        else:
            self.send_cmd("FLD")

    @staticmethod
    def connectToIdler(server_info):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(tuple(server_info))
        return conn

    def RCS(self): 
        conn = None
        host_username = None
        client_server_info = None
        if(SharedContainer.check_lender_list() == True):
            host_username = list(SharedContainer.lender_dict.keys())[0]
            client_server_info = SharedContainer.update_lender_dict(1, host_username)
            print("Using {} as host".format(client_server_info))
            conn = self.connectToIdler(client_server_info)
            lender_recv, lender_send = conn.recv, conn.send
            lender_send(bytes("EXF", 'utf-8'))
            if(str(lender_recv(ClientThread.cmd_recv_size), 'utf-8') == "GFD"):
                self.send_cmd("GFD")
                if(self.transferFile(self.client_recv, self.client_send, lender_recv, lender_send) == True):
                    if(str(lender_recv(ClientThread.cmd_recv_size), 'utf-8') == "SCF"):
                        self.send_cmd("SCF")
                        if(str(lender_recv(ClientThread.cmd_recv_size), 'utf-8') == "TOF"):
                            self.send_cmd("TOF")
                            if(self.recv_cmd() == "GOF"):
                                lender_send(bytes("GOF", "utf-8"))
                                if(self.transferFile(lender_recv, lender_send, self.client_recv, self.client_send) == True and self.recv_cmd() == "SCF"):
                                    lender_send(bytes("SCF", "utf-8"))
                                    conn.close()
                                else:
                                    lender_send(bytes("FLD", "utf-8"))
                        else:
                            self.send_cmd("FLD")
                            lender_send(bytes("FLD", 'utf-8'))
                else:
                    self.send_cmd("FLD")
                    lender_send(bytes("FLD", 'utf-8'))
            else:
                self.send_cmd("FLD")
                lender_send(bytes("FLD", 'utf-8'))
        else:
            self.send_cmd("NLA")
        if(host_username and client_server_info):
            SharedContainer.update_lender_dict(0, host_username, client_server_info)
            print("Adding {} back to lender_dict".format(client_server_info))
        if(conn):
            conn.close()

    def MML(self):
        self.send_cmd("GID")
        username = self.recv_str()
        if(username in SharedContainer.online_user_list):
            host_info = list()
            self.send_cmd("GIP")
            host_info.append(self.recv_str())
            self.send_cmd("GPT")
            host_info.append(int(self.recv_str()))
            if(SharedContainer.update_lender_dict(0, username, host_info) != False):
                self.send_cmd("SCF")
            else:
                self.send_cmd("FLD")
        else:
            self.send_cmd("ILR")


    def WBL(self):
        self.send_cmd("GID")
        username = self.recv_str()
        if(username in SharedContainer.online_user_list):
            if(SharedContainer.update_lender_dict(1, username) != False):
                self.send_cmd("SCF")
            else:
                self.send_cmd("FLD")
        else:
            self.send_cmd("ILR")

    def initialRequest(self):
        recvd_msg = self.recv_cmd()
        if(recvd_msg == 'LCS'):
            self.LCS()
        elif(recvd_msg == 'RSC'):
            self.send_cmd("GID")
            if(self.checkIfOnlineUser(self.recv_str()) == True):
                self.RCS() 
            else:
                self.send_cmd("FLD")
        elif(recvd_msg == 'MML'):
            self.MML()
        elif(recvd_msg == 'WBL'):
            self.WBL()
        elif(recvd_msg == 'DCN'):
            self.send_cmd("GID")
            username = self.recv_str()
            if(username in SharedContainer.online_user_list):
                self.send_cmd("BYE")
                SharedContainer.update_online_users(username, 1)
            else:
                print("ERROR: ILLEGAL REQUEST")
                print("recvd_msg:", recvd_msg)
                self.send_cmd("ILR")
        else:
            print("ERROR: ILLEGAL REQUEST")
            print("recvd_msg:", recvd_msg)
            self.send_cmd("ILR")
 
    def run(self):
        print("-----------------------------------------------------")
        print("Users Online:", SharedContainer.online_user_list)
        print("Lenders Online:", SharedContainer.lender_dict)
        print("Connection from:", self.client_address)
        self.initialRequest()
        print("Client", self.client_address,"Disconnected")
        print("-----------------------------------------------------")

def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        print("Server Started")
        print("Server ip:", host, "port:", port)
        while True:
            server.listen(1)
            clientsock, clientaddress = server.accept()
            newthread = ClientThread(clientaddress, clientsock)
            newthread.start()
        print("Server Shutdown")

start_server("127.0.0.1", 8001)
