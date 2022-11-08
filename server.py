import socket
import sys

users_info = {"raz": ("add_raz", ["m1"]),
              "david": ("add_david", ["m2"])}


def join_group(name, new_addr, sock):
    str1 = ""
    print("start opt 1")
    for user_name in users_info:
        users_info[user_name][1].append(name + " has joined")
        str1 += user_name + ", "
    group_names = str1[:len(str1) - 2]
    print(group_names)
    print(users_info)
    sock.sendto(group_names.encode(), new_addr)
    users_info[name] = (new_addr, [])


def main():
    port = sys.argv[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', int(port)))

    while True:
        data, addr = s.recvfrom(1024)
        splitter_list = data.decode().split(" ", 1)
        option = splitter_list[0]
        str1 = ""
        if len(splitter_list) > 1:
            name = splitter_list[1]
        if option == "1":
            join_group(name, addr, s)


if __name__ == '__main__':
    main()
