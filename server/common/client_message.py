from common.utils import Bet

""" Bet message type identifier """
BETS = "BET"


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
            lotto_agent = splitted[2]
            for i in range(total_bets_in_message):
                name = splitted[3 + i * 5]
                surname = splitted[4 + i * 5]
                document = splitted[5 + i * 5]
                birthdate = splitted[6 + i * 5]
                number = splitted[7 + i * 5]
                self.bets.append(
                    Bet(lotto_agent, name, surname, document, birthdate, number))
