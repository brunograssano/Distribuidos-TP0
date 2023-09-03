

import logging
from common.client_handler import ClientHandler
from common.utils import store_bets
from common.server_message import ok_message
from common.exceptions import SocketConnectionBroken
from common.server_message import later_message
from common.utils import load_bets
from common.utils import has_won
from common.server_message import winners_message


class LottoManager:
    """ A lottery manager. Handles the business logic """

    def __init__(self, client: ClientHandler, finished_lotteries: 'list[bool]'):
        self.client = client
        self.finished_lotteries = finished_lotteries

    def handle_lotto(self):
        """ Handles the lotto logic depending on the message type """
        try:
            while True:
                message = self.client.recv()
                if message.finished():
                    logging.debug(
                        f"action: receive_message | Lotto agent {message.lotto_agent} finished")
                    self.finished_lotteries[message.lotto_agent - 1] = True
                elif message.has_bets():
                    self.handle_bets_message(message)
                elif message.wants_winners():
                    logging.debug(
                        f"action: receive_message | Lotto agent {message.lotto_agent} wants to know its winners")
                    self.handle_winners_message(message.lotto_agent)
                    return
        except (SocketConnectionBroken, OSError) as e:
            logging.error(
                f"action: receive_message | result: fail | error: {e}")
        finally:
            self.client.close()

    def handle_bets_message(self, message):
        store_bets(message.bets)
        logging.info(f"action: apuestas_almacenadas | result: success")
        self.client.send(ok_message())

    def handle_winners_message(self, agent):
        finished = True
        for i in self.finished_lotteries:
            finished &= i
            if not finished:
                self.client.send(later_message())
                return

        logging.info("action: sorteo | result: success")
        winners = []
        for bet in load_bets():
            if bet.agency == agent and has_won(bet):
                winners.append(bet.document)
        self.client.send(winners_message(winners))
