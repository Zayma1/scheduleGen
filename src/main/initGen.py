import json
from time import sleep

#---Required classes
import classes
import subjectGroup
import teacher
import timedate

#---sys
import sys

#---variables

globals
isAllClassesDone = False
attemps = 10000
hoursAlreadyBooked = []


#---Set data
data = json.loads(sys.argv[1])

allClasses = []
allTeachers = []
allSujectsGroups = []
settings = {}


#all os this For's are used to set all the data which generator will use to gen schedules
#creating instances of classes (provided by JSON), and put them into a list.
for index,(key,value) in enumerate(data['settings'].items()):
   settings.update({key:value})


for index, (key,value) in enumerate(data['classes'].items()):
   allClasses.append(
      classes.Classes(**value)
   )

#for to set subjectGroup data
for index, (key,value) in enumerate(data['subjectGroup'].items()):
   allSujectsGroups.append(
      subjectGroup.SubjectsGroup(key,value)
   )

   #for to set subjectGroup variable in class Classes
   for index, classesObject in enumerate(allClasses):
      if classesObject.subjectGroup == key:
         classesObject.subjectGroup = subjectGroup.SubjectsGroup(key,value)
   

for index,groupName in enumerate(allSujectsGroups):
   count = 0
   for index, group in enumerate(groupName.subjects):
      count += group[2]
   
   if(count > settings.get("maxClassesPerWeek")):
      print("Limit of classes exceeded, but the generation will continue.")

    
#---End Set data



#---Functions

#function to get a teacher from a classes Object
def getTeacher(name):
      for index, value in enumerate(allTeachers):
         if value.teacherName == name:
            return value

 #function to verify if all classes are done

#function to verify how many schedules are done
def checkClassesSchedule():
   i = 0 
   global isAllClassesDone

   #verify how many classes are done
   for index, value in enumerate(allClasses):
      if(value.isScheduleDone == True):
         i += 1

   #if all classes are done return true, else return false and how many are true
   if i == len(allClasses):
      isAllClassesDone = True
      return True
   else:
      isAllClassesDone = False
      return [False,i] 

#function to get amount of classes in a day ex: monday, five amount of classes with a teacher
def countAmountOfClasses(day,teachername):
   count = 0
   for index,value in enumerate(day):
      if value.teacherName == teachername:
         count += 1

   return count

def checkHour(day,hour,teacher):
   for index, dateTime in enumerate(hoursAlreadyBooked):
      if dateTime.day == day and dateTime.hour == hour and dateTime.teacherName == teacher:
         return True
   
   return False

#function to help on development
def printTeachers(AClass):
   for index, day in enumerate(AClass):
      print(f"========= DIA: {index} ===========")
      for index2, teachers in enumerate(day):
         print(f"TEACHER: {teachers.teacherName}")

def printHours(hour):
   for index, value in enumerate(hour):
      print(f"DIA: {value.day} AULA: {value.hour} TEACHER: {value.teacherName}")

def printWeekSubjects(subjects):
   for index, value in enumerate(subjects):
      print(f"MÁTERIA: {value.teacherName}")

#---End Functions

#---Start Gen

while isAllClassesDone != True or attemps == 0:
      #for loop for set subjects into classes class
      for index, classes in enumerate(allClasses):
         classes.setSubjects()
      
      #for to organize the subjects
      for index, classes in enumerate(allClasses):
         for index3, day in enumerate(classes.schedule):
            for index2, subject in enumerate (classes.allWeekSubjects):
               if len(classes.schedule[index3 - 1]) >= 10 or index3 == 0:
                  if len(day) < 10:
                     if checkHour(index3,len(day) + 1,subject.teacherName) == False:
                        hour = len(day) + 1
                        teacherCount = countAmountOfClasses(classes.allWeekSubjects,subject.teacherName)
                        if teacherCount > 1:
                           amountOfConsecutiveClasses = 0
                           for index4, tempSubject in enumerate(classes.allWeekSubjects):
                              if tempSubject.teacherName == subject.teacherName and amountOfConsecutiveClasses <= settings.get("maxConsecutiveClasses"):
                                 if len(day) < 10:
                                    timeDate = timedate.timeDate(index3,hour,subject.teacherName)
                                    day.append(subject)
                                    hoursAlreadyBooked.append(timeDate)
                                    classes.allWeekSubjects.remove(tempSubject)
                                    amountOfConsecutiveClasses += 1
                        else:
                           timeDate = timedate.timeDate(index3,hour,subject.teacherName)
                           day.append(subject)
                           hoursAlreadyBooked.append(timeDate)
                           classes.allWeekSubjects.remove(subject)
                           amountOfConsecutiveClasses += 1

      print(f"TURMA: {allClasses[0].className} ")
      printTeachers(allClasses[0].schedule)
      print("==================================")
      print(f"TURMA: {allClasses[1].className} ")
      printTeachers(allClasses[1].schedule)
      print("===================== HORARIOS =================")
      printHours(hoursAlreadyBooked)
      sleep(100)



                     
                     
                  
                     
                  

      
        
    