import csv

class StudentList:

    def __init__(self, students_file):
        reader = csv.reader(open(students_file, newline=''))
        reader = iter(reader)
        self.header = next(reader)
        self.students = []
        for row in reader:
            self.students.append(Student(row))

    def __str__(self):
        res = 'Header: ' + str(self.header)
        for student in self.students:
            res += '\n' + str(student)
        return res

class Student:

    def __init__(self, row):
        self.row = row
        self.errors = []

    def name(self):
        first = self.row[7].strip().casefold()
        last = self.row[8].strip().casefold()
        return first + ' ' + last

    def wants_same_tutor(self):
        if self.row[10] == 'Yes':
            return True
        else:
            return False

    def grade(self):
        return self.row[14]

    def subjects(self):
        return set(subject.strip().casefold() for subject in self.row[15].split(';'))

    def needs_spanish(self):
        return self.row[17] == 'Yes'

    def __str__(self):
        return 'name={0}, wants_same_tutor={1}, grade={2}, subjects={3}, needs_spanish={4}'.format(self.name(), 
                self.wants_same_tutor(), self.grade(), self.subjects(), self.needs_spanish())
