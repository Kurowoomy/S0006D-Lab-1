import EntityManager
import States
import random
import TimeManager
import Enumerations


class Telegram:
    def __init__(self, senderEntity, recieverEntity, msg, dispatchTime, extraInfo):
        self.senderEntity = senderEntity
        self.recieverEntity = recieverEntity
        self.msg = msg
        self.dispatchTime = dispatchTime
        self.extraInfo = extraInfo

class MessageDispatcher:
    priorityQ = []

    def dispatchMessage(self, meetupTime, senderEntity, recieverEntity, msg, extraInfo):
        telegram = Telegram(senderEntity, recieverEntity, msg, meetupTime, extraInfo)
        if(TimeManager.TimeManager.currentTime == meetupTime or msg == Enumerations.message_type.msg_SMS or msg == Enumerations.message_type.msg_cantCome):
            recieverEntity.handleMessage(telegram)
        else:
            MessageDispatcher.priorityQ.append(telegram)
    def dispatchDelayedMessages(self):
        self.amount = len(MessageDispatcher.priorityQ) - 1
        while(self.amount >= 0):
            if(MessageDispatcher.priorityQ[self.amount].dispatchTime == TimeManager.TimeManager.currentTime):
                MessageDispatcher.priorityQ[self.amount].recieverEntity.handleMessage(MessageDispatcher.priorityQ[self.amount])
                MessageDispatcher.priorityQ.remove(MessageDispatcher.priorityQ[self.amount])
            self.amount -= 1
        
                
        

    def decideMeetupTime(self):
        return random.randint(6, 23)
    def decideMeetupLocation(self):
        return random.choice(list(Enumerations.location_type))