

import logging
import threading
from common.client_handler import ClientHandler
from common.utils import store_bets
from common.server_message import ok_message
from common.exceptions import SocketConnectionBroken
from common.server_message import later_message
from common.utils import load_bets
from common.utils import has_won
from common.server_message import winners_message


class LottoManager(threading.Thread):
    """ A lottery manager. Handles the business logic """

    def __init__(self, client: ClientHandler, finished_lotteries: 'list[bool]', bets_lock: threading.Lock, finished_lock: threading.Lock):
        threading.Thread.__init__(self)
        self.client = client
        self.finished_lotteries = finished_lotteries
        self.finished_lock = finished_lock
        self.bets_lock = bets_lock

    def run(self):
        """ Handles the lotto logic depending on the message type """
        try:
            while True:
                message = self.client.recv()
                if message.finished():
                    logging.debug(
                        f"action: receive_message | Lotto agent {message.lotto_agent} finished")
                    self.finished_lock.acquire()
                    self.finished_lotteries[message.lotto_agent - 1] = True
                    self.finished_lock.release()
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
        self.bets_lock.acquire()
        store_bets(message.bets)
        self.bets_lock.release()
        logging.info(f"action: apuestas_almacenadas | result: success")
        self.client.send(ok_message())

    def handle_winners_message(self, agent):
        finished = True
        self.finished_lock.acquire()
        for i in self.finished_lotteries:
            finished &= i
            if not finished:
                self.finished_lock.release()
                self.client.send(later_message())
                return
        self.finished_lock.release()

        logging.info("action: sorteo | result: success")
        winners = []
        self.bets_lock.acquire()
        for bet in load_bets():
            if bet.agency == agent and has_won(bet):
                winners.append(bet.document)
        self.bets_lock.release()
        self.client.send(winners_message(winners))

    def stop(self):
        self.client.close()
