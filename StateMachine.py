import States

class StateMachine:
    def __init__(self, entity):
        self.owner = entity
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
        if(self.globalState):
            self.globalState.execute(self.owner)
        if(self.currentState):
            self.currentState.execute(self.owner)

    def changeState(self, newState):
        #previousState funkar ej eftersom jag skapar nya instanser varje gång förutom vid revert
        self.previousState = self.currentState
        self.currentState.exit(self.owner)
        self.currentState = newState()
        self.currentState.enter(self.owner)
    def revertToPreviousState(self):
        self.newState = self.previousState
        self.previousState = self.currentState
        self.currentState.exit(self.owner)
        self.currentState = self.newState
        self.currentState.enter(self.owner)
        #self.changeState(self.previousState)
        
