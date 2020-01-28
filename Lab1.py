import Enumerations
import Entities
import StateMachine
import EntityManager
import TimeManager
import States


student1 = Entities.Student(0, "Student 1", Enumerations.location_type.school, 0, 0, 0, 15, 0, 5)
memberOfSociety1 = Entities.Worker(1, "Miner 1", Enumerations.location_type.school, 0, 0, 0, 15, 0, 2)

EntityManager.EntityManager().registerEntity(student1)
EntityManager.EntityManager().registerEntity(memberOfSociety1)

i = 0
while(i < 50):
    #låt det gå 1 h per loop
    i += 1
    print("CurrentTime is %d:00" % TimeManager.TimeManager.currentTime)
    
    student1.stateMachine.update()
    print("")
    memberOfSociety1.stateMachine.update()
    print("")
    print("")

    TimeManager.TimeManager.currentTime += 1
    if(TimeManager.TimeManager.currentTime >= 24):
        TimeManager.TimeManager.currentTime = 0