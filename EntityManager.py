import States

#keeps track of all the students and workers in the game
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