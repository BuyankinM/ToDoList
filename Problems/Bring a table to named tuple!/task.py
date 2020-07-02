from collections import namedtuple

student = namedtuple('Student', 'name, age, department')
print(student("Alina", "22", "linguistics"))
print(student("Alex", "25", "programming"))
print(student("Kate", "19", "art"))