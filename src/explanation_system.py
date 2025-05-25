# src/explanation_system.py

def explain_recommendation(course_code, course_name, reason):
    return f"✅ {course_code} ({course_name}) recommended → {reason}"

def explain_prerequisite_missing(course_code, course_name, missing):
    return f"❌ {course_code} ({course_name}) not recommended → Missing prerequisites: {', '.join(missing)}."

def explain_not_offered(course_code, course_name, semester):
    return f"❌ {course_code} ({course_name}) not offered in {semester} semester."

def explain_credit_limit_exceeded(course_code, course_name, limit):
    return f"⚠️ Cannot add {course_code} ({course_name}) → Would exceed credit limit of {limit}."

def explain_retake_priority(course_code, course_name):
    return f"🛠️ {course_code} ({course_name}) is prioritized → You failed it previously."

def explain_max_credits(cgpa, max_credits):
    if cgpa < 2.0:
        level = "📉 CGPA < 2.0"
    elif cgpa < 3.0:
        level = "📊 2.0 ≤ CGPA < 3.0"
    else:
        level = "📈 CGPA ≥ 3.0"
    return f"{level} → You are allowed to take up to {max_credits} credit hours."
