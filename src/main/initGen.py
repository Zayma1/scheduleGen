import json
from time import sleep

#---Required classes
import classes
import subjectGroup
import teacher
import timedate
from random import sample
import pandas as pd
from openpyxl import load_workbook
import jinja2
from math import ceil
from os import system

#---sys
import sys

#---variables

globals
isAllClassesDone = False
attemps = 10000
hoursAlreadyBooked = []
checkData = [True,"MessageError"]
noClasses = teacher.Teacher("---","---")
percentage = ""

defaultTime = ["7h45","8h30","9h15","10h15","11h00"
               ,"13h15","14h00","14h45","15h45","16h30"]

halfTime = ["7h45","8h30","9h15","10h15","11h00"]

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


for index, value in enumerate(data['classes']):
   allClasses.append(
      classes.Classes(**value)
   )

#for to set subjectGroup data
for index, value in enumerate(data['subjectGroup']):
   temp = []
   lastName = ""
   for index2, (key2,value2) in enumerate(value.items()):
      if(key2 == "subjects"):
         for index3, value3 in enumerate(value2):
            temp.append(list(value3.values()))

         allSujectsGroups.append(
                        subjectGroup.SubjectsGroup(lastName,temp)
                        )    
      lastName = value2
      
   #for to set subjectGroup variable in class Classes
   for index, classesObject in enumerate(allClasses):
      for index2, subject in enumerate(allSujectsGroups):
         if subject.groupName == classesObject.subjectGroup:
            classesObject.subjectGroup = subject
       
#---End Set data

#---Functions

#function to format subjects names on excel file
def formatSubjectName(subject, teacherName):
   name = ""
   for c in range(len(subject)):
      if c <= 4:
         name += subject[c]
   
   name += f"({teacherName})"
   return name


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

#function to check if there is already a teacher with classes at that time
def checkHour(day,hour,teachers):
   for index, dateTime in enumerate(hoursAlreadyBooked):
      if dateTime.day == day and dateTime.hour == hour and dateTime.teacher.teacherName == teachers.teacherName:
         return True
   
   return False

#---End Functions


#Set subjects data
for index, classes in enumerate(allClasses):
      classes.setSubjects()

#Shuffle the subjects array for all classes
for index, classes in enumerate(allClasses):
      classes.allWeekSubjects = sample(classes.allWeekSubjects,len(classes.allWeekSubjects))


#checking if a teacher has more classes per week than allowed and if a group of subjects has more classes than allowed too
#checking if there a duplicated teacher in a group
for index, groups in enumerate(allSujectsGroups):
      countGroupClasses = 0
      for index2, subjects in enumerate(groups.subjects):
         count = 0
         teacher = subjects
         countClasses = 0
         
         countGroupClasses += subjects[2]
         for index3, classes in enumerate(allClasses):
            for index4, teachers in enumerate(classes.allWeekSubjects):
               if teachers.teacherName == teacher[1]:
                  countClasses += 1
      
         for index5, subjects2 in enumerate(groups.subjects):
            if subjects2[0].capitalize() == teacher[0].capitalize() and subjects2[1].capitalize() == teacher[1].capitalize():
                  count += 1 
         
         if countClasses > settings.get("maxClassesPerWeek"):
            checkData[0] = False
            checkData[1] = f"ERROR: LIMIT OF CLASSES PER WEEK WAS EXCEED. teacher: {teacher[1]}"
         
         if count > 1:
            checkData[0] = False
            checkData[1] = f"ERROR: Duplicated teachers at group: {groups.groupName} TEACHER: {teacher}"

      if countGroupClasses > settings.get("maxClassesPerWeek"):
          checkData[0] = False
          checkData[1] = f"ERROR: THERES A GROUP WITH MORE CLASSES PER WEEK THAN ALLOWED"

#checking if amount of classes per week is greater than allowed
for index,group in enumerate(allSujectsGroups):
   count = 0
   for index, subjects in enumerate(group.subjects):
      count += subjects[2]
   
   if(count > settings.get("maxClassesPerWeek")):
      checkData[0] = False
      checkData[1] = f"Limit of classes exceeded({count}) on group({group.groupName}) Max limit({settings.get('maxClassesPerWeek')}) stoping generation."

#---START GEN
if checkData[0] == True:
   while attemps > 0:   
         count = 0
         attemps -= 1

         #for to organize the subjects
         for index, classes in enumerate(allClasses):
            for index3, day in enumerate(classes.schedule):
               for index2, subject in enumerate (classes.allWeekSubjects): 
                     if len(classes.schedule[index3 - 1]) == settings.get("maxClassPerDay") or index3 == 0:
                        if len(day) < settings.get("maxClassPerDay"):
                           if checkHour(index3,len(day)+1,subject) == False:
                              teachersCount = countAmountOfClasses(classes.allWeekSubjects,subject.teacherName)
                              addedTeachers = 0
                              if teachersCount > 1:
                                    for index4, tempSubject in enumerate(classes.allWeekSubjects):
                                       if tempSubject.teacherName == subject.teacherName:
                                          if checkHour(index3,len(day)+1,subject) == False:
                                             if addedTeachers < settings.get("maxConsecutiveClasses"):
                                                if len(day) < settings.get("maxClassPerDay"):
                                                   hour = len(day) + 1
                                                   addedTeachers += 1
                                                   day.append(tempSubject)
                                                   datetime = timedate.timeDate(index3,hour,subject)
                                                   hoursAlreadyBooked.append(datetime)
                              else:
                                    if len(day) < settings.get("maxClassPerDay"):
                                       hour = len(day) + 1
                                       day.append(subject)
                                       datetime = timedate.timeDate(index3,hour,subject)
                                       hoursAlreadyBooked.append(datetime)
                                       addedTeachers += 1

                              #removing teachers added in day from allWeekSubjects
                              tempCount = 0
                              for index, value in enumerate(classes.allWeekSubjects):
                                 if tempCount < addedTeachers:
                                    if value.teacherName == subject.teacherName:
                                       classes.allWeekSubjects.remove(value)
                                       tempCount += 1

                             

                             
         #calc percentag of classes schedule done
         amountOfClassesDone = 0
         for index, classes in enumerate(allClasses):
            if len(classes.allWeekSubjects) == 0:
               classes.isScheduleDone = True
               amountOfClassesDone += 1

         if type(checkClassesSchedule()) == list:
            percentage = f"{ceil((amountOfClassesDone*100)/len(allClasses))}%"
         else:
            percentage = f"{ceil((amountOfClassesDone*100)/len(allClasses))}%"

         checkClassesSchedule()
   

                           
   #filling with vacant classes
   for index, classes in enumerate(allClasses):
      for index2, day in enumerate(classes.schedule):
         if len(day) < settings.get("maxClassPerDay"):
            for c in range(settings.get("maxClassPerDay")-len(day)):
               day.append(noClasses)

         
   #GENERATE EXCEL FILE
   dataframe = {
      "HORARIOS": []
   }

   if settings.get("maxClassesPerWeek") == 50:
      #gen default time
      for c in range(5):
         if c != 0:
            dataframe.get("HORARIOS").append("")
         for index, time in enumerate(defaultTime):
            dataframe.get("HORARIOS").append(time)
            if index == 4:
               dataframe.get("HORARIOS").append("INTERVALO")

      
      for index, classes in enumerate(allClasses):
         dataframe.update({classes.className:[]})
         
         for index2, day in enumerate(classes.schedule):
            if index2 != 0:
               dataframe.get(classes.className).append("")
            for index3, subjects in enumerate(day):
               dataframe.get(classes.className).append(formatSubjectName(subjects.subjectName,subjects.teacherName))
               if index3 == 4:
                  dataframe.get(classes.className).append("")

      schedule = pd.DataFrame(dataframe)
      schedule.to_excel("src/scheduleResponse/Schedule.xlsx",index=False)

      system('cls')
      print("Generation complete. Check the 'scheduleResponse' folder.")

   elif settings.get("maxClassesPerWeek") == 25:
      #gen half time
      for c in range(5):
         if c != 0:
            dataframe.get("HORARIOS").append("")
         for index, time in enumerate(halfTime):
            dataframe.get("HORARIOS").append(time)

      for index, classes in enumerate(allClasses):
         dataframe.update({classes.className:[]})
         
         for index2, day in enumerate(classes.schedule):
            if index2 != 0:
               dataframe.get(classes.className).append("")
            for index3, subjects in enumerate(day):
               dataframe.get(classes.className).append(formatSubjectName(subjects.subjectName,subjects.teacherName))

      schedule = pd.DataFrame(dataframe)
      schedule.to_excel("src/scheduleResponse/Schedule.xlsx",index=False)

      print("Generation complete. Check the 'scheduleResponse' folder.")
else:
   print(f"GENERATION CANCELLED: {checkData[1]}")
#---END GEN       


