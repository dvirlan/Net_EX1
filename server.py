import socket
import sys

users_info = {"raz": ("add_raz", ["m1"]),
              "david": ("add_david", ["m2"])}


def main():
    port = sys.argv[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', int(port)))

    while True:
        data, addr = s.recvfrom(1024)
        print(data, addr)
        splitter_list = str(data).split(" ", 1)
        option = splitter_list[0]
        str1 = ""
        if len(splitter_list) > 1:
            name = splitter_list[1]
        if option == "1":
            for user_name in users_info:
                users_info[user_name][1].append(name + " has joined")
                str1 += user_name + ", "
            new_str = str1[:len(str1)-2]
            print(new_str)
            s.sendto(new_str, addr)
            users_info[name] = (addr, [])

if __name__ == '__main__':
    main()
