import Enumerations
import StateMachine
import States

class BaseGameEntity:
    nextValidID = 0
    def __init__(self, ID):
        self.setID(ID)
    def setID(self, ID):
        if(ID >= BaseGameEntity.nextValidID):
            BaseGameEntity.nextValidID += 1
            self.ID = id
    def changeLocation(self, newLocation):
        self.location = newLocation

class Student(BaseGameEntity):
    def __init__(self, ID, name, location, fatigue, hunger):
        BaseGameEntity.__init__(self, ID)
        self.stateMachine = StateMachine.StateMachine(self)
        self.stateMachine.SetCurrentState(States.Studying)
        self.stateMachine.SetGlobalState(States.StudentsGlobalState)
        self.name = name
        self.location = location
        self.fatigue = fatigue
        self.hunger = hunger
        
class Worker(BaseGameEntity):
    def __init__(self, ID):
        BaseGameEntity.__init__(self, ID)

