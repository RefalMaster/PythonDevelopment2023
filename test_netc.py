import sys
import socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((sys.argv[1], int(sys.argv[2])))
    while msg := sys.stdin.readline():
        s.sendall(msg.strip().encode())
        print(s.recv(1024).decode())