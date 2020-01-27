import Enumerations
import Messaging

class State:
    def enter(self, character):
        pass
    def execute(self, character):
        pass
    def exit(self, character):
        pass



class StudentsGlobalState(State):
    def OnMessage(self, character, telegram):
        if(telegram.msg == Enumerations.message_type.msg_meetUp):
            pass
        elif(telegram.msg == Enumerations.message_type.msg_tooHungry):
            pass
    def execute(self, character):
        if(character.fatigue >= 5):
            print(character.name, ": Fatigue level critical")
            character.stateMachine.changeState(Sleeping)
        

class Studying(State):
    def enter(self, character):
        if(character.location != Enumerations.location_type.school):
            print(character.name, ": Going to school")
            character.changeLocation(Enumerations.location_type.school)
    def execute(self, character):
        character.fatigue += 1
        character.hunger += 1
        if(character.hunger >= 4):
            print(character.name, ": Taking a food break.")
            character.stateMachine.changeState(Eating)
        else:
            print(character.name, ": Studying...")
    def exit(self, character):
        print(character.name, ": Leaving school")

class Sleeping(State):
    def enter(self, character):
        if(character.location != Enumerations.location_type.home):
            print(character.name, ": Going home")
            character.changeLocation(Enumerations.location_type.home)
    def execute(self, character):
        character.fatigue -= 1
        character.hunger += 1
        if(character.fatigue <= 0):
            print(character.name, ": Slept well")
            character.stateMachine.changeState(Studying)
        else:
            print(character.name, ": ZZZZ...")
    def exit(self, character):
        print(character.name, ": Leaving bed.")

class Eating(State):
    def enter(self, character):
        if(character.location != Enumerations.location_type.restaurant):
            print(character.name, ": Going to restaurant")
            character.changeLocation(Enumerations.location_type.restaurant)
    def execute(self, character):
        character.hunger -= 2
        if(character.hunger <= 0):
            print(character.name, ": Full and returning to previous task")
            character.stateMachine.revertToPreviousState()
        else:
            print(character.name, ": Eating")
    def exit(self, character):
        print(character.name, ": Leaving restaurant")

class Shopping(State):
    def enter(self, character):
        pass
    def execute(self, character):
        pass
    def exit(self, character):
        pass
        