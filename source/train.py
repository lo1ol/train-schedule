class Train:
    """
    Consist values necessary for identification one train
    instance of Train more then other if depart time is later
    and if depart time is equal, train with more travel time is more
    Also have method form for getting tuple, identified train (necessary for sqlite) 
    """
    def __init__(self, number, type, d_time, t_time):
        """
        Make instance of Train
        :param number: train number
        :param type: Express or Passenger
        :param d_time: department time
        :param t_time: travel time
        """
        self.number = number
        self.type = type
        self.d_time = d_time
        self.t_time = t_time

    def __eq__(self, other):
        if (self.d_time == other.d_time and self.t_time == other.t_time and self.type == other.type
            and self.number == other.number):
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if self.d_time > other.d_time:
            return True
        elif self.d_time == other.d_time and self.t_time > other.t_time:
            return True
        else:
            return False

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __lt__(self, other):
        return not self.__ge__(other)

    def __le__(self, other):
        return not self.__gt__(other)

    def form(self):
        """
        :return: dictionary with keys train_number, type, d_time, t_time
        """
        return {'train_number': self.number, 'type': self.type, 'd_time': self.d_time, 't_time': self.t_time}
