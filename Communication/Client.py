"""
    This file contains the Client code that receives and sends messages to the server.
    https://www.youtube.com/watch?v=_3nfrGdVcv0
"""
import socket
import time

HOST = '192.168.43.161'  # The server's hostname or IP address
PORT = 5050  # The port used by the server

class Client:

    def __init__(self, HOST, PORT):
        self.server_ip = HOST
        self.port = PORT
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = 'Free'
        self.is_game_started = True


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


    def verify_sent(self):
        """
        Check if the message has been received
        :return: True if the message has been received, else False
        """
        if self.check_if_received_return():
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


    def main_loop(self, message):
        self.connect()
        print('connected')
        while self.is_game_started:
            #self.check_connection()
            self.send_message(message)

            print('entered loop')
            self.status = self.check_if_received_return()
            print(self.status)
            time.sleep(0.3)



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
    client1.main_loop(b'1')
