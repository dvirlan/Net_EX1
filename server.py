import socket
import sys

users_info = {"address_raz": ("raz", ["m1"]),
              "address_david": ("david", ["m2"])}


def join_group(name, new_addr, sock):
    str1 = ""
    print("start opt 1")
    for user_address in users_info:
        users_info[user_address][1].append(name + " has joined")
        str1 += users_info[user_address][0] + ", "
    group_names = str1[:len(str1) - 2]
    print(group_names)
    sock.sendto(group_names.encode(), new_addr)
    users_info[new_addr] = (name, [])
    print(users_info)


def send_message(message, address, sock):
    for user_address in users_info:
        if user_address != address:
            users_info[user_address][1].append(users_info[address][0] + ": " + message)
    print(users_info)
    sock.sendto("".encode(), address)


def change_name(new_name, address):
    for user_address in users_info:
        if user_address == address:
            old_name = users_info[address][0]
            new_t = (new_name, users_info[address][1])
            users_info[address] = new_t
            break
    for user_address in users_info:
        if user_address != address:
            users_info[user_address][1].append(old_name + " changed his name to " + new_name)
    print(users_info)


def leave_group(name):
    users_info.pop(name)
    for user_name in users_info:
        users_info[user_name][1].append(name + "  has left the group")
    print(users_info)


def main():
    port = sys.argv[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', int(port)))

    while True:
        data, addr = s.recvfrom(1024)
        splitter_list = data.decode().split(" ", 1)
        option = splitter_list[0]
        if len(splitter_list) > 1:
            arg2 = splitter_list[1]
        if option == "1":
            original_name = arg2
            join_group(arg2, addr, s)
        elif option == "2":
            send_message(arg2, addr, s)
        elif option == "3":
            change_name(arg2, addr)
        elif option == "4":
            leave_group(original_name)


if __name__ == '__main__':
    main()
