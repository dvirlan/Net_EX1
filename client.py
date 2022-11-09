import socket
import sys


def main():
    ip_server, port_server = sys.argv[1], sys.argv[2]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        prompt = input()
        s.sendto(prompt.encode('utf-8'), (ip_server, int(port_server)))
        if prompt == '4':
            break
        data, addr = s.recvfrom(1024)
        if data.decode() != "":
            print(data.decode())
    s.close()


if __name__ == '__main__':
    main()
