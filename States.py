import Enumerations
import Messaging
import TimeManager
import EntityManager
import Entities

class State:
    def enter(self, character):
        pass
    def execute(self, character):
        if(character.isSocializing):
            character.stateMachine.revertToPreviousState()
            character.isSocializing = False
    def exit(self, character):
        pass
    def onMessage(self, character, telegram):
        return False
    def checkLocationChangeState(self, character, location):
        if(character.location != location):
            print(character.name, ": Going to our meetup spot")
            character.changeLocation(location)
            if(location == Enumerations.location_type.home):
                character.stateMachine.changeState(Sleeping)
            elif(location == Enumerations.location_type.school):
                character.stateMachine.changeState(Studying)
            elif(location == Enumerations.location_type.mines):
                character.stateMachine.changeState(Mining)
            elif(location == Enumerations.location_type.shop):
                character.stateMachine.changeState(Shopping)
            elif(location == Enumerations.location_type.cafeteria):
                character.stateMachine.changeState(Eating)
            elif(location == Enumerations.location_type.bar):
                character.stateMachine.changeState(Drinking)

class Working(State):
    def enter(self, character):
        pass
    def execute(self, character):
        pass
    def exit(self, character):
        pass


#gör som studentglobalstate
class WorkerGlobalState(State):
    def onMessage(self, character, telegram):
        dispatcher = Messaging.MessageDispatcher()
        if(not character.alive):
            print(character.name, ": Dead.")
            if(TimeManager.TimeManager.currentTime in character.appointments):
                character.appointments.pop(TimeManager.TimeManager.currentTime)
            for entity in EntityManager.EntityManager.entityList:
                if(character.stateMachine.occupation == entity.stateMachine.occupation and EntityManager.EntityManager.workers > 1):
                    if(entity == character):
                        pass
                    else:
                        print(character.name, ": Letting", entity.name, "know they're dead")
                        dispatcher.dispatchMessage(None, character, entity, Enumerations.message_type.msg_cantCome, None)
            return False
        elif(telegram.msg == Enumerations.message_type.msg_SMS):
            print(character.name, ": Checking SMS")
            dispatcher.dispatchMessage(telegram.dispatchTime, character, character, Enumerations.message_type.msg_meetUp, telegram.extraInfo)
            if(telegram.dispatchTime in character.appointments):
                character.appointments[telegram.dispatchTime] += 1
            else:
                character.appointments[telegram.dispatchTime] = EntityManager.EntityManager.workers
            return True
        elif(telegram.msg == Enumerations.message_type.msg_meetUp):
            print(character.name, ": Time to socialize")
            if(character.hunger >= 10):
                print(character.name, ": Too hungry to go")
                character.appointments.pop(TimeManager.TimeManager.currentTime)
                for entity in EntityManager.EntityManager.entityList:
                    if(character.stateMachine.occupation == entity.stateMachine.occupation and EntityManager.EntityManager.workers > 1):
                        if(entity == character):
                            pass
                        else:
                            print(character.name, ": Letting", entity.name, "know they're not coming")
                            dispatcher.dispatchMessage(None, character, entity, Enumerations.message_type.msg_cantCome, None)
            else:
                self.meetupLocation = telegram.extraInfo
                character.isSocializing = True
            return True
        elif(telegram.msg == Enumerations.message_type.msg_cantCome):
            print(character.name, ": It seems", telegram.senderEntity.name, "can't come")
            character.appointments[TimeManager.TimeManager.currentTime] -= 1
            return True
        return False
    def execute(self, character):
        dispatcher = Messaging.MessageDispatcher()
        if(character.hunger >= 24):
            print(character.name, ": Died of hunger")
            character.alive = False
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Dead)
        elif(character.fatigue >= 17):
            print(character.name, ": Fatigue level critical")
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Sleeping)
        elif((TimeManager.TimeManager.currentTime >= 0 and TimeManager.TimeManager.currentTime <= 5) and not character.sleeping):
            print(character.name, ": Time to sleep")
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Sleeping)
        elif(character.socialNeeds >= 12 and len(character.appointments) <= 0):
            print(character.name, ": Feeling lonely")
            dispatcher = Messaging.MessageDispatcher()
            meetupTime = dispatcher.decideMeetupTime()
            self.meetupLocation = dispatcher.decideMeetupLocation(character.stateMachine.occupation)
            if(TimeManager.TimeManager.currentTime in character.appointments):
                character.appointments[meetupTime] += 1
            else:
                character.appointments[meetupTime] = 1
            for entity in EntityManager.EntityManager.entityList:
                if(character.stateMachine.occupation == entity.stateMachine.occupation and EntityManager.EntityManager.workers > 1):
                    if(entity == character):
                        dispatcher.dispatchMessage(meetupTime, character, character, Enumerations.message_type.msg_meetUp, self.meetupLocation)
                    else:
                        print(character.name, ": Sending SMS to", entity.name)
                        dispatcher.dispatchMessage(meetupTime, character, entity, Enumerations.message_type.msg_SMS, self.meetupLocation)
                        character.appointments[meetupTime] += 1
        elif(character.isSocializing):
            if(TimeManager.TimeManager.currentTime in character.appointments):
                if(character.appointments[TimeManager.TimeManager.currentTime] <= 1):
                    print(character.name, ": No one is free :(")
                    character.appointments.pop(TimeManager.TimeManager.currentTime)
                    character.isSocializing = False
                else:
                    self.checkLocationChangeState(character, self.meetupLocation)
                    socialState = Socializing()
                    socialState.execute(character)

class StudentGlobalState(State):
    def onMessage(self, character, telegram):
        dispatcher = Messaging.MessageDispatcher()
        if(not character.alive):
            print(character.name, ": Dead.")
            if(TimeManager.TimeManager.currentTime in character.appointments):
                character.appointments.pop(TimeManager.TimeManager.currentTime)
            for entity in EntityManager.EntityManager.entityList:
                if(character.stateMachine.occupation == entity.stateMachine.occupation and EntityManager.EntityManager.students > 1):
                    if(entity == character):
                        pass
                    else:
                        print(character.name, ": Letting", entity.name, "know they're dead")
                        dispatcher.dispatchMessage(None, character, entity, Enumerations.message_type.msg_cantCome, None)
            return False
        elif(telegram.msg == Enumerations.message_type.msg_SMS):
            print(character.name, ": Checking SMS")
            dispatcher.dispatchMessage(telegram.dispatchTime, character, character, Enumerations.message_type.msg_meetUp, telegram.extraInfo)
            if(telegram.dispatchTime in character.appointments):
                character.appointments[telegram.dispatchTime] += 1
            else:
                character.appointments[telegram.dispatchTime] = EntityManager.EntityManager.students
            return True
        elif(telegram.msg == Enumerations.message_type.msg_meetUp):
            print(character.name, ": Time to socialize")
            if(character.hunger >= 10):
                print(character.name, ": Too hungry to go")
                character.appointments.pop(TimeManager.TimeManager.currentTime)
                for entity in EntityManager.EntityManager.entityList:
                    if(character.stateMachine.occupation == entity.stateMachine.occupation and EntityManager.EntityManager.students > 1):
                        if(entity == character):
                            pass
                        else:
                            print(character.name, ": Letting", entity.name, "know they're not coming")
                            dispatcher.dispatchMessage(None, character, entity, Enumerations.message_type.msg_cantCome, None)
            else:
                self.meetupLocation = telegram.extraInfo
                character.isSocializing = True
            return True
        elif(telegram.msg == Enumerations.message_type.msg_cantCome):
            print(character.name, ": It seems", telegram.senderEntity.name, "can't come")
            character.appointments[TimeManager.TimeManager.currentTime] -= 1
            return True
        return False
    def execute(self, character):
        dispatcher = Messaging.MessageDispatcher()
        if(character.hunger >= 24):
            print(character.name, ": Died of hunger")
            character.alive = False
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Dead)
        elif(character.fatigue >= 17):
            print(character.name, ": Fatigue level critical")
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Sleeping)
        elif((TimeManager.TimeManager.currentTime >= 0 and TimeManager.TimeManager.currentTime <= 5) and not character.sleeping):
            print(character.name, ": Time to sleep")
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Sleeping)
        elif(character.socialNeeds >= 12 and len(character.appointments) <= 0):
            print(character.name, ": Feeling lonely")
            dispatcher = Messaging.MessageDispatcher()
            meetupTime = dispatcher.decideMeetupTime()
            self.meetupLocation = dispatcher.decideMeetupLocation(character.stateMachine.occupation)
            if(TimeManager.TimeManager.currentTime in character.appointments):
                character.appointments[meetupTime] += 1
            else:
                character.appointments[meetupTime] = 1
            for entity in EntityManager.EntityManager.entityList:
                if(character.stateMachine.occupation == entity.stateMachine.occupation and EntityManager.EntityManager.students > 1):
                    if(entity == character):
                        dispatcher.dispatchMessage(meetupTime, character, character, Enumerations.message_type.msg_meetUp, self.meetupLocation)
                    else:
                        print(character.name, ": Sending SMS to", entity.name)
                        dispatcher.dispatchMessage(meetupTime, character, entity, Enumerations.message_type.msg_SMS, self.meetupLocation)
                        character.appointments[meetupTime] += 1
        elif(character.isSocializing):
            if(TimeManager.TimeManager.currentTime in character.appointments):
                if(character.appointments[TimeManager.TimeManager.currentTime] <= 1):
                    print(character.name, ": No one is free :(")
                    character.appointments.pop(TimeManager.TimeManager.currentTime)
                    character.isSocializing = False
                else:
                    self.checkLocationChangeState(character, self.meetupLocation)
                    socialState = Socializing()
                    socialState.execute(character)



class Socializing(State):
    def enter(self, character):
        pass
    def execute(self, character):
        print(character.name, ": Socializing!")
        character.socialNeeds = 0
        if(TimeManager.TimeManager.currentTime in character.appointments):
            character.appointments.pop(TimeManager.TimeManager.currentTime)
        ###character.willMeetUp = False
    def exit(self, character):
        pass

class Mining(Working):
    def enter(self, character):
        if(character.location != Enumerations.location_type.mines):
            print(character.name, ": Going to the mines")
            character.changeLocation(Enumerations.location_type.mines)
    def execute(self, character):
        if(character.hunger >= 5 and character.canShop):
            print(character.name, ": Taking a food break")
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Eating)
        elif(TimeManager.TimeManager.currentTime >=21 and character.drinkingNeeds >= 10):
            print(character.name, ": Need a drink")
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Drinking)
        else:        
            character.fatigue += 1
            character.hunger += 1
            character.money += 3
            character.socialNeeds += 1
            character.shovels -= 1
            character.drinkingNeeds += 1
            print(character.name, ": Mining...")
            character.checkIfEnoughMoney(character.money, 15)
            State.execute(self, character)
    def exit(self, character):
        print(character.name, ": Leaving the mines")

class Studying(Working):
    def enter(self, character):
        if(character.location != Enumerations.location_type.school):
            print(character.name, ": Going to school")
            character.changeLocation(Enumerations.location_type.school)
    def execute(self, character):
        if(character.hunger >= 5 and character.canShop):
            print(character.name, ": Taking a food break")
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Eating)
        elif(TimeManager.TimeManager.currentTime >=21 and character.drinkingNeeds >= 10):
            print(character.name, ": Need a drink")
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Drinking)
        else:    
            character.fatigue += 1
            character.hunger += 1
            character.money += 2
            character.socialNeeds += 1
            character.pencils -= 1
            character.drinkingNeeds += 2
            print(character.name, ": Studying...")
            character.checkIfEnoughMoney(character.money, 15)
            State.execute(self, character)
    def exit(self, character):
        print(character.name, ": Leaving school")

class Sleeping(State):
    def enter(self, character):
        if(character.location != Enumerations.location_type.home):
            print(character.name, ": Going home")
            character.changeLocation(Enumerations.location_type.home)
        character.sleeping = True
    def execute(self, character):
        if(character.fatigue <= 0):
            print(character.name, ": Slept well")
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Working)
        elif(TimeManager.TimeManager.currentTime == 8):
            print(character.name, ": Still tired")
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Working)
        else:
            character.fatigue -= 2
            character.hunger += 1
            character.socialNeeds += 1
            print(character.name, ": ZZZZ...")
            State.execute(self, character)
    def exit(self, character):
        print(character.name, ": Leaving bed")
        character.sleeping = False

class Eating(State):
    def enter(self, character):
        if(character.location != Enumerations.location_type.cafeteria):
            print(character.name, ": Going to cafeteria")
            character.changeLocation(Enumerations.location_type.cafeteria)
            if(character.foodInventory <= 0):
                print(character.name, ": Food inventory is empty")
                if(character.isSocializing):
                    State.execute(self, character)
                else:
                    character.stateMachine.changeState(Shopping)
    def execute(self, character):
        print(character.name, ": Eating...")
        character.hunger = 0
        character.fatigue += 1
        character.foodInventory -= 1
        if(character.isSocializing):
            State.execute(self, character)
        else:
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
            character.isSocializing = False
            character.stateMachine.revertToPreviousState()
        else:
            print(character.name, ": Not enough money")
            character.canShop = False
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Working)
    def exit(self, character):
        pass
        
class Dead(State):
    def enter(self, character):
        pass
    def execute(self, character):
        if(character.isSocializing):
                State.execute(self, character)
        else:
            print(character.name, ": Lying dead on the ground")
    def exit(self, character):
        pass

class Drinking(State):
    def enter(self, character):
        if(character.location != Enumerations.location_type.bar):
            print(character.name, ": Going to the bar")
            character.changeLocation(Enumerations.location_type.bar)
    def execute(self, character):
        if(character.drinkingNeeds <= 0):
            print(character.name, ": Feeling refreshed")
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Sleeping)
        character.drinkingNeeds -= 10
        character.socialNeeds += 1
        print(character.name, ": Drinking")
        State.execute(self, character)
    def exit(self, character):
        pass