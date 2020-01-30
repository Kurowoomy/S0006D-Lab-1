import Enumerations
import StateMachine
import States

class BaseGameEntity:
    nextValidID = 0
    def __init__(self, ID):
        self.setID(ID)
        self.alive = True
        self.canShop = True
        self.sleeping = False
        self.willMeetUp = False
        self.isSocializing = False
        self.participants = 0
    def setID(self, ID):
        if(ID >= BaseGameEntity.nextValidID):
            BaseGameEntity.nextValidID += 1
            self.ID = id
        else:
            print("invalid ID")
    def changeLocation(self, newLocation):
        self.location = newLocation
    def checkIfEnoughMoney(self, money, amount):
        if(money >= amount):
            self.canShop = True

class Student(BaseGameEntity):
    def __init__(self, ID, name, location, fatigue, hunger, foodInventory, pencils, money, drinkingNeeds, socialNeeds):
        BaseGameEntity.__init__(self, ID)
        self.stateMachine = StateMachine.StateMachine(self, States.Studying)
        self.stateMachine.SetCurrentState(States.Studying)
        self.stateMachine.SetPreviousState(States.Studying)
        self.stateMachine.SetGlobalState(States.StudentGlobalState)
        self.name = name
        self.location = location
        self.fatigue = fatigue
        self.hunger = hunger
        self.foodInventory = foodInventory
        self.pencils = pencils
        self.money = money
        self.drinkingNeeds = drinkingNeeds
        self.socialNeeds = socialNeeds
        
    def handleMessage(self, telegram):
        if(self.stateMachine.globalState.onMessage(self, telegram)):
            pass
        else:
            self.stateMachine.currentState.onMessage(self, telegram)
        
class Worker(BaseGameEntity):
    def __init__(self, ID, name, location, fatigue, hunger, foodInventory, shovels, money, drinkingNeeds, socialNeeds):
        BaseGameEntity.__init__(self, ID)
        self.stateMachine = StateMachine.StateMachine(self, States.Mining)
        self.stateMachine.SetCurrentState(States.Mining)
        self.stateMachine.SetPreviousState(States.Mining)
        self.stateMachine.SetGlobalState(States.WorkerGlobalState)
        self.name = name
        self.location = location
        self.fatigue = fatigue
        self.hunger = hunger
        self.foodInventory = foodInventory
        self.shovels = shovels
        self.money = money
        self.drinkingNeeds = drinkingNeeds
        self.socialNeeds = socialNeeds
    def handleMessage(self, telegram):
        if(self.stateMachine.globalState.onMessage(self, telegram)):
            pass
        else:
            self.stateMachine.currentState.onMessage(self, telegram)