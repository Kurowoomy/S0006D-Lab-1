import enum

class location_type(enum.Enum):
    home = 1
    school = 2
    mines = 3
    shop = 4
    cafeteria = 5
    bar = 6

class message_type(enum.Enum):
    msg_meetUp = 1
    msg_tooHungry = 2