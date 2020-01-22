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
        self.currentState = State_RunAway()
        self.location = location_type.homeSweetHome
        self.goldCarried = 0
        self.moneyInBank = 0
        self.thirst = 0
        self.fatigue = 0

    def update(self):
        self.thirst += 1
        self.currentState.Execute(self)

    def changeState(self, newState):
        self.currentState = newState
        print(self.currentState)
    


class State:
    def Execute(self, character):
        print(character.ID)

class State_RunAway(State):
    def Execute(self, character):
        print(character.ID, 'is running away')

class State_Sleep(State):
    #TODO: add transitions and their conditions in the state classes
    pass

#run()
miner1 = Miner(0)
miner2 = Miner(1)

print(miner1.ID, miner2.ID, BaseGameEntity.nextValidID)


