import csv


class TutorList:

    def __init__(self, tutor_file):
        reader = csv.reader(open(tutor_file, newline=''))
        reader = iter(reader)
        self.header = next(reader)
        self.tutors = []
        for row in reader:
            self.tutors.append(Tutor(row))

    def __str__(self):
        res = 'Header: ' + str(self.header)
        for tutor in self.tutors:
            res += '\n' + str(tutor)
        return res

class Tutor:

    def __init__(self, row):
        self.row = row

    def name(self):
        first = self.row[2].strip().casefold()
        last = self.row[3].strip().casefold()
        return first + ' ' + last

    def full_time_tutor(self):
        return self.row[5] == 'Full-time tutor (every Tuesday night)'

    def wants_same_student(self):
        return self.row[6] == 'Yes'

    def grades(self):
        if not self.row[7]:
            return set()
        return set(grade.strip() for grade in self.row[7].split(';'))

    def subjects(self):
        if not self.row[8]:
            return set()
        return set(subject.strip().casefold() for subject in self.row[8].split(';'))

    def speaks_spanish(self):
        return self.row[9] == 'Si'

    def __str__(self):
        return 'name={0}, full_time_tutor={1}, wants_same_student={2}, grades={3}, subjects={4}, speaks_spanish={5}'.format(
            self.name(), self.full_time_tutor(), self.wants_same_student(), self.grades(), self.subjects(), self.speaks_spanish())