import Enumerations
import Entities
import StateMachine
import EntityManager
import TimeManager
import States
import Messaging

#two students and two miners
#**Their routines are the same except they have different occupations, and
#**one student starts with more food in their inventory than the other student. Same with the miners.
student1 = Entities.Student(0, "Student 1", Enumerations.location_type.school, 0, 0, 5, 0, 0, 0, 0)
student2 = Entities.Student(1, "Student 2", Enumerations.location_type.school, 0, 0, 0, 0, 0, 0, 0)
memberOfSociety1 = Entities.Worker(2, "Miner 1", Enumerations.location_type.mines, 0, 0, 5, 0, 0, 0, 0)
memberOfSociety2 = Entities.Worker(3, "Miner 2", Enumerations.location_type.mines, 0, 0, 0, 0, 0, 0, 0)

EntityManager.EntityManager().registerEntity(student1)
EntityManager.EntityManager().registerEntity(student2)
EntityManager.EntityManager().registerEntity(memberOfSociety1)
EntityManager.EntityManager().registerEntity(memberOfSociety2)
dispatcher = Messaging.MessageDispatcher() #for dispatching delayed messages each hour

i = 0
loops = input("Enter how many hours will pass in game: ")
print(loops, "hours will pass")
while(i < int(loops)):
    #1 hour per loop
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

input("Press enter to exit program ")