import json
import os
from datetime import datetime

class StudentAuth:
    def __init__(self):
        self.students_file = "data/students.json"
        self._ensure_students_file()

    def _ensure_students_file(self):
        if not os.path.exists(self.students_file):
            with open(self.students_file, 'w') as f:
                json.dump([], f)

    def register_student(self, student_id, name, email, level):
        students = self._load_students()
        
        # Check if student already exists
        if any(s['student_id'] == student_id for s in students):
            return False, "Student ID already registered"
        
        new_student = {
            'student_id': student_id,
            'name': name,
            'email': email,
            'level': level,
            'registration_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        students.append(new_student)
        self._save_students(students)
        return True, "Registration successful"

    def get_student(self, student_id):
        students = self._load_students()
        for student in students:
            if student['student_id'] == student_id:
                return student
        return None

    def _load_students(self):
        with open(self.students_file, 'r') as f:
            return json.load(f)

    def _save_students(self, students):
        with open(self.students_file, 'w') as f:
            json.dump(students, f, indent=2) 