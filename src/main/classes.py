
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

        for index, value0 in enumerate(self.schedule):
            for index, value1 in enumerate(value0):
                if type(value1) == teacher.Teacher:
                    amountOfClasses += 1
        
        return amountOfClasses
    

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
                        if teachers.subjectName == subjects[0]:
                            count += 1
                            name = teachers.subjectName

             classes.update({name:count})

        #(for) to verify if number of classes are correct
        #that verification is based on third parameter of subjects from subjectGroup class
        #(subjectGroup.subjects[2] <- third parameter)
        for index, (subject, amount) in enumerate(classes.items()):
            for index1, subjects in enumerate(subjectgroup):
                if subjects[0] == subject:
                    if subject > subject[2]:
                        #Parameters below: 
                        #first parameter: False = amount is not correct
                        #second parameter: difference beetwen
                        #third parameter: True or False = difference is higher(true) or lower(false)
                        return [False, subject - subjects[2], True]
                    if amount < subjects[2]:
                        return [False, subjects[2] - amount, False]

        return True        
            
    
    




