# src/app.py

import streamlit as st
import pandas as pd
import os
from inference_engine import advise_student
from knowledge_base import get_all_courses
from student_auth import StudentAuth
from pdf_generator import PDFGenerator

# Initialize components
student_auth = StudentAuth()
pdf_generator = PDFGenerator()

# Load all course data once
all_courses = get_all_courses()
course_codes = list(all_courses.keys())
course_names = {code: all_courses[code]["name"] for code in course_codes}

# Course type colors for better visualization
course_type_colors = {
    "core": "🔵",
    "university_compulsory": "🟢",
    "field_training": "🟡",
    "graduation_project": "🟣",
    "elective": "🟠",
    "university_elective": "⚪",
    "zero_credit": "⚫"
}

# App layout
st.set_page_config(page_title="AIU Course Advisor", layout="wide")
st.title("🎓 AIU Course Registration Advising System")

# Session state initialization
if 'student_info' not in st.session_state:
    st.session_state.student_info = None

# Student Information Form
if st.session_state.student_info is None:
    with st.form("student_info_form"):
        st.header("👤 Student Information")
        
        student_id = st.text_input("Student ID")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        level = st.selectbox("Level", ["1", "2", "3", "4"])
        
        submit = st.form_submit_button("Continue")
        
        if submit:
            if not all([student_id, name, email, level]):
                st.error("Please fill in all fields")
            else:
                st.session_state.student_info = {
                    'student_id': student_id,
                    'name': name,
                    'email': email,
                    'level': level,
                    'registration_date': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.success("Information saved successfully!")
                st.experimental_rerun()

# Main Application
if st.session_state.student_info:
    # Display student info in sidebar
    with st.sidebar:
        st.header("Student Information")
        st.write(f"**ID:** {st.session_state.student_info['student_id']}")
        st.write(f"**Name:** {st.session_state.student_info['name']}")
        st.write(f"**Email:** {st.session_state.student_info['email']}")
        st.write(f"**Level:** {st.session_state.student_info['level']}")
        
        st.markdown("---")
        st.subheader("Course Type Legend")
        for course_type, emoji in course_type_colors.items():
            st.write(f"{emoji} {course_type.replace('_', ' ').title()}")
        
        if st.button("Clear Information"):
            st.session_state.student_info = None
            st.experimental_rerun()

    # Course Recommendation Form
    with st.form("advisor_form"):
        st.header("📋 Course Recommendation Form")

        col1, col2 = st.columns(2)
        with col1:
            semester = st.selectbox("📅 Select Your Upcoming Semester", ["Fall", "Spring"])
        with col2:
            cgpa = st.number_input("📊 Enter Your Current CGPA", min_value=0.0, max_value=4.0, step=0.01)

        # Group courses by type for better organization
        course_groups = {}
        for code in course_codes:
            course_type = all_courses[code].get("type", "core")
            if course_type not in course_groups:
                course_groups[course_type] = []
            course_groups[course_type].append(code)

        # Passed courses selection
        st.subheader("✅ Courses You've Already Passed")
        passed_courses = []
        for course_type, codes in course_groups.items():
            with st.expander(f"{course_type_colors.get(course_type, '⚪')} {course_type.replace('_', ' ').title()}"):
                # Special handling for graduation projects
                if course_type == "graduation_project":
                    # Sort by phase
                    codes.sort(key=lambda x: all_courses[x].get("phase", 0))
                    selected = st.multiselect(
                        f"Select passed graduation project phases",
                        options=codes,
                        format_func=lambda x: f"{x} - {course_names.get(x, '')} (Phase {all_courses[x].get('phase', 'N/A')})",
                        key=f"passed_{course_type}"
                    )
                else:
                    selected = st.multiselect(
                        f"Select passed {course_type} courses",
                        options=codes,
                        format_func=lambda x: f"{x} - {course_names.get(x, '')}",
                        key=f"passed_{course_type}"
                    )
                passed_courses.extend(selected)

        # Failed courses selection
        st.subheader("❌ Courses You've Failed")
        failed_courses = []
        for course_type, codes in course_groups.items():
            with st.expander(f"{course_type_colors.get(course_type, '⚪')} {course_type.replace('_', ' ').title()}"):
                # Special handling for graduation projects
                if course_type == "graduation_project":
                    # Sort by phase
                    codes.sort(key=lambda x: all_courses[x].get("phase", 0))
                    selected = st.multiselect(
                        f"Select failed graduation project phases",
                        options=codes,
                        format_func=lambda x: f"{x} - {course_names.get(x, '')} (Phase {all_courses[x].get('phase', 'N/A')})",
                        key=f"failed_{course_type}"
                    )
                else:
                    selected = st.multiselect(
                        f"Select failed {course_type} courses",
                        options=codes,
                        format_func=lambda x: f"{x} - {course_names.get(x, '')}",
                        key=f"failed_{course_type}"
                    )
                failed_courses.extend(selected)

        submit = st.form_submit_button("Get Course Recommendations")

    # Output
    if submit:
        if cgpa <= 0.0:
            st.error("Please enter a valid CGPA greater than 0.")
        else:
            with st.spinner("Analyzing..."):
                recommendations, explanations = advise_student(cgpa, passed_courses, failed_courses, semester)

            st.success("✅ Recommendation Complete!")

            if recommendations:
                st.subheader("📚 Recommended Courses")
                df = pd.DataFrame(recommendations)
                
                # Add emoji indicators for course types and phase information for graduation projects
                df['Type'] = df.apply(lambda row: 
                    f"{course_type_colors.get(row['Type'], '⚪')} {row['Type'].replace('_', ' ').title()}" + 
                    (f" (Phase {all_courses[row['Course Code']].get('phase', 'N/A')})" 
                     if row['Type'] == 'graduation_project' else ""),
                    axis=1
                )
                
                st.dataframe(df, use_container_width=True)
                st.markdown(f"**Total Credit Hours Recommended:** {df['Credits'].sum()}")
                
                # Generate PDF Report
                pdf_path = pdf_generator.generate_report(
                    st.session_state.student_info,
                    recommendations,
                    explanations
                )
                
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "📥 Download Report (PDF)",
                        f,
                        file_name=f"course_recommendation_{st.session_state.student_info['student_id']}.pdf",
                        mime="application/pdf"
                    )
            else:
                st.warning("⚠️ No eligible courses found for the selected semester and input.")

            st.subheader("🧠 Explanation for Each Recommendation")
            for exp in explanations:
                st.markdown(f"- {exp}")

# Footer
st.markdown("---")
st.caption("AIU CSE Course Registration System • Developed with Streamlit & Experta")
