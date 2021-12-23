import socket
import errno
import sys
import time

HEADER_LENGTH = 10

IP = "10.0.0.23"
PORT = 5050


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)

my_username = '11111'
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True:

    # Wait for user to input a message
    message = input(f'{my_username} > ')  # TODO define wanted message

    # If message is not empty - send it
    if message:

        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:

            # Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)

            # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                print('Connection closed by the server')
                exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # Receive and decode username
            username = client_socket.recv(username_length).decode('utf-8')

            # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            # Print message
            print(f'{username} > {message}')

    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        # We just did not receive anything
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: '.format(str(e)))
        sys.exit()



def main_loop_catcher(self):
    """
    1. check for updates from server
    2. check if There is a catch (ImageProcessor) (catch from image)
    3. send to server (if needed)
    4. get verification
    :return: None
    """
    # add variable to check if game started
    # send message from catcher to server and back to all players that the game has started
    # does the catcher wait for another validation from the server?
    while self.client.is_game_started:
        # self.client.check_if_received_return() In order to verify message, and receive messages
        if self.imageprocessor.catchFromImage()[0] is True:
            message = ('caught', self.imageprocessor.catchFromImage()[1])  # status and address
            self.client.send_message(bytes('{message}'.format(message=message).encode('utf-8')))  # correct format
        time.sleep(2.3)  # TODO define sleep time via image processing time

def main_loop_player(self):
    """
    1. check for updates from server
    2. process message
    3. change indication
    :return: None
    """
    # add variable to check if game started
    while self.client.is_game_started:
        # self.check_connection()
        self.client.status = self.client.check_if_received_return()[2]  # TODO: check message format
        if self.client.status == 2:
            self.client.send_message(bytes('{message}'.format(message=(1, self.client.name)).encode('utf-8')))
        time.sleep(2.3)  # TODO define sleep time via image processing time
