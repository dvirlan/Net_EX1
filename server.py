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
    sock.sendto(group_names.encode(), new_addr)
    users_info[name] = (new_addr, [])
    print(users_info)


def send_message(message, name):
    for user_name in users_info:
        if user_name != name:
            users_info[user_name][1].append(name + ": " + message)
    print(users_info)


def change_name(new_name, old_name):
    for user_name in users_info:
        if user_name == old_name:
            users_info[new_name] = users_info.pop(old_name)
            break
    for user_name in users_info:
        if user_name != new_name:
            users_info[user_name][1].append(old_name + " changed his name to " + new_name)
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
        str1 = ""
        if len(splitter_list) > 1:
            name = splitter_list[1]
        if option == "1":
            original_name = name
            join_group(name, addr, s)
        elif option == "2":
            send_message(name, original_name)
        elif option == "3":
            change_name(name, original_name)
        elif option == "4":
            leave_group(original_name)


if __name__ == '__main__':
    main()
