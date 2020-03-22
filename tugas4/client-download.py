import sys
import socket
import os

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print(f"connecting to {server_address}")
sock.connect(server_address)

Filename = input("Input File Name: ")

Data="download "+Filename
sock.send(Data.encode('utf-8'))
sock.shutdown(socket.SHUT_WR)

data = sock.recv(1024)
if data == b'File not Exist':
    print("File tidak ditemukan!")
else:
    f = open("client/"+Filename, 'wb')  # open in binary
    while (data):
        f.write(data)
        data = sock.recv(1024)
    print("File Berhasil diunduh!")
    f.close()

print("Closing.....")
sock.close()