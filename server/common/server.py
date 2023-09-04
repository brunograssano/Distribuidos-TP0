import socket
import logging
import threading

from common.exceptions import SignalException
from common.client_handler import ClientHandler
from common.lotto_agent import LottoManager


class Server:
    def __init__(self, port, listen_backlog, total_lotteries):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)
        self.finished_lotteries = [False] * total_lotteries
        self.finished_lock = threading.Lock()
        self.bets_lock = threading.Lock()

    def run(self):
        """
        Dummy Server loop

        Server that accept a new connections and establishes a
        communication with a client. After client with communication
        finishes, servers starts to accept new connections again
        """
        lottos: list[LottoManager] = []
        finished_lottos: list[LottoManager] = []
        try:
            while True:
                client_sock = self.__accept_new_connection()
                client_handler = ClientHandler(client_sock)
                lotto_manager = LottoManager(
                    client_handler, self.finished_lotteries, self.finished_lock, self.bets_lock)
                lotto_manager.start()
                lottos.append(lotto_manager)
                for lotto in lottos:
                    if not lotto.is_alive():
                        finished_lottos.append(lotto)
                for lotto in finished_lottos:
                    logging.info(
                        "action: joining_thread | A lotto thread finished, joining and cleaning")
                    lotto.join()
                    lottos.remove(lotto)
                finished_lottos.clear()
        except SignalException:
            for lotto in lottos:
                logging.info(
                    "action: joining_thread | Signaling a lotto thread to stop")
                lotto.stop()
                lotto.join()
            logging.info("action: closing_socket | Closing server socket")
            self._server_socket.close()

    def __accept_new_connection(self):
        """
        Accept new connections

        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """

        # Connection arrived
        logging.info('action: accept_connections | result: in_progress')
        c, addr = self._server_socket.accept()
        logging.info(f'action: accept_connections | result: success | ip: {addr[0]}')
        return c
