"""
Load CSV Data into Oracle Database
This script reads CSV files from the 'sample dataset' folder and loads them into Oracle tables.
"""

import oracledb
import csv
import os
from datetime import datetime

# Database connection parameters
# Using SYSTEM user since tables are owned by SYSTEM
DB_USER = "system"
DB_PASSWORD = "satyam"
DB_DSN = "192.168.1.28/XE"

# CSV file paths
DATA_DIR = "sample dataset"

def connect_to_db():
    """Establish connection to Oracle database"""
    try:
        conn = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=DB_DSN
        )
        print(f"✓ Connected to Oracle Database (Version: {conn.version})")
        return conn
    except Exception as e:
        print(f"✗ Error connecting to database: {e}")
        return None

def load_departments(conn):
    """Load departments.csv into departments table"""
    print("\n[1/8] Loading Departments...")
    cursor = conn.cursor()
    
    with open(os.path.join(DATA_DIR, 'departments.csv'), 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        
        for row in reader:
            cursor.execute("""
                INSERT INTO departments (dept_id, dept_name, hod, building, established_year)
                VALUES (:1, :2, :3, :4, :5)
            """, (
                int(row['dept_id']),
                row['dept_name'],
                row['hod'],
                row['building'],
                int(row['established_year'])
            ))
            count += 1
        
        conn.commit()
        print(f"  ✓ Loaded {count} departments")

def load_courses(conn):
    """Load courses.csv into courses table"""
    print("\n[2/8] Loading Courses...")
    cursor = conn.cursor()
    
    with open(os.path.join(DATA_DIR, 'courses.csv'), 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        
        for row in reader:
            cursor.execute("""
                INSERT INTO courses (course_id, course_name, dept_id, credits, semester_offered, instructor)
                VALUES (:1, :2, :3, :4, :5, :6)
            """, (
                int(row['course_id']),
                row['course_name'],
                int(row['dept_id']),
                int(row['credits']),
                int(row['semester_offered']),
                row['instructor']
            ))
            count += 1
        
        conn.commit()
        print(f"  ✓ Loaded {count} courses")

def load_students(conn):
    """Load students.csv into students table"""
    print("\n[3/8] Loading Students...")
    cursor = conn.cursor()
    
    with open(os.path.join(DATA_DIR, 'students.csv'), 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        batch = []
        
        for row in reader:
            # Convert boolean string to T/F
            hostel = 'T' if row['hostel_resident'] == 'True' else 'F'
            
            # Convert date string to date object
            dob = datetime.strptime(row['dob'], '%Y-%m-%d').date()
            
            batch.append((
                int(row['student_id']),
                row['full_name'],
                row['gender'],
                dob,
                row['city'],
                row['state'],
                int(row['dept_id']),
                int(row['admission_year']),
                row['category'],
                hostel,
                row['phone'],
                row['email']
            ))
            
            count += 1
            
            # Batch insert every 1000 records
            if len(batch) >= 1000:
                cursor.executemany("""
                    INSERT INTO students (student_id, full_name, gender, dob, city, state, 
                                         dept_id, admission_year, category, hostel_resident, phone, email)
                    VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12)
                """, batch)
                conn.commit()
                print(f"  → {count} students loaded...")
                batch = []
        
        # Insert remaining records
        if batch:
            cursor.executemany("""
                INSERT INTO students (student_id, full_name, gender, dob, city, state, 
                                     dept_id, admission_year, category, hostel_resident, phone, email)
                VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12)
            """, batch)
            conn.commit()
        
        print(f"  ✓ Loaded {count} students")

def load_enrollments(conn):
    """Load enrollments.csv into enrollments table"""
    print("\n[4/8] Loading Enrollments...")
    cursor = conn.cursor()
    
    with open(os.path.join(DATA_DIR, 'enrollments.csv'), 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        batch = []
        
        for row in reader:
            enrollment_date = datetime.strptime(row['enrollment_date'], '%Y-%m-%d').date()
            
            batch.append((
                int(row['enroll_id']),
                int(row['student_id']),
                int(row['course_id']),
                int(row['semester']),
                int(row['year']),
                enrollment_date
            ))
            
            count += 1
            
            if len(batch) >= 1000:
                cursor.executemany("""
                    INSERT INTO enrollments (enroll_id, student_id, course_id, semester, year, enrollment_date)
                    VALUES (:1, :2, :3, :4, :5, :6)
                """, batch)
                conn.commit()
                print(f"  → {count} enrollments loaded...")
                batch = []
        
        if batch:
            cursor.executemany("""
                INSERT INTO enrollments (enroll_id, student_id, course_id, semester, year, enrollment_date)
                VALUES (:1, :2, :3, :4, :5, :6)
            """, batch)
            conn.commit()
        
        print(f"  ✓ Loaded {count} enrollments")

def load_attendance(conn):
    """Load attendance.csv into attendance table"""
    print("\n[5/8] Loading Attendance...")
    cursor = conn.cursor()
    
    with open(os.path.join(DATA_DIR, 'attendance.csv'), 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        batch = []
        
        for row in reader:
            attendance_date = datetime.strptime(row['date'], '%Y-%m-%d').date()
            
            batch.append((
                int(row['attendance_id']),
                int(row['student_id']),
                int(row['course_id']),
                attendance_date,
                row['status'],
                int(row['lecture_hours'])
            ))
            
            count += 1
            
            if len(batch) >= 5000:
                cursor.executemany("""
                    INSERT INTO attendance (attendance_id, student_id, course_id, attendance_date, status, lecture_hours)
                    VALUES (:1, :2, :3, :4, :5, :6)
                """, batch)
                conn.commit()
                print(f"  → {count} attendance records loaded...")
                batch = []
        
        if batch:
            cursor.executemany("""
                INSERT INTO attendance (attendance_id, student_id, course_id, attendance_date, status, lecture_hours)
                VALUES (:1, :2, :3, :4, :5, :6)
            """, batch)
            conn.commit()
        
        print(f"  ✓ Loaded {count} attendance records")

def load_results(conn):
    """Load results.csv into results table"""
    print("\n[6/8] Loading Results...")
    cursor = conn.cursor()
    
    with open(os.path.join(DATA_DIR, 'results.csv'), 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        batch = []
        
        for row in reader:
            exam_date = datetime.strptime(row['exam_date'], '%Y-%m-%d').date()
            
            batch.append((
                int(row['result_id']),
                int(row['student_id']),
                int(row['course_id']),
                int(row['semester']),
                exam_date,
                float(row['marks']),
                row['grade'],
                row['result_status']
            ))
            
            count += 1
            
            if len(batch) >= 5000:
                cursor.executemany("""
                    INSERT INTO results (result_id, student_id, course_id, semester, exam_date, marks, grade, result_status)
                    VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
                """, batch)
                conn.commit()
                print(f"  → {count} results loaded...")
                batch = []
        
        if batch:
            cursor.executemany("""
                INSERT INTO results (result_id, student_id, course_id, semester, exam_date, marks, grade, result_status)
                VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
            """, batch)
            conn.commit()
        
        print(f"  ✓ Loaded {count} results")

def load_fees(conn):
    """Load fees.csv into fees table"""
    print("\n[7/8] Loading Fees...")
    cursor = conn.cursor()
    
    with open(os.path.join(DATA_DIR, 'fees.csv'), 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        batch = []
        
        for row in reader:
            payment_date = datetime.strptime(row['payment_date'], '%Y-%m-%d').date()
            
            batch.append((
                int(row['receipt_id']),
                int(row['student_id']),
                float(row['amount']),
                row['payment_mode'],
                payment_date,
                int(row['semester'])
            ))
            
            count += 1
            
            if len(batch) >= 5000:
                cursor.executemany("""
                    INSERT INTO fees (receipt_id, student_id, amount, payment_mode, payment_date, semester)
                    VALUES (:1, :2, :3, :4, :5, :6)
                """, batch)
                conn.commit()
                print(f"  → {count} fee records loaded...")
                batch = []
        
        if batch:
            cursor.executemany("""
                INSERT INTO fees (receipt_id, student_id, amount, payment_mode, payment_date, semester)
                VALUES (:1, :2, :3, :4, :5, :6)
            """, batch)
            conn.commit()
        
        print(f"  ✓ Loaded {count} fee records")

def load_activities(conn):
    """Load activities.csv into activities table"""
    print("\n[8/8] Loading Activities...")
    cursor = conn.cursor()
    
    with open(os.path.join(DATA_DIR, 'activities.csv'), 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        batch = []
        
        for row in reader:
            participation_date = datetime.strptime(row['participation_date'], '%Y-%m-%d').date()
            award = 'Y' if row['award_received'] == 'Yes' else 'N'
            
            batch.append((
                int(row['activity_id']),
                int(row['student_id']),
                row['activity_name'],
                row['activity_type'],
                participation_date,
                award
            ))
            
            count += 1
            
            if len(batch) >= 1000:
                cursor.executemany("""
                    INSERT INTO activities (activity_id, student_id, activity_name, activity_type, participation_date, award_received)
                    VALUES (:1, :2, :3, :4, :5, :6)
                """, batch)
                conn.commit()
                print(f"  → {count} activity records loaded...")
                batch = []
        
        if batch:
            cursor.executemany("""
                INSERT INTO activities (activity_id, student_id, activity_name, activity_type, participation_date, award_received)
                VALUES (:1, :2, :3, :4, :5, :6)
            """, batch)
            conn.commit()
        
        print(f"  ✓ Loaded {count} activity records")

def verify_data(conn):
    """Verify loaded data counts"""
    print("\n" + "="*60)
    print("DATA VERIFICATION")
    print("="*60)
    
    cursor = conn.cursor()
    
    tables = [
        'departments', 'students', 'courses', 'enrollments',
        'attendance', 'results', 'fees', 'activities'
    ]
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table.capitalize():20s}: {count:>10,} rows")

def main():
    """Main execution function"""
    print("="*60)
    print("COLLEGE MANAGEMENT SYSTEM - DATA LOADER")
    print("="*60)
    
    # Connect to database
    conn = connect_to_db()
    if not conn:
        return
    
    try:
        # Load data in order (respecting foreign key constraints)
        load_departments(conn)
        load_courses(conn)
        load_students(conn)
        load_enrollments(conn)
        load_attendance(conn)
        load_results(conn)
        load_fees(conn)
        load_activities(conn)
        
        # Verify data
        verify_data(conn)
        
        print("\n" + "="*60)
        print("✓ ALL DATA LOADED SUCCESSFULLY!")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ Error during data loading: {e}")
        conn.rollback()
    finally:
        conn.close()
        print("\nDatabase connection closed.")

if __name__ == "__main__":
    main()
