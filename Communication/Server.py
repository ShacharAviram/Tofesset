import socket

"""
    This file contains the code that operates the server.
    it should contain messages handling code, data structure for the game and error handling functions.

    https://www.youtube.com/watch?v=MbXWrmQW-OE
"""
TOFFES = 1
FREE = 0
CAUGHT = 2


def initial_connection(ind):
    conn, addr = s.accept()
    with conn:
        database[addr[0]] = 0
        print(database)
        print('Connected by', addr[0])
        data = conn.recv(4096)
        print(data)
        ind += 1
        conn.sendto(b'0', addr)
        return ind


def check_for_message(conn):
    if conn.recv(4096):
        return True
    else:
        ...


HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 5050              # Arbitrary non-privileged port
database = dict()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    ind = 0
    while ind <= 5:
        ind = initial_connection(ind)


def change_database(addr, status_change):
    database[addr] = status_change
    return database

def send_message():
    ...








