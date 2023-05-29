import socket
import sys

HOST = 'localhost'
PORT = 1234


def main():
    while True:
        try:
            sock = socket.socket()
            sock.connect((HOST, PORT))
            sending_data = input()
            if sending_data == 'exit':
                sock.sendall(b'exit')
                break
            sock.sendall(bytes(sending_data, 'utf-8'))
            while True:
                buf = sock.recv(1024).decode('utf-8')
                if len(buf) == 0:
                    break
                print(str(buf))
        except ConnectionRefusedError:
            print('The server is unavailable')
            sys.exit(0)


if __name__ == '__main__':
    main()
