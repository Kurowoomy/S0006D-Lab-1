import enum


class location_type(enum.Enum):
    goldMine = 1
    bank = 2
    saloon = 3
    homeSweetHome = 4



class BaseGameEntity:
    nextValidID = 0
    def __init__(self, id):
        self.setID(id)

    def setID(self, val):
        if val >= BaseGameEntity.nextValidID:
            BaseGameEntity.nextValidID += 1
            self.ID = val

class Miner(BaseGameEntity):
    def __init__(self, ID):
        BaseGameEntity.__init__(self, ID)
        self.currentState = EnterMineAndDigForNugget()
        self.location = location_type.goldMine
        self.goldCarried = 0
        self.moneyInBank = 0
        self.thirst = 0
        self.fatigue = 0

    def update(self):
        self.thirst += 1
        self.currentState.Execute(self)

    def changeState(self, newState):
        self.currentState.Exit(self)
        self.currentState = newState()
        self.currentState.Enter(self)

    def changeLocation(self, newLocation):
        self.location = newLocation



class State:
    pass

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
        if(character.thirst >= 5):
            character.changeState(QuenchThirst)
    def Exit(self, character):
        print("Ah'm leavin' the gold mine with mah pockets full o' gold")

class VisitBankAndDepositGold(State):
    def Enter(self, character):
        pass
    def Execute(self, character):
        pass
    def Exit(self, character):
        pass

class QuenchThirst(State):
    def Execute(self, character):
        pass

class GoHomeAndSleepTilRested(State):
    def Execute(self, character):
        pass

#run()
miner1 = Miner(0)
i = 0
while(i < 6):
    i += 1
    miner1.update()
