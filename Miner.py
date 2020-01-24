import enum
import time


class location_type(enum.Enum):
    goldMine = 1
    bank = 2
    saloon = 3
    homeSweetHome = 4
    can = 5



class message_type(enum.Enum):
    Msg_HiHoneyImHome = 1
    Msg_StewReady = 2

class Telegram:
    def __init__(self, senderEntity, recieverEntity, msg, extraInfo):
        self.senderEntity = senderEntity
        self.recieverEntity = recieverEntity
        self.msg = msg
        self.extraInfo = extraInfo

class MessageDispatcher:
    def dispatchMessage(self, telegram):
        #TODO: find object based on ID


        telegram.recieverEntity.handleMessage(telegram.msg)
        






class BaseGameEntity:
    nextValidID = 0
    def __init__(self, id):
        self.setID(id)
        self.location = location_type
        self.currentState = State()

    def setID(self, val):
        if val >= BaseGameEntity.nextValidID:
            BaseGameEntity.nextValidID += 1
            self.ID = val

    def changeLocation(self, newLocation):
        self.location = newLocation

    def changeState(self, newState):
        self.currentState.Exit(self)
        self.currentState = newState()
        self.currentState.Enter(self)

    def handleMessage(self, msg):
        pass

class Miner(BaseGameEntity):
    def __init__(self, ID):
        BaseGameEntity.__init__(self, ID)
        self.currentState = EnterMineAndDigForNugget()
        self.location = location_type.goldMine
        self.goldCarried = 0
        self.moneyInBank = 0
        self.depositedInBank = 0
        self.thirst = 0
        self.fatigue = 0

    def update(self):
        self.thirst += 1
        self.currentState.Execute(self)

class HouseWife(BaseGameEntity):
    def __init__(self, ID):
        BaseGameEntity.__init__(self, ID)
        self.currentState = CleanHouse()
        self.location = location_type.homeSweetHome
        self.bladder = 0

    def update(self):
        self.currentState.Execute(self)

    def handleMessage(self, msg):
        if(msg.msg == message_type.Msg_HiHoneyImHome):
            print("Hi honey. Let me make you some of mah fine country stew")
        




class State:
    def Enter(self, character):
        pass
    def Execute(self, character):
        pass
    def Exit(self, character):
        pass
    def onMessage(self, character, telegram):
        return True

class EnterMineAndDigForNugget(State):
    def Enter(self, character):
        if(character.location != location_type.goldMine):
            print('Walkin to the gold mine')
            character.changeLocation(location_type.goldMine)
    def Execute(self, character):
        character.goldCarried += 1
        character.fatigue += 1
        print("Pickin' up a nugget")
        if(character.goldCarried >= 3):
            character.changeState(VisitBankAndDepositGold)
        elif(character.thirst >= 5):
            character.changeState(QuenchThirst)
    def Exit(self, character):
        print("Ah'm leavin' the gold mine with mah pockets full o' gold")

class VisitBankAndDepositGold(State):
    def Enter(self, character):
        if(character.location != location_type.bank):
            print("Goin' to the bank. Yes siree")
            character.changeLocation(location_type.bank)
    def Execute(self, character):
        character.moneyInBank += 1
        character.depositedInBank += 1
        character.goldCarried = 0
        print("Depositin' gold. Total savings now:", character.moneyInBank)
        if(character.depositedInBank >= 2):
            print("Woohoo! Rich enough for now. Back home to mah li'l lady")
            character.depositedInBank = 0
            character.changeState(GoHomeAndSleepTilRested)
        else:
            character.changeState(EnterMineAndDigForNugget)
    def Exit(self, character):
        print("Leavin' the bank")

class QuenchThirst(State):
    def Enter(self, character):
        if(character.location != location_type.saloon):
            print("Boy, ah sure is thusty! Walkin' to the saloon")
            character.changeLocation(location_type.saloon)
    def Execute(self, character):
        character.thirst = 0
        print("That's mighty fine sippin' liqour")
        character.changeState(EnterMineAndDigForNugget)
    def Exit(self, character):
        print("Leavin' the saloon, feelin' good")

class GoHomeAndSleepTilRested(State):
    def Enter(self, character):
        if(character.location != location_type.homeSweetHome):
            print("Walkin' home")
            character.changeLocation(location_type.homeSweetHome)
            dispatcher = MessageDispatcher()
            telegram = Telegram(character, 2, message_type.Msg_HiHoneyImHome, None)
            dispatcher.dispatchMessage(telegram)
    def Execute(self, character):
        character.fatigue -= 3
        character.thirst = 0
        if(character.fatigue <= 0):
            print("What a God-darn fantastic nap! Time to find more gold")
            character.changeState(EnterMineAndDigForNugget)
        else:
            print("ZZZZ...")
    def Exit(self, character):
        print("Leavin' home")

class CleanHouse(State):
    def Enter(self, character):
        if(character.location != location_type.homeSweetHome):
            character.changeLocation(location_type.homeSweetHome)
    def Execute(self, character):
        character.bladder += 1
        print("Moppin' the floor")
        if(character.bladder >= 5):
            character.changeState(FeelCallOfNature)
    def Exit(self, character):
        pass

class FeelCallOfNature(State):
    def Enter(self, character):
        if(character.location != location_type.can):
            print("Walkin' to the can. Need to powda mah pretty li'l nose")
            character.changeLocation(location_type.can)
    def Execute(self, character):
        character.bladder = 0
        print("Ahhhhhh! Sweet relief!")
        character.changeState(CleanHouse)
    def Exit(self, character):
        print("Leavin' the john")

#run()
miner1 = Miner(0)
wife1 = HouseWife(1)

i = 0
while(i < 39):
    time.sleep(1)

    i += 1
    print("Miner:")
    miner1.update()
    print("")
    print("Wife:")
    wife1.update()
    print("")