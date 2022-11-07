import socket
import sys


def main():
    port = sys.argv[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', int(port)))
    users_info = {}
    users_messages = {}


    while True:
        data, addr = s.recvfrom(1024)
        print(str(data), addr)
        s.sendto(data.upper(), addr)


if __name__ == '__main__':
    main()
