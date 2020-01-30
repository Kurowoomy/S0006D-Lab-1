import States

class EntityManager:
    entityList = []
    students = 0
    workers = 0
    def registerEntity(self, entity):
        EntityManager.entityList.append(entity)
        if(entity.stateMachine.occupation == States.Studying):
            EntityManager.students += 1
        elif(entity.stateMachine.occupation == States.Mining):
            EntityManager.workers += 1
    def findEntityThroughID(self, ID):
        for x in self.entityList:
            if(self.entityList[x].ID == ID):
                return self.entityList[x]
        print("Entity with ID", ID, "not found")