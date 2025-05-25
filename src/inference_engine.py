# src/inference_engine.py

from experta import *
import json
import os
from datetime import datetime

# Fact to represent student input
class StudentProfile(Fact):
    """Student profile with CGPA and course history"""
    cgpa: float
    passed: list
    failed: list
    semester: str

class Course(Fact):
    """Course information"""
    pass

class CourseAdvisor(KnowledgeEngine):
    @DefFacts()
    def _initial_facts(self):
        yield InitialFact()

    @Rule(
        StudentProfile(
            cgpa=MATCH.cgpa,
            passed=MATCH.passed,
            failed=MATCH.failed,
            semester=MATCH.semester
        )
    )
    def recommend_courses(self, cgpa, passed, failed, semester):
        # Load all course data
        courses = self._load_courses()
        policies = self._load_policies()
        study_plan = self._load_study_plan()

        # Get credit limit based on CGPA
        credit_limit = self._get_credit_limit(cgpa, policies)
        
        # Get available courses for the semester
        available_courses = self._get_available_courses(courses, semester)
        
        # Filter courses based on prerequisites and failed courses
        eligible_courses = self._filter_eligible_courses(
            available_courses,
            passed,
            failed,
            study_plan
        )
        
        # Sort courses by priority with enhanced logic
        sorted_courses = self._sort_courses_by_priority(
            eligible_courses,
            passed,
            failed,
            study_plan,
            semester
        )
        
        # Select courses within credit limit
        selected_courses = self._select_courses_within_limit(
            sorted_courses,
            credit_limit
        )
        
        # Generate detailed explanations
        explanations = self._generate_explanations(
            selected_courses,
            passed,
            failed,
            study_plan,
            semester
        )
        
        # Declare recommendations
        for course in selected_courses:
            self.declare(
                Course(
                    code=course["code"],
                    name=course["name"],
                    credits=course["credits"],
                    type=course.get("type", "core"),
                    semester=course["semester_offered"][0],
                    level=course.get("level", self._get_course_level(course["code"], study_plan))
                )
            )

    def _load_courses(self):
        """Load all course data from JSON files"""
        courses = {}
        
        # Load core courses
        with open("data/Courses/Core_courses.json", "r") as f:
            core_courses = json.load(f)
            for course in core_courses:
                course["type"] = "core"
                courses[course["code"]] = course
        
        # Load graduation courses
        with open("data/Courses/Graduation_courses.json", "r") as f:
            grad_courses = json.load(f)
            for course in grad_courses:
                course["type"] = "graduation"
                courses[course["code"]] = course
        
        # Load field training courses
        with open("data/Courses/FT_courses.json", "r") as f:
            ft_courses = json.load(f)
            for course in ft_courses:
                course["type"] = "field_training"
                courses[course["code"]] = course
        
        # Load elective courses
        with open("data/Courses/Electives/Elective_courses.json", "r") as f:
            elective_courses = json.load(f)
            for course in elective_courses:
                course["type"] = "elective"
                courses[course["code"]] = course
        
        # Load university requirements
        with open("data/Courses/UniReq/Compulsory_unireq.json", "r") as f:
            compulsory_courses = json.load(f)
            for course in compulsory_courses:
                course["type"] = "university_compulsory"
                courses[course["code"]] = course
        
        with open("data/Courses/UniReq/Elective_unireq.json", "r") as f:
            elective_uni_courses = json.load(f)
            for course in elective_uni_courses:
                course["type"] = "university_elective"
                courses[course["code"]] = course
        
        with open("data/Courses/UniReq/Zero_unireq.json", "r") as f:
            zero_courses = json.load(f)
            for course in zero_courses:
                course["type"] = "zero_credit"
                courses[course["code"]] = course
        
        return courses

    def _load_policies(self):
        """Load university policies"""
        with open("data/Policies.json", "r") as f:
            return json.load(f)

    def _load_study_plan(self):
        """Load study plan"""
        with open("data/StudyPlan.json", "r") as f:
            return json.load(f)

    def _get_credit_limit(self, cgpa, policies):
        """Get maximum allowed credits based on CGPA"""
        for limit in policies["credit_limits"]:
            if (limit["cgpa_min"] <= cgpa < limit["cgpa_max"] if limit["exclusive_max"]
                else limit["cgpa_min"] <= cgpa <= limit["cgpa_max"]):
                return limit["max_credits"]
        return 12  # Default limit

    def _get_available_courses(self, courses, semester):
        """Get courses available in the given semester"""
        return [
            course for course in courses.values()
            if semester in course["semester_offered"]
        ]

    def _filter_eligible_courses(self, courses, passed, failed, study_plan):
        """Filter courses based on prerequisites and failed courses"""
        eligible = []
        for course in courses:
            # Skip if course is already passed
            if course["code"] in passed:
                continue
                
            # Check prerequisites
            prereqs_met = True
            if "prerequisites" in course:
                for prereq in course["prerequisites"]:
                    if prereq not in passed:
                        prereqs_met = False
                        break
            
            if prereqs_met:
                eligible.append(course)
        
        return eligible

    def _get_course_level(self, course_code, study_plan):
        """Get the level of a course from the study plan"""
        for level in ["level_1", "level_2", "level_3", "level_4"]:
            for semester in ["fall", "spring"]:
                for course in study_plan[level][semester]["courses"]:
                    if course["code"] == course_code:
                        return level
        return "level_1"  # Default level

    def _get_student_level(self, passed, study_plan):
        """Determine student's current level based on passed courses"""
        total_credits = 0
        for level in ["level_1", "level_2", "level_3", "level_4"]:
            for semester in ["fall", "spring"]:
                for course in study_plan[level][semester]["courses"]:
                    if course["code"] in passed:
                        total_credits += course["credits"]
        
        if total_credits < 30:
            return "level_1"
        elif total_credits < 60:
            return "level_2"
        elif total_credits < 90:
            return "level_3"
        else:
            return "level_4"

    def _sort_courses_by_priority(self, courses, passed, failed, study_plan, semester):
        """Enhanced course prioritization based on multiple factors"""
        def get_course_priority(course):
            priority = 0
            current_level = self._get_student_level(passed, study_plan)
            course_level = self._get_course_level(course["code"], study_plan)
            
            # 1. Failed courses get highest priority (1000 points)
            if course["code"] in failed:
                priority += 1000
            
            # 2. Level-based priority (500 points)
            if course_level == current_level:
                priority += 500
            elif course_level == self._get_next_level(current_level):
                priority += 300
            elif course_level == self._get_previous_level(current_level):
                priority += 100
            
            # 3. Course type priority
            course_type = course.get("type", "core")
            if course_type == "core":
                priority += 200
            elif course_type == "university_compulsory":
                priority += 150
            elif course_type == "field_training":
                priority += 100
            elif course_type == "graduation":
                priority += 90
            elif course_type == "elective":
                priority += 80
            elif course_type == "university_elective":
                priority += 70
            elif course_type == "zero_credit":
                priority += 60
            
            # 4. Semester alignment (100 points)
            if semester in course["semester_offered"]:
                priority += 100
            
            # 5. Prerequisite chain priority (50 points per level)
            prereq_chain = self._get_prerequisite_chain(course["code"], study_plan)
            priority += len(prereq_chain) * 50
            
            # 6. Credit hours priority (10 points per credit)
            priority += course["credits"] * 10
            
            return priority
        
        return sorted(courses, key=get_course_priority, reverse=True)

    def _get_next_level(self, current_level):
        """Get the next level in sequence"""
        levels = ["level_1", "level_2", "level_3", "level_4"]
        current_index = levels.index(current_level)
        return levels[current_index + 1] if current_index < len(levels) - 1 else current_level

    def _get_previous_level(self, current_level):
        """Get the previous level in sequence"""
        levels = ["level_1", "level_2", "level_3", "level_4"]
        current_index = levels.index(current_level)
        return levels[current_index - 1] if current_index > 0 else current_level

    def _get_prerequisite_chain(self, course_code, study_plan):
        """Get the chain of prerequisites for a course"""
        chain = []
        courses = self._load_courses()
        
        def add_prereqs(code):
            if code in courses and "prerequisites" in courses[code]:
                for prereq in courses[code]["prerequisites"]:
                    if prereq not in chain:
                        chain.append(prereq)
                        add_prereqs(prereq)
        
        add_prereqs(course_code)
        return chain

    def _select_courses_within_limit(self, courses, credit_limit):
        """Select courses within the credit limit"""
        selected = []
        total_credits = 0
        
        for course in courses:
            if total_credits + course["credits"] <= credit_limit:
                selected.append(course)
                total_credits += course["credits"]
        
        return selected

    def _generate_explanations(self, courses, passed, failed, study_plan, semester):
        """Generate detailed explanations for course recommendations"""
        explanations = []
        current_level = self._get_student_level(passed, study_plan)
        
        for course in courses:
            explanation = f"Recommended {course['code']} ({course['name']}) because:"
            
            # Failed course explanation
            if course["code"] in failed:
                explanation += " You need to retake this failed course."
            
            # Prerequisites explanation
            if "prerequisites" in course:
                prereqs = ", ".join(course["prerequisites"])
                explanation += f" You have completed the prerequisites ({prereqs})."
            
            # Course type explanation
            course_type = course.get("type", "core")
            if course_type == "core":
                explanation += " This is a core course required for your degree."
            elif course_type == "university_compulsory":
                explanation += " This is a compulsory university requirement."
            elif course_type == "field_training":
                explanation += " This is a field training course required for practical experience."
            elif course_type == "graduation":
                explanation += " This is a graduation project/thesis course."
            elif course_type == "elective":
                explanation += " This is a technical elective course for your specialization."
            elif course_type == "university_elective":
                explanation += " This is a university elective course to broaden your knowledge."
            elif course_type == "zero_credit":
                explanation += " This is a zero-credit course required for graduation."
            
            # Level explanation
            course_level = self._get_course_level(course["code"], study_plan)
            if course_level == current_level:
                explanation += f" This course is part of your current level ({current_level})."
            elif course_level == self._get_next_level(current_level):
                explanation += f" This course is from the next level, but you have completed enough credits to take it."
            elif course_level == self._get_previous_level(current_level):
                explanation += f" This course is from a previous level that you haven't completed yet."
            
            # Semester explanation
            if semester in course["semester_offered"]:
                explanation += f" This course is offered in the {semester} semester."
            
            # Credit hours explanation
            if course_type != "zero_credit":
                explanation += f" This course is worth {course['credits']} credit hours."
            else:
                explanation += " This is a zero-credit course."
            
            explanations.append(explanation)
        
        return explanations

def advise_student(cgpa, passed_courses, failed_courses, semester):
    """Main function to get course recommendations"""
    engine = CourseAdvisor()
    engine.reset()
    
    # Declare student profile
    engine.declare(
        StudentProfile(
            cgpa=cgpa,
            passed=passed_courses,
            failed=failed_courses,
            semester=semester
        )
    )
    
    # Run the engine
    engine.run()
    
    # Collect recommendations
    recommendations = []
    for fact in engine.facts.values():
        if isinstance(fact, Course):
            recommendations.append({
                "Course Code": fact["code"],
                "Course Name": fact["name"],
                "Credits": fact["credits"],
                "Type": fact["type"],
                "Semester": fact["semester"],
                "Level": fact["level"]
            })
    
    # Get explanations
    explanations = engine._generate_explanations(
        [engine._load_courses()[r["Course Code"]] for r in recommendations],
        passed_courses,
        failed_courses,
        engine._load_study_plan(),
        semester
    )
    
    return recommendations, explanations
