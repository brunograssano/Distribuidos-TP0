

import logging
from common.client_handler import ClientHandler
from common.utils import store_bets
from common.server_message import ok_message
from common.exceptions import SocketConnectionBroken


class LottoManager:
    """ A lottery manager. Handles the business logic """

    def __init__(self, client: ClientHandler):
        self.client = client

    def handle_lotto(self):
        """ Handles the lotto logic depending on the message type (only store_bets for now)"""
        try:
            message = self.client.recv()
            store_bets(message.bets)
            logging.info(
                f"action: apuesta_almacenada | result: success | dni: {message.bets[0].document} | numero: {message.bets[0].number}")
            self.client.send(ok_message())
        except (SocketConnectionBroken, OSError) as e:
            logging.error(
                f"action: receive_message | result: fail | error: {e}")
        finally:
            self.client.close()
