# src/knowledge_base.py

import os
import json

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
COURSES_DIR = os.path.join(DATA_DIR, 'Courses')
ELECTIVES_DIR = os.path.join(COURSES_DIR, 'Electives')
UNIREQ_DIR = os.path.join(COURSES_DIR, 'UniReq')

def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

# Load policies and study plan
def load_policies():
    return load_json(os.path.join(DATA_DIR, "Policies.json"))

def load_study_plan():
    return load_json(os.path.join(DATA_DIR, "StudyPlan.json"))

# Load course groups
def load_core_courses():
    return load_json(os.path.join(COURSES_DIR, "Core_courses.json"))

def load_ft_courses():
    return load_json(os.path.join(COURSES_DIR, "FT_courses.json"))

def load_graduation_courses():
    return load_json(os.path.join(COURSES_DIR, "Graduation_courses.json"))

def load_elective_courses():
    return load_json(os.path.join(ELECTIVES_DIR, "Elective_courses.json"))

def load_university_compulsory():
    return load_json(os.path.join(UNIREQ_DIR, "Compulsory_unireq.json"))

def load_university_elective():
    return load_json(os.path.join(UNIREQ_DIR, "Elective_unireq.json"))

def load_zero_credit_unireq():
    return load_json(os.path.join(UNIREQ_DIR, "Zero_unireq.json"))

# Merge all courses into a single dictionary
def get_all_courses():
    all_courses = {}

    # Core
    for course in load_core_courses():
        all_courses[course["code"]] = course

    # Field Training
    for course in load_ft_courses():
        all_courses[course["code"]] = course

    # Graduation Project
    for course in load_graduation_courses():
        all_courses[course["code"]] = course

    # Electives
    for course in load_elective_courses():
        all_courses[course["code"]] = course

    # University Compulsory
    for course in load_university_compulsory():
        all_courses[course["code"]] = course

    # University Electives
    for course in load_university_elective():
        all_courses[course["code"]] = course

    # Zero Credit Courses
    for course in load_zero_credit_unireq():
        all_courses[course["code"]] = course

    return all_courses
