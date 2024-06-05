
import teacher
from time import sleep


class Classes():
    def __init__(self,className,subjectGroup,isScheduleDone):
        self.className = className
        self.subjectGroup = subjectGroup
        self.isScheduleDone = isScheduleDone
        self.allWeekSubjects = []
        self.schedule = [[],[],[],[],[]] #each vector means one day, monday, tue etc
    
    #function to check if all the days are agree, that means if have 8 periods of class
    def checkScheduleBase(self):
        amount = 0

        for index, day in enumerate(self.schedule):
            for index, teachers in enumerate(day):
                if type(teachers) == teacher.Teacher:
                    amount += 1
        
        return amount
    

    #function to verify if the amount of classes are correct (classes per week)
    def setSubjects(self):
        for index, value in enumerate(self.subjectGroup.subjects):
            for c in range(value[2]):
                teachers = teacher.Teacher(value[1],value[0])
                self.allWeekSubjects.append(teachers)
            

   
            
    
    




