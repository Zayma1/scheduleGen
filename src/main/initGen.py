import json
from time import sleep

#---Required classes
import classes
import subjectGroup
import teacher

#---sys
import sys

#---variables

globals
isAllClassesDone = False
attemps = 10000


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
   
for index, classes in enumerate(allClasses):
   classes.setSubjectDataFromSubjectGroup()

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
   
def printTeachers(AClass):
   for index, day in enumerate(AClass):
      print(f"DIA: {index}")
      for index2, teachers in enumerate(day):
         print(f"TEACHER: {teachers.teacherName}")
      


#---End Functions

#---Start Gen

while isAllClassesDone != True or attemps == 0:
      for index, classes in enumerate(allClasses):
         #using checkingAmountOfClasses to verify if the amount of classes are correct
         checkAmountofClasses = classes.checkAmountOfClasses()

         #if the amount of classes are != True, so it ill return a vector.
         #the vector contains the amount of classes is needed to add or remove, and 
         #the teacher.
         if checkAmountofClasses != True:

            moreOrLower = checkAmountofClasses[2] #more(need to remove classes) #lower(need to add more classes)
            amount = checkAmountofClasses[1]
            teacherTemp = checkAmountofClasses[0]

            #each For above remove or add a classes, if its False then add, then True
            # remove
            
            if len(classes.allWeekSubjects) <= settings.get("maxClassesPerWeek"):
               if moreOrLower == False:
                  print(f"Adding: {teacherTemp.teacherName}")
                  classes.allWeekSubjects.append(teacherTemp)

               elif moreOrLower == True:
                  print(f"Removing: {teacherTemp.teacherName}") 
                  classes.allWeekSubjects.remove(teacherTemp)
            else:
               print("ERROR OCCURED ON GENERATING CLASSES (CLASSES LIMIT EXCEED)")
               break
         
    