import States

class StateMachine:
    def __init__(self, entity, occupation):
        self.owner = entity
        self.occupation = occupation
        self.currentState = None
        self.previousState = None
        self.globalState = None

    def SetCurrentState(self, state):
        self.currentState = state()
    def SetGlobalState(self, state):
        self.globalState = state()
    def SetPreviousState(self, state):
        self.previousState = state()

    def update(self):
        if(self.owner.alive):
            if(self.globalState):
                self.globalState.execute(self.owner)
                print("")
        if(self.currentState):
            self.currentState.execute(self.owner)


    def changeState(self, newState):
        self.previousState = self.currentState
        self.currentState.exit(self.owner)
        if(newState == States.Working):
            self.currentState = self.occupation()
        else:
            self.currentState = newState()
        self.currentState.enter(self.owner)
    def revertToPreviousState(self):
        self.newState = self.previousState
        self.previousState = self.currentState
        self.currentState.exit(self.owner)
        self.currentState = self.newState
        self.currentState.enter(self.owner)
        
