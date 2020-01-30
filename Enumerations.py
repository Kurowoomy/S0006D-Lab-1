import enum
import random

class location_type(enum.Enum):
    home = 1
    school = 2
    mines = 3
    shop = 4
    cafeteria = 5
    bar = 6

class message_type(enum.Enum):
    msg_SMS = 1
    msg_meetUp = 2
    msg_cantCome = 3