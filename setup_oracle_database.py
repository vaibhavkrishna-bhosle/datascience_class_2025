"""
Create Oracle User and Tables
This script creates a new user and all required tables for the college management system.
"""

import oracledb

# Admin connection parameters (use SYSTEM or other admin user)
ADMIN_USER = "system"
ADMIN_PASSWORD = "oracle"  # Change this to your SYSTEM password
DB_DSN = "192.168.1.28/XE"

# New user details
NEW_USER = "c##student"
NEW_PASSWORD = "student123"

def create_user_and_grant_privileges():
    """Create user and grant necessary privileges"""
    print("="*60)
    print("CREATING USER AND GRANTING PRIVILEGES")
    print("="*60)
    
    try:
        # Connect as admin
        conn = oracledb.connect(
            user=ADMIN_USER,
            password=ADMIN_PASSWORD,
            dsn=DB_DSN
        )
        print(f"✓ Connected as {ADMIN_USER}")
        
        cursor = conn.cursor()
        
        # Drop user if exists
        try:
            cursor.execute(f"DROP USER {NEW_USER} CASCADE")
            print(f"✓ Dropped existing user {NEW_USER}")
        except:
            print(f"  (User {NEW_USER} doesn't exist yet)")
        
        # Create user
        cursor.execute(f"CREATE USER {NEW_USER} IDENTIFIED BY {NEW_PASSWORD}")
        print(f"✓ Created user: {NEW_USER}")
        
        # Grant privileges
        cursor.execute(f"GRANT CONNECT, RESOURCE TO {NEW_USER}")
        cursor.execute(f"GRANT CREATE SESSION TO {NEW_USER}")
        cursor.execute(f"GRANT CREATE TABLE TO {NEW_USER}")
        cursor.execute(f"GRANT CREATE VIEW TO {NEW_USER}")
        cursor.execute(f"GRANT CREATE SEQUENCE TO {NEW_USER}")
        cursor.execute(f"GRANT UNLIMITED TABLESPACE TO {NEW_USER}")
        print(f"✓ Granted privileges to {NEW_USER}")
        
        conn.commit()
        conn.close()
        
        print("\n✓ User created successfully!")
        return True
        
    except Exception as e:
        print(f"\n✗ Error creating user: {e}")
        return False

def create_tables():
    """Create all tables in the new user schema"""
    print("\n" + "="*60)
    print("CREATING TABLES")
    print("="*60)
    
    try:
        # Connect as new user
        conn = oracledb.connect(
            user=NEW_USER,
            password=NEW_PASSWORD,
            dsn=DB_DSN
        )
        print(f"✓ Connected as {NEW_USER}")
        
        cursor = conn.cursor()
        
        # 1. Drop existing tables (in reverse order of dependencies)
        print("\nDropping existing tables (if any)...")
        tables_to_drop = ['activities', 'fees', 'results', 'attendance', 
                         'enrollments', 'courses', 'students', 'departments']
        
        for table in tables_to_drop:
            try:
                cursor.execute(f"DROP TABLE {table} CASCADE CONSTRAINTS")
                print(f"  ✓ Dropped {table}")
            except:
                pass  # Table doesn't exist
        
        # 2. Create departments table
        print("\n[1/8] Creating departments table...")
        cursor.execute("""
            CREATE TABLE departments (
                dept_id NUMBER PRIMARY KEY,
                dept_name VARCHAR2(100) NOT NULL,
                hod VARCHAR2(100),
                building VARCHAR2(100),
                established_year NUMBER(4)
            )
        """)
        print("  ✓ departments table created")
        
        # 3. Create students table
        print("\n[2/8] Creating students table...")
        cursor.execute("""
            CREATE TABLE students (
                student_id NUMBER PRIMARY KEY,
                full_name VARCHAR2(100) NOT NULL,
                gender VARCHAR2(10) CHECK (gender IN ('Male', 'Female', 'Other')),
                dob DATE NOT NULL,
                city VARCHAR2(50),
                state VARCHAR2(50) DEFAULT 'Karnataka',
                dept_id NUMBER NOT NULL,
                admission_year NUMBER(4) NOT NULL,
                category VARCHAR2(20) CHECK (category IN ('SC', 'ST', 'OBC', 'General')),
                hostel_resident CHAR(1) CHECK (hostel_resident IN ('T', 'F')),
                phone VARCHAR2(15),
                email VARCHAR2(100) UNIQUE,
                CONSTRAINT fk_student_dept FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
            )
        """)
        print("  ✓ students table created")
        
        # 4. Create courses table
        print("\n[3/8] Creating courses table...")
        cursor.execute("""
            CREATE TABLE courses (
                course_id NUMBER PRIMARY KEY,
                course_name VARCHAR2(100) NOT NULL,
                dept_id NUMBER NOT NULL,
                credits NUMBER(1) CHECK (credits BETWEEN 1 AND 6),
                semester_offered NUMBER(1) CHECK (semester_offered BETWEEN 1 AND 6),
                instructor VARCHAR2(100),
                CONSTRAINT fk_course_dept FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
            )
        """)
        print("  ✓ courses table created")
        
        # 5. Create enrollments table
        print("\n[4/8] Creating enrollments table...")
        cursor.execute("""
            CREATE TABLE enrollments (
                enroll_id NUMBER PRIMARY KEY,
                student_id NUMBER NOT NULL,
                course_id NUMBER NOT NULL,
                semester NUMBER(1) CHECK (semester BETWEEN 1 AND 6),
                year NUMBER(4) NOT NULL,
                enrollment_date DATE NOT NULL,
                CONSTRAINT fk_enroll_student FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                CONSTRAINT fk_enroll_course FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
                CONSTRAINT unique_student_course UNIQUE (student_id, course_id, semester, year)
            )
        """)
        print("  ✓ enrollments table created")
        
        # 6. Create attendance table
        print("\n[5/8] Creating attendance table...")
        cursor.execute("""
            CREATE TABLE attendance (
                attendance_id NUMBER PRIMARY KEY,
                student_id NUMBER NOT NULL,
                course_id NUMBER NOT NULL,
                attendance_date DATE NOT NULL,
                status VARCHAR2(10) CHECK (status IN ('Present', 'Absent')),
                lecture_hours NUMBER(1) DEFAULT 0,
                CONSTRAINT fk_attend_student FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                CONSTRAINT fk_attend_course FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
            )
        """)
        print("  ✓ attendance table created")
        
        # 7. Create results table
        print("\n[6/8] Creating results table...")
        cursor.execute("""
            CREATE TABLE results (
                result_id NUMBER PRIMARY KEY,
                student_id NUMBER NOT NULL,
                course_id NUMBER NOT NULL,
                semester NUMBER(1) CHECK (semester BETWEEN 1 AND 6),
                exam_date DATE NOT NULL,
                marks NUMBER(5,2) CHECK (marks BETWEEN 0 AND 100),
                grade VARCHAR2(2) CHECK (grade IN ('A+', 'A', 'B', 'C', 'D', 'F')),
                result_status VARCHAR2(10) CHECK (result_status IN ('Pass', 'Fail')),
                CONSTRAINT fk_result_student FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                CONSTRAINT fk_result_course FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
            )
        """)
        print("  ✓ results table created")
        
        # 8. Create fees table
        print("\n[7/8] Creating fees table...")
        cursor.execute("""
            CREATE TABLE fees (
                receipt_id NUMBER PRIMARY KEY,
                student_id NUMBER NOT NULL,
                amount NUMBER(10,2) NOT NULL CHECK (amount > 0),
                payment_mode VARCHAR2(20) CHECK (payment_mode IN ('Cash', 'Online', 'UPI', 'Cheque')),
                payment_date DATE NOT NULL,
                semester NUMBER(1) CHECK (semester BETWEEN 1 AND 6),
                CONSTRAINT fk_fees_student FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
            )
        """)
        print("  ✓ fees table created")
        
        # 9. Create activities table
        print("\n[8/8] Creating activities table...")
        cursor.execute("""
            CREATE TABLE activities (
                activity_id NUMBER PRIMARY KEY,
                student_id NUMBER NOT NULL,
                activity_name VARCHAR2(100) NOT NULL,
                activity_type VARCHAR2(20) CHECK (activity_type IN ('Cultural', 'Sports', 'Academic', 'NSS')),
                participation_date DATE NOT NULL,
                award_received CHAR(1) CHECK (award_received IN ('Y', 'N')),
                CONSTRAINT fk_activity_student FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
            )
        """)
        print("  ✓ activities table created")
        
        # 10. Create indexes
        print("\nCreating indexes...")
        indexes = [
            "CREATE INDEX idx_student_dept ON students(dept_id)",
            "CREATE INDEX idx_course_dept ON courses(dept_id)",
            "CREATE INDEX idx_enroll_student ON enrollments(student_id)",
            "CREATE INDEX idx_enroll_course ON enrollments(course_id)",
            "CREATE INDEX idx_attend_student ON attendance(student_id)",
            "CREATE INDEX idx_attend_course ON attendance(course_id)",
            "CREATE INDEX idx_attend_date ON attendance(attendance_date)",
            "CREATE INDEX idx_result_student ON results(student_id)",
            "CREATE INDEX idx_result_course ON results(course_id)",
            "CREATE INDEX idx_fees_student ON fees(student_id)",
            "CREATE INDEX idx_fees_date ON fees(payment_date)",
            "CREATE INDEX idx_activity_student ON activities(student_id)"
        ]
        
        for idx_sql in indexes:
            cursor.execute(idx_sql)
        print("  ✓ All indexes created")
        
        # 11. Create sequences
        print("\nCreating sequences...")
        sequences = [
            "CREATE SEQUENCE seq_student_id START WITH 10101 INCREMENT BY 1",
            "CREATE SEQUENCE seq_enroll_id START WITH 5001 INCREMENT BY 1",
            "CREATE SEQUENCE seq_attendance_id START WITH 8001 INCREMENT BY 1",
            "CREATE SEQUENCE seq_result_id START WITH 9001 INCREMENT BY 1",
            "CREATE SEQUENCE seq_receipt_id START WITH 7001 INCREMENT BY 1",
            "CREATE SEQUENCE seq_activity_id START WITH 6001 INCREMENT BY 1"
        ]
        
        for seq_sql in sequences:
            cursor.execute(seq_sql)
        print("  ✓ All sequences created")
        
        conn.commit()
        conn.close()
        
        print("\n" + "="*60)
        print("✓ ALL TABLES CREATED SUCCESSFULLY!")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n✗ Error creating tables: {e}")
        return False

def verify_setup():
    """Verify the setup"""
    print("\n" + "="*60)
    print("VERIFYING SETUP")
    print("="*60)
    
    try:
        conn = oracledb.connect(
            user=NEW_USER,
            password=NEW_PASSWORD,
            dsn=DB_DSN
        )
        
        cursor = conn.cursor()
        
        # List all tables
        cursor.execute("""
            SELECT table_name FROM user_tables ORDER BY table_name
        """)
        
        tables = cursor.fetchall()
        print("\nTables created:")
        for table in tables:
            print(f"  ✓ {table[0]}")
        
        conn.close()
        
    except Exception as e:
        print(f"✗ Error verifying setup: {e}")

def main():
    """Main execution"""
    print("\n" + "="*60)
    print("ORACLE DATABASE SETUP")
    print("College Management System")
    print("="*60)
    
    # Step 1: Create user
    if not create_user_and_grant_privileges():
        print("\n✗ Setup failed at user creation stage")
        return
    
    # Step 2: Create tables
    if not create_tables():
        print("\n✗ Setup failed at table creation stage")
        return
    
    # Step 3: Verify
    verify_setup()
    
    print("\n" + "="*60)
    print("✓ SETUP COMPLETE!")
    print("="*60)
    print(f"\nUser: {NEW_USER}")
    print(f"Password: {NEW_PASSWORD}")
    print("\nYou can now run 'load_data_to_oracle.py' to load the CSV data.")
    print("="*60)

if __name__ == "__main__":
    main()
