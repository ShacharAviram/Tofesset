import socket
import select
import random

HEADER_LENGTH = 10

IP = "10.60.4.245"
PORT = 5050
Game_begin = False

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind, so server informs operating system that it's going to use given IP and port
# For a server using 0.0.0.0 means to listen on all available interfaces, useful to connect locally to 127.0.0.1 and remotely to LAN interface IP
server_socket.bind((IP, PORT))

# This makes server listen to new connections
server_socket.listen()

# List of sockets for select.select()
sockets_list = [server_socket]

# List of connected clients - socket as a key, user header and name as data
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')

database = dict()


def get_player_list(dict):
    list = []
    for key in dict.keys():
        list.append(key)
    return list


def get_random_catcher(loop_num):
    if loop_num == 1:
        players = get_player_list(database)
        toffes_user = random.choice(players)
        return toffes_user


# Handles message receiving
def receive_message(client_socket):
    try:

        # Receive our "header" containing message length, it's size is defined and constant
        message_header = client_socket.recv(HEADER_LENGTH)

        # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        if not len(message_header):
            return False

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:
        # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
        # or just lost his connection
        # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
        # and that's also a cause when we receive an empty message
        return False


loop_num = 1


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for notified_socket in read_sockets:
        # If notified socket is a server socket - new connection, accept it
        if notified_socket == server_socket:

            # Accept new connection
            # That gives us new socket - client socket, connected to this given client only, it's unique for that client
            # The other returned object is ip/port set
            client_socket, client_address = server_socket.accept()
            # Client should send his name right away, receive it
            user = receive_message(client_socket)
            database[user['data'].decode('utf-8')] = 0
            # If False - client disconnected before he sent his name
            if user is False:
                continue

            # Add accepted socket to select.select() list
            sockets_list.append(client_socket)

            # Also save username and username header
            clients[client_socket] = user

            print('Accepted new connection from {}:{}, username: {}'.format(*client_address,
                                                                            user['data'].decode('utf-8')))
        # Else existing socket is sending a message
        else:

            # Receive message
            message = receive_message(notified_socket)
            # print(message) unnecessary
            # If False, client disconnected, cleanup
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)

                # Remove from our list of users
                del clients[notified_socket]

                continue

            # Get user by notified socket, so we will know who sent the message
            user = clients[notified_socket]
            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
            if message["data"].decode("utf-8") in '3':
                Game_begin = True
            # Begin game on queue!
            if Game_begin:
                # Getting random catcher
                toffes = get_random_catcher(loop_num)
                # Sending catcher he is the catcher
                if loop_num == 1:
                    loop_num += 1
                    # Update database with catcher
                    database[toffes] = 1
                    for client_socket in clients:
                        # Send it only to referred to client
                        if clients[client_socket]['data'].decode('utf-8') == toffes:
                            # Send user and message (both with their headers)
                            # We are reusing here message header sent by sender, and saved username header send by user when he connected
                            client_socket.send(user['header'] + 'S'.encode('utf-8') + message['header'] + '1'.encode('utf-8'))
                if message["data"].decode("utf-8") in '':
                    # Update database
                    database[user["data"].decode("utf-8")] = message["data"].decode("utf-8")
                # Iterate over connected clients and broadcast message
                for client_socket in clients:
                    # Send it only to reffered to client
                    # Send catching message, can be sent only by catcher
                    if clients[client_socket] == message and \
                            database[user["data"].decode("utf-8")] == 1 and \
                            user["data"].decode("utf-8") != message["data"].decode('utf-8'):
                        # Send user and message (both with their headers)
                        # We are reusing here message header sent by sender, and saved username header send by user when he connected
                        client_socket.send(user['header'] + user['data'] + message['header'] + '2'.encode('utf-8'))
                        # Update database with info catcher
                        database[message['data'].decode('utf-8')] = 2
            print(database)

    # It's not really necessary to have this, but will handle some socket exceptions just in case
    for notified_socket in exception_sockets:
        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)

        # Remove from our list of users
        del clients[notified_socket]


