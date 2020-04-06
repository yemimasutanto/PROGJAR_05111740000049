import socket
import os
import json

TARGET_IP = "127.0.0.1"
TARGET_PORT = 8889

class ChatClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (TARGET_IP, TARGET_PORT)
        self.sock.connect(self.server_address)
        self.tokenid = ""

    #fungsi yang berisi proses jika user menginput command, apa yg akan terjadi
    def proses(self, cmdline):
        j = cmdline.split(" ")
        try:
            command = j[0].strip()
            if (command == 'auth'):
                username = j[1].strip()
                password = j[2].strip()
                return self.login(username, password)
            elif (command == 'send'):
                usernameto = j[1].strip()
                message = ""
                for w in j[2:]:
                    message = "{} {}".format(message, w)
                return self.sendmessage(usernameto, message)
            elif (command == 'inbox'):
                return self.inbox()
            elif (command == 'logout'):
                return self.logout()
            elif (command == 'status'):
                return self.list()
            else:
                return "Sorry, wrong command"
        except IndexError:
            return "Sorry, wrong command [Index Error]"

    #fungsi untuk mengirim input command ke server
    def sendstring(self, string):
        try:
            self.sock.sendall(string.encode())
            receivemsg = ""
            while True:
                data = self.sock.recv(64)
                print("Receiving from server", data)
                if (data):
                    receivemsg = "{}{}".format(receivemsg,
                                               data.decode())
                    if receivemsg[-4:] == '\r\n\r\n':
                        print("end of string")
                        return json.loads(receivemsg)
        except:
            self.sock.close()
            return {'status': 'ERROR', 'message': 'Failed'}

    #fungsi proses login
    def login(self, username, password):
        string = "auth {} {} \r\n".format(username, password)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            self.tokenid = result['tokenid']
            return "Success, Username: {}, token: {} ".format(username, self.tokenid)
        else:
            return "Error, {}".format(result['message'])

    #fungsi proses dalam pengiriman pesan
    def sendmessage(self, usernameto="xxx", message="xxx"):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "send {} {} {} \r\n".format(self.tokenid, usernameto, message)
        print(string)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "message sent to {}".format(usernameto)
        else:
            return "Error, {}".format(result['message'])

    def inbox(self):
        if (self.tokenid == ""):
            return "Error, user not authorized"
        string = "inbox {} \r\n".format(self.tokenid)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "{}".format(json.dumps(result['messages']))
        else:
            return "Error, {}".format(result['message'])

    #fungsi proses logout
    def logout(self):
        if (self.tokenid == ""):
            return "Error, user not authorized"
        string = "logout {} \r\n".format(self.tokenid)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            self.tokenid = ""
            return "Closing Connection....."
        else:
            return "Error, {}".format(result['message'])

    #fungsi proses list
    def list(self):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "status {} \r\n".format(self.tokenid)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "Online User: {}".format(json.dumps(result['message']))
        else:
            return "Error, {}".format(result['message'])

if __name__ == "__main__":
    cc = ChatClient()
    while True:
        print("CLI Progjar")
        cmdline = input("> {}: ".format(cc.tokenid))
        print(cc.proses(cmdline))