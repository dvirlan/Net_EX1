import socket
import sys

users_info = {}


def main():
    port = sys.argv[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', int(port)))

    while True:
        #data, addr = s.recvfrom(1024)
        data = "1 DANIEL"
        addr = "add1"
        l = str(data).split(" ", 1)
        option = int(l[0])
        if len(l) > 1:
            name = l[1]
        if option == 1:
            for user_name in users_info:
                users_info[user_name][1].append(name + " has joined")
            users_info[name] = (addr, [])
        print(users_info)
        #print(str(data), addr)
        #s.sendto(data.upper(), addr)


if __name__ == '__main__':
    main()
