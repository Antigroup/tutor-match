import csv

from students import Student, StudentList
from tutors import Tutor, TutorList

def editDistance(str1, str2, m=None, n=None):
    if m is None:
        m = len(str1)
    if n is None:
        n = len(str2)
    # Create a table to store results of subproblems 
    dp = [[0 for x in range(n+1)] for x in range(m+1)] 

    # Fill d[][] in bottom up manner 
    for i in range(m+1): 
        for j in range(n+1): 

            # If first string is empty, only option is to 
            # insert all characters of second string 
            if i == 0: 
                dp[i][j] = j    # Min. operations = j 

            # If second string is empty, only option is to 
            # remove all characters of second string 
            elif j == 0: 
                dp[i][j] = i    # Min. operations = i 

            # If last characters are same, ignore last char 
            # and recur for remaining string 
            elif str1[i-1] == str2[j-1]: 
                dp[i][j] = dp[i-1][j-1] 

            # If last character are different, consider all 
            # possibilities and find minimum 
            else: 
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert 
                                   dp[i-1][j],        # Remove 
                                   dp[i-1][j-1])    # Replace 

    return dp[m][n]

def first(iterable, predicate=lambda x: True):
    for i in iterable:
        if predicate(i):
            return i
    return None

def check_match_hard(student, tutor):
    """Checks that tutor can teach student, given grade level, subjects, and spanish fluency."""
    if not tutor.full_time_tutor():
        return False
    if tutor.grades() and student.grade() not in tutor.grades():
        return False
    if tutor.subjects() and not student.subjects().issubset(tutor.subjects()):

        return False
    if student.needs_spanish() and not tutor.speaks_spanish():
        return False
    
    return True

def load_previous_matches():
    result = {}
    reader = csv.reader(open('previous-matches.csv', newline=''))
    reader = iter(reader)
    next(reader) # drop header

    for row in reader:
        row = tuple(i.strip().casefold() for i in row)
        tutor_last, tutor_first, cotutor_last, cotutor_first, student_first, student_last = row
        if tutor_first != '':
            result[student_first + ' ' + student_last] = tutor_first + ' ' + tutor_last
            continue
        if cotutor_first != '':
            result[student_first + ' ' + student_last] = cotutor_first + ' ' + cotutor_last
            continue
    return result


def main():
    def add_match(student, tutor):
        row = student.row + tutor.row
        if student.errors:
            row += ';'.join(student.errors),
        matches.append(row)
        unmatched_students.students.remove(student)
        unmatched_tutors.tutors.remove(tutor)

    previous_matches = load_previous_matches()
    unmatched_students = StudentList('data/students.csv')
    unmatched_tutors = TutorList('data/tutors.csv')

    matches = []
    # Allow previous matches to stay together.
    for student in unmatched_students.students:
        if not student.wants_same_tutor():
            continue
        if student.name() not in previous_matches.keys():
            student.errors.append('Could not find student in previous-matches.csv.')
            continue
        previous_tutor_name = previous_matches[student.name()]
        previous_tutor = first(unmatched_tutors.tutors,
                lambda tutor: tutor.name() == previous_tutor_name)
        if not previous_tutor:
            student.errors.append('Could not find previous tutor: %s' % previous_tutor_name)
            continue
        if not previous_tutor.wants_same_student():
            student.errors.append('Previous tutor (%s) does not want same student.' % previous_tutor_name)
            continue

        student.errors.append('Using previous tutor.')
        add_match(student, previous_tutor)

    for student in list(unmatched_students.students): # copy so we can delete entries while iterating
        possible_tutors = [t for t in unmatched_tutors.tutors if check_match_hard(student, t)]
        if not possible_tutors:
            student.errors.append('No suitable tutors remaining.')
            continue
        
        add_match(student, possible_tutors[0])

    writer = csv.writer(open('unmatched_students.csv', mode='w', newline=''))
    writer.writerow(unmatched_students.header + ['Matching Notes'])
    for student in unmatched_students.students:
        row = student.row
        if student.errors:
            row += ';'.join(student.errors),
        writer.writerow(row)

    writer = csv.writer(open('unmatched_tutors.csv', mode='w', newline=''))
    writer.writerow(unmatched_tutors.header)
    for tutor in unmatched_tutors.tutors:
        for student in unmatched_students.students:
            if check_match_hard(student, tutor):
                print('wtf?')
        writer.writerow(tutor.row)
    
    writer = csv.writer(open('matches.csv', mode='w', newline=''))
    writer.writerow(unmatched_students.header + unmatched_tutors.header + ['Matching Notes'])
    for match in matches:
        writer.writerow(match)

if __name__ == '__main__':
    main()