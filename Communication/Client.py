"""
    This file contains the Client code that receives and sends messages to the server.
    https://www.youtube.com/watch?v=_3nfrGdVcv0
"""
import socket

HOST = '192.168.43.161'  # The server's hostname or IP address
PORT = 5050  # The port used by the server

class Client:

    def __init__(self, HOST, PORT):
        self.server_ip = HOST
        self.port = PORT
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = 'Free'
        self.is_game_started = False


    def connect(self):
        """
        Connect to server
        :return: None
        """
        self.s.connect((self.server_ip, self.port))


    def check_if_received(self):
        """
        Check is a message has been received
        :return: True or False
        """
        data = self.s.recv(1024)
        if data:
            return True
        else:
            return False


    def receive(self):
        """
        Receive message from server
        :return: Data - type string
        """
        data = self.s.recv(1024)
        return repr(data)


    def send_message(self, message):
        """
        Sends a message to the server
        :param message: The message we want to send, type string
        :return: None
        """
        self.s.sendall(message)


    def verify_sent(self):
        """
        Check if the message has been received
        :return: True if the message has been received, else False
        """
        if self.receive():
            return True
        else:
            return False


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


    def main_loop(self):
        self.connect()
        while self.is_game_started:
            self.check_connection()
            if self.check_if_received():
                self.status = self.receive()


"""
send current state: caught, free, tagger ; ip address
send to server: have_caught, have_freed ; ip address
verify connection by using exceptions.

main loop
check message and send to manager
fetch status 
"""

if __name__ == "__main__":
    client1 = Client('192.168.43.165', 5050)
    client1.connect()
    client1.send_message(b'hi')
