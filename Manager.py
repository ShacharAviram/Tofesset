"""
    This file is the overall manager of the device. it contains the player status and controls the actions in the game.
"""
import Client
import ImageProcessor
import Indicator
import errno

class Manager:
    def __init__(self):
        """
        initialize an instance of a project manager
        contains player's status
        """
        self.mode = None  # Am I a catcher or a player?  0 - free player, 1 - catcher, 2 - caught player
        self.imageprocessor = None  # If I am a catcher
        self.indicator = None
        self.client = Client()
        self.HEADER_LENGTH = 10
        # A variable that determines if the game has started.
        # the value is changed by an outer user
        self.game_start = True


    def init_connection(self):
        """
        Make the first connection and update the mode
        :return: None
        """
        Client.client.connect()
        self.mode = self.Client.check_if_received_return()


    def init_camera_manager(self):
        """
        Create an Image processor class for the catcher
        :return: None
        """
        self.imageprocessor = ImageProcessor.ImageProcess()


    def init_indicator(self, role):
        """
        Create an Indicator class for each player
        :param role:
        :return: None
        """
        self.indicator = Indicator.Indicator()
        self.indicator.indicate(role)

    def begin_game(self):
        """
        Begin the game and call the relevant functions
        :return:
        """
        self.init_connection()
        self.init_indicator(self.mode)

        if self.mode == 1:
            self.init_camera_manager()

        if self.mode == 0:
            self.main_loop_player()
        elif self.mode == 1:
            self.main_loop_catcher()
        else:
            print('the player is suspended')



    def main_loop_player(self):
        """
        1. check for updates from server
        2. process message
        3. change indication
        :return: None
        """
        while True:

            message_header = self.client.s.recv(self.HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            st_sign_message = self.client.s.recv(message_length).decode('utf-8')

            while st_sign_message == 'start':

                try:
                    # Now we want to loop over received messages (there might be more than one) and print them
                    while True:

                        # Receive our "header" containing username length, it's size is defined and constant
                        username_header = self.client.s.recv(self.HEADER_LENGTH)
                        # If we received no data, server gracefully closed a connection,
                        # for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
                        if not len(username_header):
                            print('Connection closed by the server')
                            exit()

                        # Convert header to int value
                        username_length = int(username_header.decode('utf-8').strip())
                        # Receive and decode username
                        username = self.client.s.recv(username_length).decode('utf-8')

                        # Now do the same for message (as we received username, we received whole message,
                        # there's no need to check if it has any length)
                        message_header = self.client.s.recv(self.HEADER_LENGTH)
                        message_length = int(message_header.decode('utf-8').strip())
                        message = self.client.s.recv(message_length).decode('utf-8')

                        # Update status and print to screen
                        self.client.status = message  # TODO: check message format
                        if self.client.status == 'caught':
                            self.client.send_message(bytes('{message}'.format
                                                           (message=('caught', username)).encode('utf-8')))
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


    def main_loop_catcher(self):
        """
        1. check for updates from server
        2. check if There is a catch (ImageProcessor) (catch from image)
        3. send to server (if needed)
        4. get verification
        :return: None
        """
        while True:
            while self.game_start:

                st_message = 'start'
                self.client.send_message(
                    bytes('{message}'.format(message=st_message).encode('utf-8')))
                # does the catcher wait for another validation from the server?
                try:
                    # Now we want to loop over received messages (there might be more than one) and print them
                    while True:

                        # Receive our "header" containing username length, it's size is defined and constant
                        username_header = self.client.s.recv(self.HEADER_LENGTH)
                        # If we received no data, server gracefully closed a connection,
                        # for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
                        if not len(username_header):
                            print('Connection closed by the server')
                            exit()

                        # Convert header to int value
                        username_length = int(username_header.decode('utf-8').strip())
                        # Receive and decode username
                        username = self.client.s.recv(username_length).decode('utf-8')

                        # Now do the same for message (as we received username, we received whole message,
                        # there's no need to check if it has any length)
                        message_header = self.client.s.recv(self.HEADER_LENGTH)
                        message_length = int(message_header.decode('utf-8').strip())
                        message = self.client.s.recv(message_length).decode('utf-8')

                        # print message to the screen
                        print(message)
                        # check if received information from data processing, if so, send to server
                        if self.imageprocessor.catchFromImage()[0] is True:
                            snd_message = ('caught', self.imageprocessor.catchFromImage()[1])  # status and address
                            self.client.send_message(
                                bytes('{message}'.format(message=snd_message).encode('utf-8')))  # correct format

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
