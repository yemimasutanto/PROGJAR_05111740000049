import sys
import socket
import os

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print(f"connecting to {server_address}")
sock.connect(server_address)

try:
    Filename = input("Input File Name: ")
    if os.path.isfile("client/" + Filename):
        Request = "upload " + Filename
        print("File detect: " + Filename)
        f = open("client/" + Filename, "rb")
        Filename = "AOE" + Request
        Fil8 = Filename.encode("utf-8")
        datasend = f.read() + Fil8

        print("Sending File.....")
        sock.send(datasend)
        sock.shutdown(socket.SHUT_WR)
        data = sock.recv(10).decode()
        print(data)
    else:
        print("File Tidak ditemukan!")

finally:
    print("\nClosing connnection")
    sock.close()