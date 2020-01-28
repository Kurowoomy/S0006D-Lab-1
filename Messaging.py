import EntityManager


class Telegram:
    def __init__(self, senderEntity, recieverEntity, msg, time, location):
        self.senderEntity = senderEntity
        self.recieverEntity = recieverEntity
        self.msg = msg

class MessageDispatcher:
    def dispatchMessage(self, telegram):
        self.reciever = EntityManager.EntityManager.entityList[telegram.recieverEntity]
        self.reciever.handleMessage(telegram)