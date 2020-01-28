import Enumerations
import Messaging
import TimeManager

class State:
    def enter(self, character):
        pass
    def execute(self, character):
        pass
    def exit(self, character):
        pass

class Working(State):
    def enter(self, character):
        pass
    def execute(self, character):
        pass
    def exit(self, character):
        pass



class GlobalState(State):
    def OnMessage(self, character, telegram):
        if(not character.alive):
            print(character.name, ": Dead.")
        elif(telegram.msg == Enumerations.message_type.msg_meetUp):
            pass
        elif(telegram.msg == Enumerations.message_type.msg_tooHungry):
            pass
    def execute(self, character):
        if(character.hunger >= 24):
            print(character.name, ": Died of hunger")
            character.alive = False
            character.stateMachine.changeState(Dead)
        elif(character.fatigue >= 16):
            print(character.name, ": Fatigue level critical")
            character.stateMachine.changeState(Sleeping)
        elif(TimeManager.TimeManager.currentTime == 0):
            print(character.name, ": Time to sleep")
            character.stateMachine.changeState(Sleeping)
        
        
        

class Mining(Working):
    def enter(self, character):
        if(character.location != Enumerations.location_type.mines):
            print(character.name, ": Going to the mines")
            character.changeLocation(Enumerations.location_type.mines)
    def execute(self, character):
        character.fatigue += 1
        character.hunger += 1
        character.money += 3
        if(character.hunger >= 5 and character.canShop):
            print(character.name, ": Taking a food break")
            character.stateMachine.changeState(Eating)
        else:
            character.shovels -= 1
            print(character.name, ": Mining...")
            character.checkIfEnoughMoney(character.money, 15)
    def exit(self, character):
        print(character.name, ": Leaving the mines")

class Studying(Working):
    def enter(self, character):
        if(character.location != Enumerations.location_type.school):
            print(character.name, ": Going to school")
            character.changeLocation(Enumerations.location_type.school)
    def execute(self, character):
        character.fatigue += 1
        character.hunger += 1
        character.money += 2
        if(character.hunger >= 5 and character.canShop):
            print(character.name, ": Taking a food break")
            character.stateMachine.changeState(Eating)
        else:
            character.pencils -= 1
            print(character.name, ": Studying...")
            character.checkIfEnoughMoney(character.money, 15)
    def exit(self, character):
        print(character.name, ": Leaving school")

class Sleeping(State):
    def enter(self, character):
        if(character.location != Enumerations.location_type.home):
            print(character.name, ": Going home")
            character.changeLocation(Enumerations.location_type.home)
    def execute(self, character):
        character.fatigue -= 2
        character.hunger += 1
        if(character.fatigue <= 0):
            print(character.name, ": Slept well")
            character.stateMachine.changeState(Working)
        elif(TimeManager.TimeManager.currentTime == 8):
            print(character.name, ": Still tired")
            character.stateMachine.changeState(Working)
        else:
            print(character.name, ": ZZZZ...")
    def exit(self, character):
        print(character.name, ": Leaving bed")

class Eating(State):
    def enter(self, character):
        if(character.location != Enumerations.location_type.cafeteria):
            print(character.name, ": Going to cafeteria")
            character.changeLocation(Enumerations.location_type.cafeteria)
            if(character.foodInventory <= 0):
                print(character.name, ": Food inventory is empty")
                character.stateMachine.changeState(Shopping)
    def execute(self, character):
        print(character.name, ": Eating...")
        character.hunger = 0
        character.fatigue += 1
        character.foodInventory -= 1
        print(character.name, ": Full and returning to work")
        character.stateMachine.changeState(Working)
    def exit(self, character):
        pass

class Shopping(State):
    def enter(self, character):
        if(character.location != Enumerations.location_type.shop):
            print(character.name, ": Going to the shop")
            character.changeLocation(Enumerations.location_type.shop)
    def execute(self, character):
        self.amount = 5
        if(character.money >= self.amount*3):
            character.foodInventory += self.amount
            character.money -= self.amount
            if(character.stateMachine.occupation == Studying):
                print(character.name, ": Stacking up on food and pencils")
                character.pencils += self.amount*2
                character.money -= self.amount*2
            elif(character.stateMachine.occupation == Mining):
                print(character.name, ": Stacking up on food and shovels")
                character.shovels += 10
                character.money -= 10
            character.stateMachine.revertToPreviousState()
        else:
            print(character.name, ": Not enough money")
            character.canShop = False
            character.stateMachine.changeState(Working)
    def exit(self, character):
        pass
        
class Dead(State):
    def enter(self, character):
        pass
    def execute(self, character):
        print(character.name, ": Lying dead on the ground")
    def exit(self, character):
        pass

class Drinking(State):
    def enter(self, character):
        pass
    def execute(self, character):
        pass
    def exit(self, character):
        pass