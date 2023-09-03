

def ok_message():
    """ An OK message string to signal the client the message was processed correctly """
    return "OK"


def later_message():
    """ A LATER message string to signal the client to wait """
    return "LATER"


def winners_message(winners: 'list[str]'):
    """ A WINNER message string to send the lotto agent the winners """
    msg = f"WIN,{len(winners)}"
    for winner in winners:
        msg += f",{winner}"
    return msg
