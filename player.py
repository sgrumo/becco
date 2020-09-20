class Player:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "{}".format(self.name)

    def __repr__(self):
        return str(self)
