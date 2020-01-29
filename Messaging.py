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
        if(TimeManager.TimeManager.currentTime == meetupTime or msg == Enumerations.message_type.msg_SMS):
            recieverEntity.handleMessage(telegram)
        else:
            MessageDispatcher.priorityQ.append(telegram)
    def dispatchDelayedMessages(self):
        for telegram in MessageDispatcher.priorityQ:
            if(telegram.dispatchTime == TimeManager.TimeManager.currentTime):
                telegram.recieverEntity.handleMessage(telegram)

    def decideMeetupTime(self):
        return random.randint(6, 23)
    def decideMeetupLocation(self):
        return random.choice(list(Enumerations.location_type))