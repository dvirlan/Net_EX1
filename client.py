import socket
import sys


def main():
    # get from the user args the ip and the port of the server
    ip_server, port_server = sys.argv[1], int(sys.argv[2])
    if port_server < 0 or port_server > 65535:
        return
    # create a socket to send messages to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        prompt = input()
        s.sendto(prompt.encode('utf-8'), (ip_server, port_server))
        # quit if the user chooses 4
        if prompt == '4':
            break
        # get the answer from the server and print it
        data, addr = s.recvfrom(1024)
        if data.decode() != "":
            print(data.decode())
    s.close()


if __name__ == '__main__':
    main()
