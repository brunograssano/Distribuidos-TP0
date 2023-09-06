from common.utils import Bet

""" Bet message type identifier """
BETS = "BET"

""" Finish message type identifier, signals that the lotto finished loading bets """
FINISH = "FIN"

""" Winner message type identifier, signals that the lotto wants to know its winners """
WINNER = "WIN"

CLIENT_MESSAGE_TYPE_INDEX = 0
TOTAL_BETS_INDEX = 1
LOTTO_AGENT_BETS_INDEX = 2
LOTTO_AGENT_INDEX = 1
BETS_NAME_OFFSET = 3
BETS_SURNAME_OFFSET = 4
BETS_DOCUMENT_OFFSET = 5
BETS_BIRTHDATE_OFFSET = 6
BETS_NUMBER_OFFSET = 7
COMMA_SEPARATOR = ","
TOTAL_BET_FIELDS = 5


class ClientMessage:
    """ A client message representation """

    def __init__(self, data: str):
        """
        Deserializes a string client message to the object
        """
        splitted = data.split(COMMA_SEPARATOR)
        self.type = splitted[CLIENT_MESSAGE_TYPE_INDEX]
        if self.type == BETS:
            self.bets: list[Bet] = []
            total_bets_in_message = int(splitted[TOTAL_BETS_INDEX])
            self.lotto_agent = int(splitted[LOTTO_AGENT_BETS_INDEX])
            for i in range(total_bets_in_message):
                name = splitted[BETS_NAME_OFFSET + i * TOTAL_BET_FIELDS]
                surname = splitted[BETS_SURNAME_OFFSET + i * TOTAL_BET_FIELDS]
                document = splitted[BETS_DOCUMENT_OFFSET +
                                    i * TOTAL_BET_FIELDS]
                birthdate = splitted[BETS_BIRTHDATE_OFFSET +
                                     i * TOTAL_BET_FIELDS]
                number = splitted[BETS_NUMBER_OFFSET + i * TOTAL_BET_FIELDS]
                self.bets.append(
                    Bet(self.lotto_agent, name, surname, document, birthdate, number))
        elif self.type == FINISH or self.type == WINNER:
            self.lotto_agent = int(splitted[LOTTO_AGENT_INDEX])

    def finished(self) -> bool:
        return self.type == FINISH

    def has_bets(self) -> bool:
        return self.type == BETS

    def wants_winners(self) -> bool:
        return self.type == WINNER
