from common.utils import Bet

""" Bet message type identifier """
BETS = "BET"

""" Finish message type identifier, signals that the lotto finished loading bets """
FINISH = "FIN"

""" Winner message type identifier, signals that the lotto wants to know its winners """
WINNER = "WIN"


class ClientMessage:
    """ A client message representation """

    def __init__(self, data: str):
        """
        Deserializes a string client message to the object
        """
        splitted = data.split(",")
        self.type = splitted[0]
        if self.type == BETS:
            self.bets: list[Bet] = []
            total_bets_in_message = int(splitted[1])
            self.lotto_agent = int(splitted[2])
            for i in range(total_bets_in_message):
                name = splitted[3 + i * 5]
                surname = splitted[4 + i * 5]
                document = splitted[5 + i * 5]
                birthdate = splitted[6 + i * 5]
                number = splitted[7 + i * 5]
                self.bets.append(
                    Bet(self.lotto_agent, name, surname, document, birthdate, number))
        elif self.type == FINISH or self.type == WINNER:
            self.lotto_agent = int(splitted[1])

    def finished(self) -> bool:
        return self.type == FINISH

    def has_bets(self) -> bool:
        return self.type == BETS

    def wants_winners(self) -> bool:
        return self.type == WINNER
