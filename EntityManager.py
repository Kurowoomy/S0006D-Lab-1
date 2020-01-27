

class EntityManager:
    entityList = []
    def registerEntity(self, entity):
        self.entityList.append(entity)
    def findEntityThroughID(self, ID):
        for x in self.entityList:
            if(self.entityList[x].ID == ID):
                return self.entityList[x]
        print("Entity with ID", ID, "not found")