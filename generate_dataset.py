import csv
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
random.seed(42)

# Configuration
NUM_STUDENTS = 10000
NUM_DEPARTMENTS = 4
NUM_COURSES = 10
COURSES_PER_STUDENT = 6
MONTHS_ATTENDANCE = 6

# Helper functions
def generate_phone():
    return f"9{random.randint(100000000, 999999999)}"

def generate_email(name):
    return f"{name.lower().replace(' ', '.')}@college.edu"

def random_date(start_date, end_date):
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    return start_date + timedelta(days=random_days)

# Cities in Bidar district
cities = ["Bidar", "Humnabad", "Basavakalyan", "Bhalki", "Aurad"]
first_names_male = ["Manoj", "Ravi", "Suresh", "Prakash", "Amit", "Vijay", "Arun", "Kiran", "Deepak", "Sandeep", 
                    "Rahul", "Nikhil", "Prashant", "Vishal", "Rohan", "Sachin", "Akash", "Pavan", "Ganesh", "Krishna"]
first_names_female = ["Ananya", "Shreya", "Priya", "Kavya", "Sneha", "Pooja", "Divya", "Anjali", "Neha", "Swati",
                      "Manisha", "Jyoti", "Rekha", "Sunita", "Meena", "Shalini", "Vandana", "Pallavi", "Shweta", "Archana"]
last_names = ["Patil", "Reddy", "Kulkarni", "Desai", "Naik", "Chavan", "Jadhav", "Gowda", "Rao", "Shetty",
              "Kumar", "Singh", "Sharma", "Gupta", "Verma", "Nair", "Menon", "Iyer", "Joshi", "Bhat"]
genders = ["Male", "Female"]
categories = ["General", "OBC", "SC", "ST"]

print("Generating departments.csv...")
# Generate departments
departments = [
    {"dept_id": 1, "dept_name": "Computer Science", "hod": "Dr. Veeresh Desai", "building": "Main Block", "established_year": 2002},
    {"dept_id": 2, "dept_name": "Commerce", "hod": "Prof. Sahana Naik", "building": "Commerce Wing", "established_year": 1998},
    {"dept_id": 3, "dept_name": "Physics", "hod": "Dr. Ravi Chavan", "building": "Science Block", "established_year": 1995},
    {"dept_id": 4, "dept_name": "English", "hod": "Prof. Meenakshi Patil", "building": "Arts Block", "established_year": 2000}
]

with open('sample dataset/departments.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["dept_id", "dept_name", "hod", "building", "established_year"])
    writer.writeheader()
    writer.writerows(departments)

print("Generating courses.csv...")
# Generate courses - distribute 10 courses across 4 departments
course_names_by_dept = {
    1: ["Python Programming", "Data Structures", "Web Development"],
    2: ["Cost Accounting", "Business Mathematics", "Financial Management"],
    3: ["Electrodynamics", "Quantum Mechanics"],
    4: ["British Literature", "Creative Writing"]
}

instructors = ["Prof. Asha Jadhav", "Dr. Ramesh Kumar", "Prof. Lakshmi Nair", "Dr. Sunil Patil", 
               "Prof. Meera Deshmukh", "Dr. Anil Joshi", "Prof. Sunita Rao", "Dr. Prakash Shetty"]

courses = []
course_id = 301
for dept_id, course_list in course_names_by_dept.items():
    for course_name in course_list:
        courses.append({
            "course_id": course_id,
            "course_name": course_name,
            "dept_id": dept_id,
            "credits": random.choice([3, 4]),
            "semester_offered": random.randint(1, 6),
            "instructor": random.choice(instructors)
        })
        course_id += 1

with open('sample dataset/courses.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["course_id", "course_name", "dept_id", "credits", "semester_offered", "instructor"])
    writer.writeheader()
    writer.writerows(courses)

# Create mapping of department to courses
dept_to_courses = {}
for course in courses:
    dept_id = course["dept_id"]
    if dept_id not in dept_to_courses:
        dept_to_courses[dept_id] = []
    dept_to_courses[dept_id].append(course["course_id"])

print("Generating students.csv...")
# Generate students
students = []
start_dob = datetime(2000, 1, 1)
end_dob = datetime(2006, 12, 31)

for i in range(1, NUM_STUDENTS + 1):
    student_id = 100 + i
    gender = random.choice(genders)
    
    if gender == "Male":
        first_name = random.choice(first_names_male)
    else:
        first_name = random.choice(first_names_female)
    
    last_name = random.choice(last_names)
    full_name = f"{first_name} {last_name}"
    
    dept_id = random.randint(1, NUM_DEPARTMENTS)
    
    students.append({
        "student_id": student_id,
        "full_name": full_name,
        "gender": gender,
        "dob": random_date(start_dob, end_dob).strftime("%Y-%m-%d"),
        "city": random.choice(cities),
        "state": "Karnataka",
        "dept_id": dept_id,
        "admission_year": random.choice([2021, 2022, 2023, 2024]),
        "category": random.choice(categories),
        "hostel_resident": random.choice([True, False]),
        "phone": generate_phone(),
        "email": generate_email(full_name) + str(student_id)
    })

with open('sample dataset/students.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["student_id", "full_name", "gender", "dob", "city", "state", 
                                           "dept_id", "admission_year", "category", "hostel_resident", "phone", "email"])
    writer.writeheader()
    writer.writerows(students)

print("Generating enrollments.csv...")
# Generate enrollments - each student enrolls in 6 courses from their department
enrollments = []
enroll_id = 5001
start_enrollment = datetime(2023, 1, 1)
end_enrollment = datetime(2024, 8, 31)

for student in students:
    student_id = student["student_id"]
    dept_id = student["dept_id"]
    
    # Get courses for this department
    available_courses = dept_to_courses[dept_id]
    
    # If department has fewer than 6 courses, repeat some courses across semesters
    selected_courses = []
    if len(available_courses) >= COURSES_PER_STUDENT:
        selected_courses = random.sample(available_courses, COURSES_PER_STUDENT)
    else:
        # Repeat courses if needed
        selected_courses = (available_courses * ((COURSES_PER_STUDENT // len(available_courses)) + 1))[:COURSES_PER_STUDENT]
    
    # Track used combinations to avoid duplicates
    used_combinations = set()
    
    for idx, course_id in enumerate(selected_courses):
        # Assign different semesters to avoid duplicates
        # Distribute across semesters 1-6
        semester = (idx % 6) + 1
        year = 2023 if semester <= 3 else 2024
        
        # Ensure uniqueness
        while (student_id, course_id, semester, year) in used_combinations:
            semester = random.randint(1, 6)
            year = random.choice([2023, 2024])
        
        used_combinations.add((student_id, course_id, semester, year))
        
        enrollments.append({
            "enroll_id": enroll_id,
            "student_id": student_id,
            "course_id": course_id,
            "semester": semester,
            "year": year,
            "enrollment_date": random_date(start_enrollment, end_enrollment).strftime("%Y-%m-%d")
        })
        enroll_id += 1

with open('sample dataset/enrollments.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["enroll_id", "student_id", "course_id", "semester", "year", "enrollment_date"])
    writer.writeheader()
    writer.writerows(enrollments)

print("Generating attendance.csv...")
# Generate attendance - 6 months of data
attendance_records = []
attendance_id = 8001
end_date = datetime(2024, 10, 31)
start_date = end_date - timedelta(days=180)  # 6 months

# Generate attendance for each enrollment
for enrollment in enrollments:
    student_id = enrollment["student_id"]
    course_id = enrollment["course_id"]
    
    # Generate random attendance days (assume 2-3 classes per week over 6 months)
    num_classes = random.randint(40, 60)
    
    for _ in range(num_classes):
        date = random_date(start_date, end_date)
        status = random.choices(["Present", "Absent"], weights=[0.85, 0.15])[0]
        lecture_hours = 2 if status == "Present" else 0
        
        attendance_records.append({
            "attendance_id": attendance_id,
            "student_id": student_id,
            "course_id": course_id,
            "date": date.strftime("%Y-%m-%d"),
            "status": status,
            "lecture_hours": lecture_hours
        })
        attendance_id += 1

# Sort by date
attendance_records.sort(key=lambda x: x["date"])

with open('sample dataset/attendance.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["attendance_id", "student_id", "course_id", "date", "status", "lecture_hours"])
    writer.writeheader()
    writer.writerows(attendance_records)

print("Generating results.csv...")
# Generate results for all enrollments
results = []
result_id = 9001
grade_map = {
    (90, 100): "A+",
    (80, 89): "A",
    (70, 79): "B",
    (60, 69): "C",
    (50, 59): "D",
    (0, 49): "F"
}

for enrollment in enrollments:
    student_id = enrollment["student_id"]
    course_id = enrollment["course_id"]
    semester = enrollment["semester"]
    
    marks = random.randint(35, 100)
    
    # Determine grade
    grade = "F"
    for (min_marks, max_marks), g in grade_map.items():
        if min_marks <= marks <= max_marks:
            grade = g
            break
    
    result_status = "Pass" if marks >= 50 else "Fail"
    
    # Exam date based on semester
    exam_month = 4 if semester % 2 == 0 else 11  # Even semesters in April, odd in November
    exam_date = datetime(2024, exam_month, random.randint(15, 25))
    
    results.append({
        "result_id": result_id,
        "student_id": student_id,
        "course_id": course_id,
        "semester": semester,
        "exam_date": exam_date.strftime("%Y-%m-%d"),
        "marks": marks,
        "grade": grade,
        "result_status": result_status
    })
    result_id += 1

with open('sample dataset/results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["result_id", "student_id", "course_id", "semester", "exam_date", 
                                           "marks", "grade", "result_status"])
    writer.writeheader()
    writer.writerows(results)

print("Generating fees.csv...")
# Generate fees for all students
fees = []
receipt_id = 7001
start_payment = datetime(2023, 1, 1)
end_payment = datetime(2024, 10, 31)
payment_modes = ["Cash", "Online", "UPI"]

for student in students:
    student_id = student["student_id"]
    
    # Generate 2-4 fee payments per student
    num_payments = random.randint(2, 4)
    
    for _ in range(num_payments):
        amount = random.randint(12000, 18000)
        
        fees.append({
            "receipt_id": receipt_id,
            "student_id": student_id,
            "amount": amount,
            "payment_mode": random.choice(payment_modes),
            "payment_date": random_date(start_payment, end_payment).strftime("%Y-%m-%d"),
            "semester": random.randint(1, 6)
        })
        receipt_id += 1

with open('sample dataset/fees.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["receipt_id", "student_id", "amount", "payment_mode", "payment_date", "semester"])
    writer.writeheader()
    writer.writerows(fees)

print("Generating activities.csv...")
# Generate activities - random participation
activities = []
activity_id = 6001
activity_names = [
    ("Tech Fest", "Academic"),
    ("Annual Sports Meet", "Sports"),
    ("Debate Competition", "Cultural"),
    ("Hackathon", "Academic"),
    ("Cricket Tournament", "Sports"),
    ("Music Competition", "Cultural"),
    ("NSS Camp", "NSS"),
    ("Science Exhibition", "Academic"),
    ("Dance Competition", "Cultural"),
    ("Marathon", "Sports")
]
start_activity = datetime(2023, 1, 1)
end_activity = datetime(2024, 10, 31)

# 30-40% of students participate in activities
participating_students = random.sample([s["student_id"] for s in students], k=int(NUM_STUDENTS * 0.35))

for student_id in participating_students:
    # Each participating student joins 1-3 activities
    num_activities = random.randint(1, 3)
    selected_activities = random.sample(activity_names, num_activities)
    
    for activity_name, activity_type in selected_activities:
        activities.append({
            "activity_id": activity_id,
            "student_id": student_id,
            "activity_name": activity_name,
            "activity_type": activity_type,
            "participation_date": random_date(start_activity, end_activity).strftime("%Y-%m-%d"),
            "award_received": random.choice(["Yes", "No"])
        })
        activity_id += 1

with open('sample dataset/activities.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["activity_id", "student_id", "activity_name", "activity_type", 
                                           "participation_date", "award_received"])
    writer.writeheader()
    writer.writerows(activities)

print("\n=== Dataset Generation Complete ===")
print(f"Students: {len(students):,}")
print(f"Departments: {len(departments)}")
print(f"Courses: {len(courses)}")
print(f"Enrollments: {len(enrollments):,}")
print(f"Attendance Records: {len(attendance_records):,}")
print(f"Results: {len(results):,}")
print(f"Fee Payments: {len(fees):,}")
print(f"Activity Participations: {len(activities):,}")
print("\nAll CSV files have been generated in 'sample dataset' folder!")
