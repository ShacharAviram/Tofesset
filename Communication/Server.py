import socket
import time
"""
    This file contains the code that operates the server.
    it should contain messages handling code, data structure for the game and error handling functions.

    https://www.youtube.com/watch?v=MbXWrmQW-OE
"""

TOFFESS = 1
FREE = 0
CAUGHT = 2


class Server:
    def __init__(self):
        self.HOST = ''
        self.PORT = 5050
        self.database = dict()
        self.num_of_players = 0

    def initialize_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen(1)
            ind = 0
            while ind <= 2:
                conn, addr = s.accept()
                with conn:
                    if addr[0] not in self.database:
                        self.database[addr[0]] = 0
                        print(self.database)
                        print('Connected by', addr[0])
                        data = conn.recv(4096)
                        # print(data)
                        conn.sendto(b'0', addr)

                if data:
                    self.change_database(addr[0], data)
                    print(self.database)

    def initial_connection(ind):
        conn, addr = s.accept()
        with conn:
            database[addr[0]] = [0, conn]
            print(database)
            print('Connected by', addr[0])
            data = conn.recv(4096)
            print(data)
            ind += 1
            conn.sendto(b'0', addr)
            return ind, conn, addr


    def check_for_message():
        """if .recv(4096):
            return True
        else:
            return False"""


    def change_database(self, addr, status_change):
        self.database[addr] = status_change
        return self.database




    def create_catcher(ind):
        if ind == 1:
            database[0] = 1


    def send_message():
        ...





if __name__ == '__main__':
    server = Server()
    Server.initialize_server(server)



