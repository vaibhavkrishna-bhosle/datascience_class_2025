-- ============================================================================
-- College Management System - Database Schema
-- ============================================================================
-- This script creates tables for managing student data, courses, attendance,
-- fees, results, and extracurricular activities for a college in Bidar, Karnataka
-- ============================================================================

-- Drop tables if they exist (in reverse order of dependencies)
DROP TABLE activities CASCADE CONSTRAINTS;
DROP TABLE fees CASCADE CONSTRAINTS;
DROP TABLE results CASCADE CONSTRAINTS;
DROP TABLE attendance CASCADE CONSTRAINTS;
DROP TABLE enrollments CASCADE CONSTRAINTS;
DROP TABLE courses CASCADE CONSTRAINTS;
DROP TABLE students CASCADE CONSTRAINTS;
DROP TABLE departments CASCADE CONSTRAINTS;

-- ============================================================================
-- 1. DEPARTMENTS TABLE
-- ============================================================================
CREATE TABLE departments (
    dept_id NUMBER PRIMARY KEY,
    dept_name VARCHAR2(100) NOT NULL,
    hod VARCHAR2(100),
    building VARCHAR2(100),
    established_year NUMBER(4)
);

-- ============================================================================
-- 2. STUDENTS TABLE
-- ============================================================================
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
);

-- ============================================================================
-- 3. COURSES TABLE
-- ============================================================================
CREATE TABLE courses (
    course_id NUMBER PRIMARY KEY,
    course_name VARCHAR2(100) NOT NULL,
    dept_id NUMBER NOT NULL,
    credits NUMBER(1) CHECK (credits BETWEEN 1 AND 6),
    semester_offered NUMBER(1) CHECK (semester_offered BETWEEN 1 AND 6),
    instructor VARCHAR2(100),
    CONSTRAINT fk_course_dept FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

-- ============================================================================
-- 4. ENROLLMENTS TABLE
-- ============================================================================
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
);

-- ============================================================================
-- 5. ATTENDANCE TABLE
-- ============================================================================
CREATE TABLE attendance (
    attendance_id NUMBER PRIMARY KEY,
    student_id NUMBER NOT NULL,
    course_id NUMBER NOT NULL,
    attendance_date DATE NOT NULL,
    status VARCHAR2(10) CHECK (status IN ('Present', 'Absent')),
    lecture_hours NUMBER(1) DEFAULT 0,
    CONSTRAINT fk_attend_student FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    CONSTRAINT fk_attend_course FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
);

-- ============================================================================
-- 6. RESULTS TABLE
-- ============================================================================
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
);

-- ============================================================================
-- 7. FEES TABLE
-- ============================================================================
CREATE TABLE fees (
    receipt_id NUMBER PRIMARY KEY,
    student_id NUMBER NOT NULL,
    amount NUMBER(10,2) NOT NULL CHECK (amount > 0),
    payment_mode VARCHAR2(20) CHECK (payment_mode IN ('Cash', 'Online', 'UPI', 'Cheque')),
    payment_date DATE NOT NULL,
    semester NUMBER(1) CHECK (semester BETWEEN 1 AND 6),
    CONSTRAINT fk_fees_student FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- ============================================================================
-- 8. ACTIVITIES TABLE
-- ============================================================================
CREATE TABLE activities (
    activity_id NUMBER PRIMARY KEY,
    student_id NUMBER NOT NULL,
    activity_name VARCHAR2(100) NOT NULL,
    activity_type VARCHAR2(20) CHECK (activity_type IN ('Cultural', 'Sports', 'Academic', 'NSS')),
    participation_date DATE NOT NULL,
    award_received CHAR(1) CHECK (award_received IN ('Y', 'N')),
    CONSTRAINT fk_activity_student FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- ============================================================================
-- CREATE INDEXES FOR BETTER QUERY PERFORMANCE
-- ============================================================================

-- Indexes on foreign keys
CREATE INDEX idx_student_dept ON students(dept_id);
CREATE INDEX idx_course_dept ON courses(dept_id);
CREATE INDEX idx_enroll_student ON enrollments(student_id);
CREATE INDEX idx_enroll_course ON enrollments(course_id);
CREATE INDEX idx_attend_student ON attendance(student_id);
CREATE INDEX idx_attend_course ON attendance(course_id);
CREATE INDEX idx_attend_date ON attendance(attendance_date);
CREATE INDEX idx_result_student ON results(student_id);
CREATE INDEX idx_result_course ON results(course_id);
CREATE INDEX idx_fees_student ON fees(student_id);
CREATE INDEX idx_fees_date ON fees(payment_date);
CREATE INDEX idx_activity_student ON activities(student_id);

-- ============================================================================
-- CREATE SEQUENCES FOR AUTO-INCREMENT (IF NEEDED)
-- ============================================================================

CREATE SEQUENCE seq_student_id START WITH 10101 INCREMENT BY 1;
CREATE SEQUENCE seq_enroll_id START WITH 5001 INCREMENT BY 1;
CREATE SEQUENCE seq_attendance_id START WITH 8001 INCREMENT BY 1;
CREATE SEQUENCE seq_result_id START WITH 9001 INCREMENT BY 1;
CREATE SEQUENCE seq_receipt_id START WITH 7001 INCREMENT BY 1;
CREATE SEQUENCE seq_activity_id START WITH 6001 INCREMENT BY 1;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Display all created tables
SELECT table_name FROM user_tables ORDER BY table_name;

-- Display all constraints
SELECT constraint_name, constraint_type, table_name 
FROM user_constraints 
WHERE table_name IN ('DEPARTMENTS', 'STUDENTS', 'COURSES', 'ENROLLMENTS', 
                     'ATTENDANCE', 'RESULTS', 'FEES', 'ACTIVITIES')
ORDER BY table_name, constraint_type;

-- Display all indexes
SELECT index_name, table_name, uniqueness 
FROM user_indexes 
WHERE table_name IN ('DEPARTMENTS', 'STUDENTS', 'COURSES', 'ENROLLMENTS', 
                     'ATTENDANCE', 'RESULTS', 'FEES', 'ACTIVITIES')
ORDER BY table_name;

COMMIT;

-- ============================================================================
-- END OF SCRIPT
-- ============================================================================
