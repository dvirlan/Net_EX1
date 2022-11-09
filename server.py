import socket
import sys

users_info = {}
# {"address_raz": ("raz", ["m1"]),
#               "address_david": ("david", ["m2"])}


def concat_messages(address):
    full_message = ""
    list_messages = users_info[address][1]
    for message in list_messages:
        full_message += (message + "\n")
    full_message = full_message[:-1]
    t = users_info[address][0], []
    users_info[address] = t
    return full_message


def join_group(name, new_addr, sock):
    str1 = ""
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
    sock.sendto(concat_messages(address).encode(), address)
    print(users_info)



def change_name(new_name, address, sock):
    for user_address in users_info:
        if user_address == address:
            old_name = users_info[address][0]
            new_t = (new_name, users_info[address][1])
            users_info[address] = new_t
            break
    for user_address in users_info:
        if user_address != address:
            users_info[user_address][1].append(old_name + " changed his name to " + new_name)
    sock.sendto(concat_messages(address).encode(), address)

    print(users_info)


def leave_group(address):
    left_name = users_info[address][0]
    users_info.pop(address)
    for user_address in users_info:
        users_info[user_address][1].append(left_name + " has left the group")
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
            join_group(arg2, addr, s)
        elif option == "2":
            send_message(arg2, addr, s)
        elif option == "3":
            change_name(arg2, addr, s)
        elif option == "4":
            leave_group(addr)
        elif option == "5":
            s.sendto(concat_messages(addr).encode(), addr)
        else:
            s.sendto("Illegal request".encode(), addr)



if __name__ == '__main__':
    main()
