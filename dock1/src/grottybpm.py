class TicketState(object):
    name = "state"
    allowed = []

    def switch(self, state):
        if state.name in self.allowed:
            self.__class__ = state
            return True
        else:
            return False

    def __str__(self):
        return self.name


class Opened(TicketState):
    name = "opened"
    allowed = ['answered', 'closed']


class Answered(TicketState):
    name = "answered"
    allowed = ['awaiting', 'closed']


class Closed(TicketState):
    name = "closed"
    allowed = []


class Awaiting(TicketState):
    name = "awaiting"
    allowed = ['answered']


d = {'opened': Opened, 'answered': Answered, 'closed': Closed, 'awaiting': Awaiting}


class StateEngine(object):
    def __init__(self, initialstate='opened'):
        if initialstate not in d:
            raise ValueError('Such status doen\'t exists')
        self.state = d[initialstate]()

    def change(self, state):
        return self.state.switch(d[state])
