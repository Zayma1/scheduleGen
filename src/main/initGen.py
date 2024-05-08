import json

#---Required classes
import classes
import subjectGroup
import teacher

#---sys
import sys

#---variables

globals
isAllClassesDone = False
attemps = 1000


#---Set data
data = json.loads(sys.argv[1])

allClasses = []
allTeachers = []
allSujectsGroups = []

#all os this For's are used to set all the data which generator will use to gen schedules
#creating instances of classes (provided by JSON), and put them into a list.
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

#for to set teachers data
for index, (key,value) in enumerate(data['teachers'].items()):
   allTeachers.append(
      teacher.Teacher(**value)
   )


print(allClasses[0].subjectGroup.subjects)
#---End Set data



#---Functions

 #function to verify if all classes are done
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

#---End Functions



#---Start Gen

#while isAllClassesDone != True or attemps == 0:
   #for index, value in enumerate(allClasses):
      
