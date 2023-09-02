
import logging
import socket

from common.exceptions import SocketConnectionBroken


class ClientStream:
    """
    Interface to send and receive from a socket and prevent short reads/writes
    when communicating with the client
    """

    def __init__(self, socket: socket):
        """
        socket must be a TCP socket
        """
        self.socket = socket
        self.addr = socket.getpeername()

    def send(self, data):
        """ 
        Sends byte data to the client preventing short sends
        Raises SocketConnectionBroken if there is an error
        """
        total_bytes = len(data)
        total_sent = 0
        while total_sent < total_bytes:
            bytes_sent = self.socket.send(data[total_sent:])
            if bytes_sent == 0:
                logging.error(
                    f"action: send_message | result: fail | ip: {self.addr[0]} | No bytes sent, socket connection broken")
                raise SocketConnectionBroken()
            total_sent += bytes_sent
        logging.debug(
            f"action: sent_message | result: success | ip: {self.addr[0]} | msg: {data}")

    def recv(self, total_recv: int):
        """ 
        Receives and returns byte data from the client preventing short reads.
        Raises SocketConnectionBroken if there is an error
        """
        recv_bytes = 0
        data = b""
        while recv_bytes < total_recv:
            recv_data = self.socket.recv(total_recv - recv_bytes)
            if recv_data == b'':
                logging.error(
                    f"action: receive_message | result: fail | ip: {self.addr[0]} | No bytes received, socket connection broken")
                raise SocketConnectionBroken()
            recv_bytes += len(recv_data)
            data += recv_data
        logging.debug(
            f"action: receive_message | result: success | ip: {self.addr[0]} | msg: {data}")
        return data

    def close(self):
        """ Closes the socket """
        logging.info(
            f"action: closing_socket | Closing client socket {self.addr[0]}")
        self.socket.close()
