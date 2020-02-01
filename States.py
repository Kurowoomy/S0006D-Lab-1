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
            if(isinstance(character.stateMachine.previousState, Eating) and not isinstance(character.stateMachine.currentState, Shopping) and character.hunger < 5):
                pass
            else:
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



class WorkerGlobalState(State):
    #when entity recieves a message, return True if successful
    def onMessage(self, character, telegram):
        dispatcher = Messaging.MessageDispatcher()

        #can't read any SMS if dead
        if(not character.alive):
            print(character.name, ": Dead.")
            if(TimeManager.TimeManager.currentTime in character.appointments): #remove appointment if dead
                character.appointments.pop(TimeManager.TimeManager.currentTime)
            for entity in EntityManager.EntityManager.entityList: #let friends know entity can't come to appointment
                if(character.stateMachine.occupation == entity.stateMachine.occupation and EntityManager.EntityManager.workers > 1):
                    if(entity == character):
                        pass
                    else:
                        print(character.name, ": Letting", entity.name, "know they're dead")
                        dispatcher.dispatchMessage(None, character, entity, Enumerations.message_type.msg_cantCome, None)
            return False

        #recieves new appointment
        elif(telegram.msg == Enumerations.message_type.msg_SMS):
            print(character.name, ": Checking SMS")
            dispatcher.dispatchMessage(telegram.dispatchTime, character, character, Enumerations.message_type.msg_meetUp, telegram.extraInfo)
            if(telegram.dispatchTime in character.appointments):
                character.appointments[telegram.dispatchTime] += 1
            else:
                character.appointments[telegram.dispatchTime] = EntityManager.EntityManager.workers
            return True

        #time to socialize
        elif(telegram.msg == Enumerations.message_type.msg_meetUp and TimeManager.TimeManager.currentTime in character.appointments):
            print(character.name, ": Time to socialize")

            if(character.hunger >= 10):
                print(character.name, ": Too hungry to go")
                character.appointments.pop(TimeManager.TimeManager.currentTime)
                for entity in EntityManager.EntityManager.entityList: #let friends know entity can't come to appointment
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

        #gets message saying a friend can't come to appointment
        elif(telegram.msg == Enumerations.message_type.msg_cantCome):
            print(character.name, ": It seems", telegram.senderEntity.name, "can't come")
            if(TimeManager.TimeManager.currentTime in character.appointments):
                character.appointments[TimeManager.TimeManager.currentTime] -= 1
            return True

        return False

    #runs every update before another state
    def execute(self, character):
        dispatcher = Messaging.MessageDispatcher()
        
        #always increase these stats except in their respective state
        if(not character.isSocializing):
            character.socialNeeds += 1
        if(not character.isEating):
            character.hunger += 1

        #priorities of global events for entity:
        #1. dying of hunger
        if(character.hunger >= 18):
            print(character.name, ": Died of hunger")
            character.alive = False
            EntityManager.EntityManager.workers -= 1
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Dead)

        #2. falling asleep
        elif(character.fatigue >= 28):
            print(character.name, ": Fatigue level critical")
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Sleeping)

        #3. forcing them to sleep when it's nighttime
        elif((TimeManager.TimeManager.currentTime >= 0 and TimeManager.TimeManager.currentTime <= 5) and not character.sleeping):
            print(character.name, ": Time to sleep")
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Sleeping)

        #4. feeling lonely
        elif(character.socialNeeds >= 12 and len(character.appointments) <= 0):
            print(character.name, ": Feeling lonely")
            
            if(EntityManager.EntityManager.workers > 1): #set up appointment if entity has friends
                dispatcher = Messaging.MessageDispatcher()
                meetupTime = dispatcher.decideMeetupTime()
                self.meetupLocation = dispatcher.decideMeetupLocation(character.stateMachine.occupation)

                if(TimeManager.TimeManager.currentTime in character.appointments):
                    character.appointments[meetupTime] += 1
                else:
                    character.appointments[meetupTime] = 1

                for entity in EntityManager.EntityManager.entityList: #tell friends and itself about the appointment

                    if(character.stateMachine.occupation == entity.stateMachine.occupation and entity.alive):
                        if(entity == character):
                            dispatcher.dispatchMessage(meetupTime, character, character, Enumerations.message_type.msg_meetUp, self.meetupLocation)
                        else:
                            print(character.name, ": Sending SMS to", entity.name)
                            dispatcher.dispatchMessage(meetupTime, character, entity, Enumerations.message_type.msg_SMS, self.meetupLocation)
                            if(meetupTime in character.appointments):
                                character.appointments[meetupTime] += 1

        #5. check if entity can enter the state Socializing
        elif(character.isSocializing):
            if(TimeManager.TimeManager.currentTime in character.appointments):

                if(character.appointments[TimeManager.TimeManager.currentTime] <= 1):
                    print(character.name, ": No one is free :(")
                    character.appointments.pop(TimeManager.TimeManager.currentTime)
                    character.isSocializing = False
                else:
                    self.checkLocationChangeState(character, self.meetupLocation)
                    socialState = Socializing()
                    #**Socializing executes in the global state since they need to
                    #**be able to socialize while doing another task, eg. eating.
                    socialState.execute(character)

#almost identical to WorkerGlobalState except EntityManager.EntityManager.workers is changed to EntityManager.EntityManager.students
class StudentGlobalState(State):
    #when entity recieves a message, return True if successful
    def onMessage(self, character, telegram):
        dispatcher = Messaging.MessageDispatcher()

        #can't read any SMS if dead
        if(not character.alive):
            print(character.name, ": Dead.")
            if(TimeManager.TimeManager.currentTime in character.appointments): #remove appointment if dead
                character.appointments.pop(TimeManager.TimeManager.currentTime)
            for entity in EntityManager.EntityManager.entityList: #let friends know entity can't come to appointment
                if(character.stateMachine.occupation == entity.stateMachine.occupation and EntityManager.EntityManager.students > 1):
                    if(entity == character):
                        pass
                    else:
                        print(character.name, ": Letting", entity.name, "know they're dead")
                        dispatcher.dispatchMessage(None, character, entity, Enumerations.message_type.msg_cantCome, None)
            return False

        #recieves new appointment
        elif(telegram.msg == Enumerations.message_type.msg_SMS):
            print(character.name, ": Checking SMS")
            dispatcher.dispatchMessage(telegram.dispatchTime, character, character, Enumerations.message_type.msg_meetUp, telegram.extraInfo)
            if(telegram.dispatchTime in character.appointments):
                character.appointments[telegram.dispatchTime] += 1
            else:
                character.appointments[telegram.dispatchTime] = EntityManager.EntityManager.students
            return True

        #time to socialize
        elif(telegram.msg == Enumerations.message_type.msg_meetUp and TimeManager.TimeManager.currentTime in character.appointments):
            print(character.name, ": Time to socialize")

            if(character.hunger >= 10):
                print(character.name, ": Too hungry to go")
                character.appointments.pop(TimeManager.TimeManager.currentTime)
                for entity in EntityManager.EntityManager.entityList: #let friends know entity can't come to appointment
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

        #gets message saying a friend can't come to appointment
        elif(telegram.msg == Enumerations.message_type.msg_cantCome):
            print(character.name, ": It seems", telegram.senderEntity.name, "can't come")
            if(TimeManager.TimeManager.currentTime in character.appointments):
                character.appointments[TimeManager.TimeManager.currentTime] -= 1
            return True

        return False

    #runs every update before another state
    def execute(self, character):
        dispatcher = Messaging.MessageDispatcher()
        
        #always increase these stats except in their respective state
        if(not character.isSocializing):
            character.socialNeeds += 1
        if(not character.isEating):
            character.hunger += 1

        #priorities of global events for entity:
        #1. dying of hunger
        if(character.hunger >= 18):
            print(character.name, ": Died of hunger")
            character.alive = False
            EntityManager.EntityManager.students -= 1
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Dead)

        #2. falling asleep
        elif(character.fatigue >= 28):
            print(character.name, ": Fatigue level critical")
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Sleeping)

        #3. forcing them to sleep when it's nighttime
        elif((TimeManager.TimeManager.currentTime >= 0 and TimeManager.TimeManager.currentTime <= 5) and not character.sleeping):
            print(character.name, ": Time to sleep")
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Sleeping)

        #4. feeling lonely
        elif(character.socialNeeds >= 12 and len(character.appointments) <= 0):
            print(character.name, ": Feeling lonely")
            
            if(EntityManager.EntityManager.students > 1): #set up appointment if entity has friends
                dispatcher = Messaging.MessageDispatcher()
                meetupTime = dispatcher.decideMeetupTime()
                self.meetupLocation = dispatcher.decideMeetupLocation(character.stateMachine.occupation)

                if(TimeManager.TimeManager.currentTime in character.appointments):
                    character.appointments[meetupTime] += 1
                else:
                    character.appointments[meetupTime] = 1

                for entity in EntityManager.EntityManager.entityList: #tell friends and itself about the appointment

                    if(character.stateMachine.occupation == entity.stateMachine.occupation and entity.alive):
                        if(entity == character):
                            dispatcher.dispatchMessage(meetupTime, character, character, Enumerations.message_type.msg_meetUp, self.meetupLocation)
                        else:
                            print(character.name, ": Sending SMS to", entity.name)
                            dispatcher.dispatchMessage(meetupTime, character, entity, Enumerations.message_type.msg_SMS, self.meetupLocation)
                            if(meetupTime in character.appointments):
                                character.appointments[meetupTime] += 1

        #5. check if entity can enter the state Socializing
        elif(character.isSocializing):
            if(TimeManager.TimeManager.currentTime in character.appointments):

                if(character.appointments[TimeManager.TimeManager.currentTime] <= 1):
                    print(character.name, ": No one is free :(")
                    character.appointments.pop(TimeManager.TimeManager.currentTime)
                    character.isSocializing = False
                else:
                    self.checkLocationChangeState(character, self.meetupLocation)
                    socialState = Socializing()
                    #**Socializing executes in the global state since they need to
                    #**be able to socialize while doing another task, eg. eating.
                    socialState.execute(character)



#sets the socialNeeds to 0 in one execute
class Socializing(State):
    def enter(self, character):
        pass
    def execute(self, character):
        print(character.name, ": Socializing!")
        character.socialNeeds = 0
        if(TimeManager.TimeManager.currentTime in character.appointments):
            character.appointments.pop(TimeManager.TimeManager.currentTime)
    def exit(self, character):
        pass

#fatigue and money increase fast
class Mining(Working):
    def enter(self, character):
        if(character.location != Enumerations.location_type.mines):
            print(character.name, ": Going to the mines")
            character.changeLocation(Enumerations.location_type.mines)
    def execute(self, character):
        character.fatigue += 2
        character.money += 2
        character.shovels -= 1
        character.drinkingNeeds += 1
        print(character.name, ": Mining...")
        character.checkIfEnoughMoney(character.money, 10)
        State.execute(self, character)
        #switch to Eating
        if(character.hunger >= 5 and character.canShop):
            print(character.name, ": Taking a food break")
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Eating)
        #switch to Drinking
        elif(TimeManager.TimeManager.currentTime >=21 and character.drinkingNeeds >= 12):
            print(character.name, ": Need a drink")
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Drinking)
    def exit(self, character):
        print(character.name, ": Leaving the mines")

#drinkingNeeds increases fast
class Studying(Working):
    def enter(self, character):
        if(character.location != Enumerations.location_type.school):
            print(character.name, ": Going to school")
            character.changeLocation(Enumerations.location_type.school)
    def execute(self, character):
        character.fatigue += 1
        character.money += 1
        character.pencils -= 1
        character.drinkingNeeds += 2
        print(character.name, ": Studying...")
        character.checkIfEnoughMoney(character.money, 10)
        State.execute(self, character)
        #switch to Eating
        if(character.hunger >= 5 and character.canShop):
            print(character.name, ": Taking a food break")
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Eating)
        #switch to Drinking
        elif(TimeManager.TimeManager.currentTime >=21 and character.drinkingNeeds >= 12):
            print(character.name, ": Need a drink")
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Drinking)
    def exit(self, character):
        print(character.name, ": Leaving school")

class Sleeping(State):
    def enter(self, character):
        if(character.location != Enumerations.location_type.home):
            print(character.name, ": Going home")
            character.changeLocation(Enumerations.location_type.home)
        character.sleeping = True
    def execute(self, character):
        #switch to Eating if hungry, else to Working
        if(character.fatigue <= 0 and not (TimeManager.TimeManager.currentTime >= 0 and TimeManager.TimeManager.currentTime <= 5)):
            print(character.name, ": Slept well")
            if(character.isSocializing):
                State.execute(self, character)
            else:
                if(character.hunger >= 5):
                    character.stateMachine.changeState(Eating)
                else:
                    character.stateMachine.changeState(Working)
        #force them to wake up at 8 o'clock
        elif(TimeManager.TimeManager.currentTime == 8):
            print(character.name, ": Still tired")
            if(character.isSocializing):
                State.execute(self, character)
            else:
                if(character.hunger >= 5):
                    character.stateMachine.changeState(Eating)
                else:
                    character.stateMachine.changeState(Working)
        else:
            character.fatigue -= 3
            print(character.name, ": ZZZZ...")
            State.execute(self, character)
    def exit(self, character):
        print(character.name, ": Leaving bed")
        character.sleeping = False

#sets the hunger to 0 in one execute
class Eating(State):
    def enter(self, character):
        if(character.location != Enumerations.location_type.cafeteria):
            print(character.name, ": Going to cafeteria")
            character.isEating = True
            character.changeLocation(Enumerations.location_type.cafeteria)
            #switch to Shopping
            if(character.foodInventory <= 0):
                print(character.name, ": Food inventory is empty")
                if(character.isSocializing):
                    State.execute(self, character)
                else:
                    character.stateMachine.changeState(Shopping)
    def execute(self, character):
        #switch to Working
        print(character.name, ": Eating...")
        character.hunger = 0
        character.fatigue += 1
        character.foodInventory -= 1
        if(character.isSocializing):
            State.execute(self, character)
        else:
            character.stateMachine.changeState(Working)
    def exit(self, character):
        character.isEating = False

class Shopping(State):
    def enter(self, character):
        if(character.location != Enumerations.location_type.shop):
            print(character.name, ": Going to the shop")
            character.changeLocation(Enumerations.location_type.shop)
    def execute(self, character):
        self.amount = 5
        #revert to Eating
        #buy food
        if(character.money >= self.amount*2):
            print(character.name, ": Stacking up on food")
            character.foodInventory += self.amount
            character.money -= self.amount*2
            character.fatigue += 1
            character.drinkingNeeds += 1
            #buy work material
            if(character.money >= self.amount*3):
                if(character.stateMachine.occupation == Studying):
                    print(character.name, ": Stacking up on pencils")
                    character.pencils += self.amount*3
                    character.money -= self.amount*3
                elif(character.stateMachine.occupation == Mining):
                    print(character.name, ": Stacking up on shovels")
                    character.shovels += self.amount*3
                    character.money -= self.amount*3
            character.isSocializing = False
            character.stateMachine.revertToPreviousState()
        #switch to Working
        else:
            print(character.name, ": Not enough money")
            character.canShop = False
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Working)
    def exit(self, character):
        pass
        
#won't leave this state if entered
class Dead(State):
    def enter(self, character):
        pass
    def execute(self, character):
        print(character.name, ": Lying dead on the ground")
    def exit(self, character):
        pass

class Drinking(State):
    def enter(self, character):
        if(character.location != Enumerations.location_type.bar):
            print(character.name, ": Going to the bar")
            character.changeLocation(Enumerations.location_type.bar)
    def execute(self, character):
        #switch to Sleeping
        if(character.drinkingNeeds <= 0):
            print(character.name, ": Feeling refreshed")
            if(character.isSocializing):
                State.execute(self, character)
            else:
                character.stateMachine.changeState(Sleeping)
        if(not character.isSocializing):
            character.socialNeeds += 1 #feeling extra lonely when drinking alone
        character.drinkingNeeds -= 11
        character.fatigue += 1
        print(character.name, ": Drinking")
        State.execute(self, character)
    def exit(self, character):
        pass