import socket
import sys

# created by Dvir Landau and Daniel Meir Karl

# the user dict has a key of client's address and his value is a tuple
# consists of his name and a list of his current left messages
# for example,  {"address_raz": ("raz", ["m1"]),
#                "address_david": ("david", ["m2"])}
users_info = {}


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
    # add a message to everyone that the new user has joined
    for user_address in reversed(users_info):
        users_info[user_address][1].append(name + " has joined")
        # create a string that names all participants.
        str1 += users_info[user_address][0] + ", "
    group_names = str1[:len(str1) - 2]
    # print(group_names)
    sock.sendto(group_names.encode(), new_addr)
    users_info[new_addr] = (name, [])
    # print(users_info)


def send_message(message, address, sock):
    for user_address in users_info:
        # add a message to everyone's list except the sender
        if user_address != address:
            users_info[user_address][1].append(users_info[address][0] + ": " + message)
    # send all his remained messages to the client
    sock.sendto(concat_messages(address).encode(), address)
    # print(users_info)


def change_name(new_name, address, sock):
    for user_address in users_info:
        if user_address == address:
            old_name = users_info[address][0]
            new_t = (new_name, users_info[address][1])
            users_info[address] = new_t
            break
    # add a message to everyone (except the user that changed his name) that the user changed his name.
    for user_address in users_info:
        if user_address != address:
            users_info[user_address][1].append(old_name + " changed his name to " + new_name)
    # send all his remained messages to the client
    sock.sendto(concat_messages(address).encode(), address)

    # print(users_info)


def leave_group(address):
    left_name = users_info[address][0]
    # remove the user from the dict
    users_info.pop(address)
    # add a message to everyone (except the user that left the group) that the user left the group.
    for user_address in users_info:
        users_info[user_address][1].append(left_name + " has left the group")
    # print(users_info)


def main():
    # get the port from user, create a socket and bind the port to the socket
    port = int(sys.argv[1])
    if port < 0 or port > 65535:
        return
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', port))
    # every loop the sever serve a request from a client
    while True:
        data, addr = s.recvfrom(1024)
        # split the request into 2 parts
        splitter_list = data.decode().split(" ", 1)

        option = splitter_list[0].lstrip()
        arg2 = ""
        # check if there is 2nd arg and save it
        if len(splitter_list) > 1:
            arg2 = splitter_list[1]
        # check if the client sent Illegal request - operation that needs registration before or
        # missing a 2nd arg when it's needed for the operartion
        if ((option == "1" or option == "2" or option == "3") and arg2 == "") or (
                addr not in users_info and option != "1") or (addr in users_info and option == "1"):
            s.sendto("Illegal request".encode(), addr)
        # go to the appropriate function according to the client's option
        elif option == "1":
            join_group(arg2, addr, s)
        elif option == "2":
            send_message(arg2, addr, s)
        elif option == "3":
            change_name(arg2, addr, s)
        elif option == "4":
            leave_group(addr)
        elif option == "5":
            # send all his remained messages to the client
            s.sendto(concat_messages(addr).encode(), addr)
        else:
            s.sendto("Illegal request".encode(), addr)


if __name__ == '__main__':
    main()
