import json
from faker import Faker
from random import randint, choice, shuffle
import datetime

faker = Faker()

def generate_json():
    result = {}
    result["departments"] = [generate_department(i) for i in range(10)]
    result["professors"] = [generate_professor(result["departments"]) for _ in range(20)]
    result["classes"] = [generate_class(result["professors"]) for _ in range(10)]
    result["students"] = [generate_student(result["classes"]) for _ in range(100)]
    return result

department_names = [
    "Computer Science",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Civil Engineering",
    "Physics",
    "Mathematics",
    "Marketing",
    "Business Administration",
    "Finance",
    "Art"
]
shuffle(department_names)

def generate_department(i):
    return {
        "department_id": faker.unique.random_int(min=1000, max=9999),
        "name": department_names[i]
    }

def generate_professor(departments):
    department = choice(departments)
    return {
        "employee_id": faker.unique.random_int(min=1000, max=9999),
        "department_id": department['department_id'],
        "first_name": faker.first_name(),
        "last_name": faker.last_name()
    }

def generate_class(professors):
    level_list = [100, 101, 102, 200, 201, 202]
    return {
        "class_id": faker.unique.random_int(min=1000, max=9999),
        "title": faker.catch_phrase(),
        "level": choice(level_list),
        "professor_id": choice(professors)["employee_id"]
    }

def generate_student(classes):
    enrollments = [{
        "class_id": choice(classes)["class_id"],
        "enrollment_date": faker.date_between_dates(
            date_start=datetime.date(2020, 1, 1),
            date_end=datetime.date(2023, 12, 31)
        ).isoformat()
    } for _ in range(randint(1, 10))]

    return {
        "student_id": faker.unique.random_int(min=1000, max=9999),
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "enrollments": enrollments
    }


fake_data = generate_json()

with open('my_data.json', 'w') as json_file:
    json.dump(fake_data, json_file, ensure_ascii=False, indent=2)