# src/knowledge_base_editor.py

import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'Courses')

# File paths
PATHS = {
    "core": os.path.join(DATA_DIR, "Core_courses.json"),
    "ft": os.path.join(DATA_DIR, "FT_courses.json"),
    "graduation": os.path.join(DATA_DIR, "Graduation_courses.json"),
    "elective": os.path.join(DATA_DIR, "Electives", "Elective_courses.json"),
    "uni_compulsory": os.path.join(DATA_DIR, "UniReq", "Compulsory_unireq.json"),
    "uni_elective": os.path.join(DATA_DIR, "UniReq", "Elective_unireq.json"),
    "zero_unireq": os.path.join(DATA_DIR, "UniReq", "Zero_unireq.json")
}

def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    print("✅ File saved.")

def list_courses(course_type):
    data = load_json(PATHS[course_type])
    print("\n--- Course List ---")
    if isinstance(data, list):
        for course in data:
            print(f"{course['code']} - {course['name']}")
    elif isinstance(data, dict):  # Elective groups or university electives
        for group, courses in data.items():
            print(f"\nGroup: {group}")
            for course in courses:
                print(f"  {course['code']} - {course['name']}")
    print("--------------------\n")

def add_course(course_type):
    print("\n📝 Enter New Course Info")
    code = input("Course Code: ").strip()
    name = input("Course Name: ").strip()
    credits = int(input("Credit Hours: ").strip())
    semester = input("Semester Offered (comma-separated, e.g., Fall,Spring,Both): ").strip().split(",")
    description = input("Description: ").strip()
    prerequisites = input("Prerequisites (comma-separated codes or leave empty): ").strip().split(",") if input("Does it have prerequisites? (y/n): ").lower() == 'y' else []
    corequisites = input("Co-requisites (comma-separated codes or leave empty): ").strip().split(",") if input("Any co-requisites? (y/n): ").lower() == 'y' else []

    course = {
        "code": code,
        "name": name,
        "credits": credits,
        "semester_offered": [s.strip() for s in semester],
        "description": description,
        "prerequisites": [p.strip() for p in prerequisites if p],
        "corequisites": [c.strip() for c in corequisites if c]
    }

    # Electives and university electives need group/category info
    if course_type == "elective":
        data = load_json(PATHS["elective"])
        group = input("Elective Group (E1 to E6): ").strip().upper()
        data.setdefault(group, []).append(course)
        save_json(PATHS["elective"], data)

    elif course_type == "uni_elective":
        data = load_json(PATHS["uni_elective"])
        category = input("Elective Category (e.g., Languages, Art_Literature): ").strip()
        data["electives"].setdefault(category, []).append(course)
        save_json(PATHS["uni_elective"], data)

    else:  # core, ft, graduation, uni_compulsory, zero_unireq
        data = load_json(PATHS[course_type])
        data.append(course)
        save_json(PATHS[course_type], data)

    print(f"✅ Course {code} added to {course_type}.")

def main():
    print("🎓 Knowledge Base Editor")
    while True:
        print("\nAvailable Types: core, ft, graduation, elective, uni_compulsory, uni_elective, zero_unireq")
        choice = input("Enter course type or 'exit' to quit: ").strip().lower()

        if choice == "exit":
            print("Exiting...")
            break
        elif choice not in PATHS:
            print("❌ Invalid course type.")
            continue

        action = input("Action? (list / add): ").strip().lower()
        if action == "list":
            list_courses(choice)
        elif action == "add":
            add_course(choice)
        else:
            print("❌ Invalid action.")

if __name__ == "__main__":
    main()
