import Enumerations
import Entities
import StateMachine
import EntityManager
import TimeManager
import States
import Messaging


student1 = Entities.Student(0, "Student 1", Enumerations.location_type.school, 4, 10, 0, 1, 0, 100, 0)
student2 = Entities.Student(1, "Student 2", Enumerations.location_type.school, 0, 0, 8, 15, 15, 0, 10)
memberOfSociety1 = Entities.Worker(2, "Miner 1", Enumerations.location_type.mines, 0, 10, 0, 15, 0, 0, 0)
memberOfSociety2 = Entities.Worker(3, "Miner 2", Enumerations.location_type.mines, 0, 0, 0, 15, 0, 0, 0)

EntityManager.EntityManager().registerEntity(student1)
EntityManager.EntityManager().registerEntity(student2)
EntityManager.EntityManager().registerEntity(memberOfSociety1)
EntityManager.EntityManager().registerEntity(memberOfSociety2)
dispatcher = Messaging.MessageDispatcher()

i = 0
while(i < 35):
    #låt det gå 1 h per loop
    #TODO: balansera, börja med sleeping
    TimeManager.time.sleep(1)
    i += 1
    print("CurrentTime is %d:00" % TimeManager.TimeManager.currentTime)
    
    dispatcher.dispatchDelayedMessages()

    student1.stateMachine.update()
    print("")
    print("")
    student2.stateMachine.update()
    print("")
    print("")
    memberOfSociety1.stateMachine.update()
    print("")
    print("")
    memberOfSociety2.stateMachine.update()
    print("")
    print("---------------")
    print("")

    TimeManager.TimeManager.currentTime += 1
    if(TimeManager.TimeManager.currentTime >= 24):
        TimeManager.TimeManager.currentTime = 0