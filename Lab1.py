import Enumerations
import Entities
import StateMachine
import EntityManager


student1 = Entities.Student(0, "Student 1", Enumerations.location_type.school, 0, 0)
student2 = Entities.Student(1, "Student 2", Enumerations.location_type.school, 0, 0)
memberOfSociety1 = Entities.Worker(2)
memberOfSociety2 = Entities.Worker(3)

EntityManager.EntityManager().registerEntity(student1)
EntityManager.EntityManager().registerEntity(student2)
EntityManager.EntityManager().registerEntity(memberOfSociety1)
EntityManager.EntityManager().registerEntity(memberOfSociety2)

i = 0
while(i < 15):
    i += 1
    
    student1.stateMachine.update()
    print("")