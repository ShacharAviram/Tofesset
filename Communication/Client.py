"""
    This file contains the Client code that receives and sends messages to the server.
    https://www.youtube.com/watch?v=_3nfrGdVcv0
"""
import socket
import time

HOST = '10.0.0.23'  # The server's hostname or IP address
PORT = 5050  # The port used by the server

class Client:

    def __init__(self, HOST, PORT):
        self.server_ip = HOST
        self.port = PORT
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = 0
        self.is_game_started = True
        self.name = 11111  # TODO automatically define client address


    def connect(self):
        """
        Connect to server
        :return: None
        """
        self.s.connect((self.server_ip, self.port))


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
        Sends a message to the server
        :param message: The message we want to send, type string
        :return: None
        """
        self.s.sendall(message)


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
            #self.check_connection()
            print('entered loop')
            # if self.check_if_received_return():
            self.send_message(bytes('{message}'.format(message=message).encode('utf-8')))
            self.status = self.check_if_received_return()
            print(self.status)
            time.sleep(2)  # TODO define sleep time via image processing time



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

"""
import Client
client2 = Client.Client('10.0.0.23', 2022)
client2.main_loop(b'2')
"""