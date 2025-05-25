# 🎓 AIU CSE Course Registration Advising System

An intelligent Knowledge-Based System (KBS) for course registration advising in the Computer Science and Engineering department at Alamein International University. This system helps CSE students select appropriate courses based on their academic history and compliance with university policies.

## 🌟 Features

- **Smart Course Recommendations**
  - Based on academic history and CGPA
  - Considers prerequisites and course dependencies
  - Respects university credit limits
  - Prioritizes courses based on level and semester

- **Comprehensive Course Management**
  - Core courses
  - University compulsory courses
  - Field training courses
  - Graduation projects
  - Technical electives
  - University electives
  - Zero-credit courses

- **Student Information Management**
  - Student profile management
  - Academic history tracking
  - Course completion status
  - CGPA-based credit limits

- **Detailed Explanations**
  - Clear reasoning for each recommendation
  - Prerequisite completion status
  - Course type and level information
  - Semester availability

- **PDF Report Generation**
  - Professional course recommendation reports
  - Student information summary
  - Detailed course explanations
  - Credit hour calculations

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Knowledge Engine**: Experta
- **Data Management**: JSON
- **PDF Generation**: ReportLab
- **Data Processing**: Pandas

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/aiu-cse-advisor.git
   cd aiu-cse-advisor
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

1. Start the application:
   ```bash
   streamlit run src/app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:****
   ```

3. Follow the on-screen instructions:
   - Enter student information
   - Select passed and failed courses
   - Enter CGPA and semester
   - Get course recommendations
   - Download PDF report

## 📁 Project Structure

```
AIU CSE Course Registration Advising System/
├── data/
│   ├── Courses/
│   │   ├── Core_courses.json
│   │   ├── Electives/
│   │   ├── FT_courses.json
│   │   ├── Graduation_courses.json
│   │   └── UniReq/
│   ├── Policies.json
│   ├── StudyPlan.json
│   └── students.json
├── src/
│   ├── app.py
│   ├── inference_engine.py
│   ├── explanation_system.py
│   ├── knowledge_base_editor.py
│   ├── knowledge_base.py
│   ├── pdf_generator.py
│   └── student_auth.py
├── reports/
├── requirements.txt
└── README.md
```

## 🧠 Knowledge Base

The system uses several JSON files to maintain its knowledge base:

- **Core_courses.json**: Core CSE courses
- **Electives/**: Technical elective courses
- **FT_courses.json**: Field training courses
- **Graduation_courses.json**: Graduation project courses
- **Policies.json**: University policies and credit limits
- **StudyPlan.json**: Course study plan and prerequisites
- **UniReq/**: University requirement courses

## 📊 Course Prioritization

Courses are prioritized based on multiple factors:

1. Failed courses (highest priority)
2. Level-based priority
   - Current level courses
   - Next level courses
   - Previous level courses
3. Course type priority
   - Core courses
   - University compulsory
   - Field training
   - Graduation
   - Electives
4. Semester alignment
5. Prerequisite chain
6. Credit hours

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
