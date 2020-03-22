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
if os.path.isfile("client/" + Filename):
    Kirim = "upload " + Filename
    print("Sending: " + Filename)
    myfile = open("client/" + Filename, "rb")
    Filename = "AOE" + Kirim
    Fil8 = Filename.encode("utf-8")
    datasend = myfile.read() + Fil8
    sock.send(datasend)
    sock.shutdown(socket.SHUT_WR)
    hasil = sock.recv(10).decode()
    print(hasil)
else:
    print("File Tidak ditemukan!")

print("Closing........")
sock.close()