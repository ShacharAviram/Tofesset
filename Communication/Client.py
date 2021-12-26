"""
    This file contains the Client code that receives and sends messages to the server.
    https://www.youtube.com/watch?v=_3nfrGdVcv0
"""
import socket
import time
import errno

HOST = '10.0.0.18'  # The server's hostname or IP address
PORT = 5050  # The port used by the server
HEADER_LENGTH = 10

class Client:

    def __init__(self, HOST, PORT):
        self.server_ip = HOST
        self.port = PORT
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = 0
        self.is_game_started = True
        self.name = 'c'  # TODO automatically define client address
        self.HEADER_LENGTH = 10


    def connect(self):
        """
        Connect to server
        :return: None
        """
        self.s.connect((self.server_ip, self.port))
        username = self.name.encode('utf-8')
        username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
        self.s.sendall((username_header + username))


    def check_if_received_return(self):
        """
        Check is a message has been received
        :return: data if received, else None
        """
        data = self.s.recv(4096)
        if data:
            # self.send_message(data)  # check if necessary
            return repr(data)
        else:
            return None


    def send_message(self, message):
        """
        ***Check if message is True, only then call this function***
        Sends a message to the server
        :param message: The message we want to send, type string
        :return: None
        """
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        self.s.sendall(message_header + message)


    def check_change_status(self):
        """
        :return:
        """
        if self.status != self.check_if_received_return()[2]:
            return True


    def check_connection(self):
        """
        Checks if a disconnection has occurred, if so it tries to reconnect
        :return: None
        """
        try:
            self.s.send("connected?")
        except:
            # recreate the socket and reconnect
            self.s.connect((HOST, PORT))
            self.s.send("connected")


    def main_loop_player(self):
        """
        1. check for updates from server
        2. process message
        3. change indication
        :return: None
        """
        self.connect()
        message_header = self.s.recv(self.HEADER_LENGTH)
        message_length = int(message_header.decode('utf-8').strip())
        st_sign_message = self.s.recv(message_length).decode('utf-8')
        while True:

            while st_sign_message == 'start':

                # Wait for user to input a message
                message = ''  # TODO define wanted message

                # If message is not empty - send it
                if message:
                    # Encode message to bytes, prepare header and convert to bytes, like for username above,
                    # then send
                    message = message.encode('utf-8')
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(message_header + message)

                try:
                    # Now we want to loop over received messages (there might be more than one) and print them
                    while True:

                        # Receive our "header" containing username length, it's size is defined and constant
                        username_header = self.s.recv(self.HEADER_LENGTH)
                        # If we received no data, server gracefully closed a connection,
                        # for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
                        if not len(username_header):
                            print('Connection closed by the server')
                            exit()

                        # Convert header to int value
                        username_length = int(username_header.decode('utf-8').strip())
                        # Receive and decode username
                        username = self.s.recv(username_length).decode('utf-8')

                        # Now do the same for message (as we received username, we received whole message,
                        # there's no need to check if it has any length)
                        message_header = self.s.recv(self.HEADER_LENGTH)
                        message_length = int(message_header.decode('utf-8').strip())
                        message = self.s.recv(message_length).decode('utf-8')

                        # Update status and print to screen
                        self.status = message  # TODO: check message format
                        if self.status == '2':
                            self.send_message(bytes('{message}'.format(message=('caught', username)).encode('utf-8')))
                        print(message)
                # exception for possible errors
                except IOError as e:
                    # This is normal on non blocking connections -
                    #   when there are no incoming data error is going to be raised
                    # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
                    # We are going to check for both - if one of them -
                    #   that's expected, means no incoming data, continue as normal
                    # If we got different error code - something happened
                    if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                        print('Reading error: {}'.format(str(e)))
                        exit()

                    # We just did not receive anything
                    continue

                except Exception as e:
                    # Any other exception - something happened, exit
                    print('Reading error: '.format(str(e)))
                    exit()

if __name__ == "__main__":
    client1 = Client('10.0.0.18', 5050)
    client1.main_loop_player()
