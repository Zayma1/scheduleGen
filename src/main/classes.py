
import teacher
from time import sleep


class Classes():
    def __init__(self,className,subjectGroup,isScheduleDone):
        self.className = className
        self.subjectGroup = subjectGroup
        self.isScheduleDone = isScheduleDone
        self.schedule = [[],[],[],[],[]] #each vector means one day, monday, tue etc
    

    #function to check if all the days are agree, that means if have 8 periods of class
    def checkScheduleBase(self):
        amount = 0

        for index, value0 in enumerate(self.schedule):
            for index, value1 in enumerate(value0):
                if type(value1) == teacher.Teacher:
                    amount += 1
        
        return amount
    

    #function to verify if the amount of classes are correct (classes per week)
    def checkAmountOfClasses(self):

        subjectgroup = self.subjectGroup
        classSchedule = self.schedule

        #this dict will save all classes and amount of classes in a week
        #Example: 'math': 2
        classes = {}


        #(for) to count how many classes in a week and append in classes
        for index0, subjects in enumerate(subjectgroup.subjects):
             count = 0
             name = ""
             for index1, scheduleDays in enumerate(classSchedule):
                for index2, teachers in enumerate(scheduleDays):
                    if type(teachers) == teacher.Teacher:
                        if teachers.teacherName == subjects[1]:
                            count += 1
                            name = teachers.teacherName
                
                            classes.update({name:count})

        #(for) to verify if number of classes are correct
        #that verification is based on third parameter of subjects from subjectGroup class
        #(subjectGroup.subjects[2] <- third parameter)
        
        
        for index, (subject, amount) in enumerate(classes.items()):
            for index1, subjects in enumerate(subjectgroup.subjects):
                if subjects[1] == subject:
                    if amount > subjects[2]:
                        #Parameters below: 
                        #first parameter: False = amount is not correct
                        #second parameter: difference beetwen
                        #third parameter: True or False = difference is higher(true) or lower(false)
                        teacherToReturn = teacher.Teacher(subjects[1],subjects[0],subjects[2])
                        return [teacherToReturn, amount - subjects[2], True]
                    if amount < subjects[2]:
                        teacherToReturn = teacher.Teacher(subjects[1],subjects[1],subjects[2])
                        return [teacherToReturn, subjects[2] - amount, False]
        return True     

   
            
    
    




