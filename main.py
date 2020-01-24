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
        self.depositedInBank = 0
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

    def increaseFatigue(self):
        if(self.goldCarried >= 3):
            self.fatigue += 1



class State:
    def Enter(self, character):
        pass
    def Execute(self, character):
        pass
    def Exit(self, character):
        pass

class EnterMineAndDigForNugget(State):
    def Enter(self, character):
        if(character.location != location_type.goldMine):
            print('Walkin to the gold mine')
            character.changeLocation(location_type.goldMine)
    def Execute(self, character):
        character.goldCarried += 1
        character.increaseFatigue()
        print("Pickin' up a nugget")
        if(character.goldCarried >= 3):
            character.changeState(VisitBankAndDepositGold)
        if(character.thirst >= 5):
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
        if(character.depositedInBank >= 5):
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
    def Execute(self, character):
        character.fatigue -= 1
        character.thirst = 0
        print("ZZZZ...")
        if(character.fatigue <= 0):
            print("What a God-darn fantastic nap! Time to find more gold")
            character.changeState(EnterMineAndDigForNugget)
    def Exit(self, character):
        print("Leavin' home")

#run()
miner1 = Miner(0)
i = 0
while(i < 39):
    i += 1
    miner1.update()

#läs hur man gör global states
