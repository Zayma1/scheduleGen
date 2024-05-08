
import teacher


class Classes():
    def __init__(self,className,subjectGroup,isScheduleDone):
        self.className = className
        self.subjectGroup = subjectGroup
        self.isScheduleDone = isScheduleDone
        self.schedule = [[],[],[],[],[]] #each vector means one day, monday, tue etc
    

    #function to check if all the days are agree, that means if have 8 periods of class
    def checkScheduleBase(self):
        amountOfClasses = 0

        for index, value in enumerate(self.schedule):
            for index, value in enumerate(value):
                if type(value) == teacher.Teacher:
                    amountOfClasses += 1
        
        return amountOfClasses
    
    #function to check if the number of classes are agree
    #def checkNumberOfClasses(self):
        
    

classTest = Classes("351", "a", False)

#print(classTest.checkScheduleBase())