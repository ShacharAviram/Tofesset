"""
    This file contains the Client code that receives and sends messages to the server.
    https://www.youtube.com/watch?v=_3nfrGdVcv0
"""
import socket
import time
import errno

HOST = '10.0.0.23'  # The server's hostname or IP address
PORT = 5050  # The port used by the server
HEADER_LENGTH = 10

class Client:

    def __init__(self, HOST, PORT):
        self.server_ip = HOST
        self.port = PORT
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = 0
        self.is_game_started = True
        self.name = '11111'  # TODO automatically define client address


    def connect(self):
        """
        Connect to server
        :return: None
        """
        self.s.connect((self.server_ip, self.port))
        username = self.name.encode('utf-8')
        username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
        self.s.sendall(('free', username_header + username))


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


    def main_loop(self, message):
        self.connect()
        print('connected')
        self.send_message(message)
        while self.is_game_started:
            print('entered loop')
            # if self.check_if_received_return():
            self.send_message(bytes('{message}'.format(message=message).encode('utf-8')))
            self.status = self.check_if_received_return()
            print(self.status)
            time.sleep(2)  # TODO define sleep time via image processing time


    def main_loop2(self):

        while True:
            # Wait for user to input a message
            message = input(f'{self.name} > ')  # TODO define wanted message
            # If message is not empty - send it
            if message:
                self.send_message(message)
            try:
                # Now we want to loop over received messages (there might be more than one) and print them
                while True:
                    # Receive our "header" containing username length, it's size is defined and constant
                    username_header = self.s.recv(HEADER_LENGTH)
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
                    message_header = self.s.recv(HEADER_LENGTH)
                    message_length = int(message_header.decode('utf-8').strip())
                    message = self.s.recv(message_length).decode('utf-8')
                    # Print message
                    print(f'{username} > {message}')

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


"""
send current state: caught, free, tagger ; ip address
send to server: have_caught, have_freed ; ip address
verify connection by using exceptions.

main loop
check message and send to manager
fetch status 
"""

if __name__ == "__main__":
    client1 = Client('10.0.0.23', 2022)
    client1.main_loop(b'0')
