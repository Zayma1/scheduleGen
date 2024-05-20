class Teacher():
    def __init__(self, teacherName, subjectName,hoursAlreadyBooked):
        self.teacherName = teacherName
        self.subjectName = subjectName
        self.hoursAlreadyBooked = hoursAlreadyBooked


    def checkHour(self, hour):
        hoursAlreadyBooked = self.hoursAlreadyBooked

        if hour in hoursAlreadyBooked:
            return True
        else:
            return False