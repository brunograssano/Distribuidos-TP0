import logging
import socket
from common.client_stream import ClientStream
from common.client_message import ClientMessage

INITIAL_MESSAGE_SIZE_IN_BYTES = 4


class ClientHandler:

    def __init__(self, socket: socket):
        """
        socket must be a TCP socket
        """
        self.client_stream = ClientStream(socket)

    def recv(self) -> ClientMessage:
        """ Receives a message from the client converting byte data to ClientMessage """
        size = self.client_stream.recv(INITIAL_MESSAGE_SIZE_IN_BYTES)
        message_size = int.from_bytes(size, byteorder='big', signed=False)
        logging.info(
            f"action: receive_message | result: success | Receiving {message_size} bytes")
        data = self.client_stream.recv(message_size)
        decoded = data.decode('utf-8')
        logging.info(
            f"action: receive_message | result: success | msg: '{decoded}'")
        return ClientMessage(decoded)

    def send(self, message: str):
        """ Sends a message to the client converting a string to byte data """
        encoded = message.encode('utf-8')
        encoded_length = len(encoded)
        bytes_to_send = int.to_bytes(
            encoded_length, length=4, byteorder='big', signed=False)
        logging.info(
            f"action: sending_message | bytes size: {encoded_length} | msg: '{message}'")
        self.client_stream.send(bytes_to_send)
        self.client_stream.send(encoded)

    def close(self):
        """ Closes the connection to the client """
        self.client_stream.close()
