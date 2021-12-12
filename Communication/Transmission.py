"""
    This file contains the code that sends messages to other devices.
    the messages need to be created, sent, and verified (that it was received)

    https://www.youtube.com/watch?v=MbXWrmQW-OE
"""


class Transmitter:
    def __init__(self):
        """
        initialize an instance of an transmitter
        """
        pass

    def create_caught_message(self, *args):
        """
        writes the message and gets the id of the reciever
        :return: written message + id of the reciever
        """
        pass

    def create_verification_message(self, *args):
        pass

    def send_message(self, *args):
        """
        send the message!
        :return: True if recieved, False else.
        """
        pass

    def verify_recieving(self, *args):
        """
        checks that the last sent message was recieved.
        :return: True if recieved, False else.
        """
        pass

