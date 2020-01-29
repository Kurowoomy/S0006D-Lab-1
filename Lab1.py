import Enumerations
import Entities
import StateMachine
import EntityManager
import TimeManager
import States
import Messaging


student1 = Entities.Student(0, "Student 1", Enumerations.location_type.school, 0, 0, 0, 15, 0, 0, 0)
student2 = Entities.Student(0, "Student 2", Enumerations.location_type.school, 0, 0, 0, 15, 0, 0, 0)
memberOfSociety1 = Entities.Worker(1, "Miner 1", Enumerations.location_type.school, 0, 0, 0, 15, 0, 0, 0)

EntityManager.EntityManager().registerEntity(student1)
EntityManager.EntityManager().registerEntity(student2)
EntityManager.EntityManager().registerEntity(memberOfSociety1)
dispatcher = Messaging.MessageDispatcher()

i = 0
while(i < 35):
    #låt det gå 1 h per loop
    i += 1
    print("CurrentTime is %d:00" % TimeManager.TimeManager.currentTime)
    
    dispatcher.dispatchDelayedMessages()

    student1.stateMachine.update()
    print("")
    student2.stateMachine.update()
    print("")
    memberOfSociety1.stateMachine.update()
    print("")
    print("")

    TimeManager.TimeManager.currentTime += 1
    if(TimeManager.TimeManager.currentTime >= 24):
        TimeManager.TimeManager.currentTime = 0