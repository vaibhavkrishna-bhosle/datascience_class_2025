"""
Generate Indian College Dataset with Data Quality Issues
This script creates a messy dataset that requires cleaning using pandas apply function
"""

from faker import Faker
import pandas as pd
import random
import numpy as np

# Initialize Faker with Indian locale
fake = Faker('en_IN')
Faker.seed(42)
random.seed(42)
np.random.seed(42)

# Indian-specific data
indian_states = ['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Delhi', 'Gujarat', 
                 'West Bengal', 'Telangana', 'Rajasthan', 'Uttar Pradesh', 'Kerala']

departments = ['Computer Science', 'Electronics', 'Mechanical', 'Civil', 
               'Information Technology', 'Electrical', 'Chemical']

courses = ['B.Tech', 'M.Tech', 'B.E', 'M.E', 'BCA', 'MCA']

# Generate base data
num_students = 500

data = {
    'student_id': [],
    'name': [],
    'email': [],
    'phone': [],
    'age': [],
    'gender': [],
    'course': [],
    'department': [],
    'semester': [],
    'cgpa': [],
    'attendance': [],
    'city': [],
    'state': [],
    'admission_date': [],
    'fees_paid': [],
    'hostel': []
}

for i in range(num_students):
    # Generate clean base data
    student_id = f"STU{2020 + random.randint(0, 4)}{random.randint(1000, 9999)}"
    name = fake.name()
    email = fake.email()
    phone = fake.phone_number()
    age = random.randint(17, 28)
    gender = random.choice(['Male', 'Female', 'Other'])
    course = random.choice(courses)
    department = random.choice(departments)
    semester = random.randint(1, 8)
    cgpa = round(random.uniform(5.0, 10.0), 2)
    attendance = round(random.uniform(40, 100), 1)
    city = fake.city()
    state = random.choice(indian_states)
    admission_date = fake.date_between(start_date='-5y', end_date='today')
    fees_paid = random.choice([True, False])
    hostel = random.choice(['Yes', 'No'])
    
    # Add to data
    data['student_id'].append(student_id)
    data['name'].append(name)
    data['email'].append(email)
    data['phone'].append(phone)
    data['age'].append(age)
    data['gender'].append(gender)
    data['course'].append(course)
    data['department'].append(department)
    data['semester'].append(semester)
    data['cgpa'].append(cgpa)
    data['attendance'].append(attendance)
    data['city'].append(city)
    data['state'].append(state)
    data['admission_date'].append(admission_date)
    data['fees_paid'].append(fees_paid)
    data['hostel'].append(hostel)

# Create DataFrame
df = pd.DataFrame(data)

# NOW INTRODUCE DATA QUALITY ISSUES

# 1. Mixed case issues in names (30% of records)
sample_indices = random.sample(range(len(df)), int(len(df) * 0.3))
for idx in sample_indices:
    df.loc[idx, 'name'] = df.loc[idx, 'name'].upper()

sample_indices = random.sample(range(len(df)), int(len(df) * 0.2))
for idx in sample_indices:
    df.loc[idx, 'name'] = df.loc[idx, 'name'].lower()

# 2. Email issues - mixed case and extra spaces (40% of records)
sample_indices = random.sample(range(len(df)), int(len(df) * 0.4))
for idx in sample_indices:
    if random.random() > 0.5:
        df.loc[idx, 'email'] = "  " + df.loc[idx, 'email'] + "  "
    else:
        df.loc[idx, 'email'] = df.loc[idx, 'email'].upper()

# 3. Phone number format inconsistencies
phone_formats = []
for phone in df['phone']:
    choice = random.random()
    if choice < 0.2:
        # Add country code
        phone_formats.append(f"+91-{phone}")
    elif choice < 0.4:
        # Add spaces
        phone_formats.append(phone.replace('-', ' '))
    elif choice < 0.6:
        # Remove all formatting
        phone_formats.append(phone.replace('-', '').replace(' ', ''))
    elif choice < 0.8:
        # Add extra characters
        phone_formats.append(f"({phone})")
    else:
        phone_formats.append(phone)
df['phone'] = phone_formats

# 4. Age issues - some as strings, some negative, some unrealistic
age_issues = []
for age in df['age']:
    choice = random.random()
    if choice < 0.15:
        age_issues.append(str(age))  # String
    elif choice < 0.25:
        age_issues.append(-age)  # Negative
    elif choice < 0.30:
        age_issues.append(age + 50)  # Unrealistic
    else:
        age_issues.append(age)
df['age'] = age_issues

# 5. Gender inconsistencies - different representations
gender_variations = []
for gender in df['gender']:
    if gender == 'Male':
        gender_variations.append(random.choice(['Male', 'M', 'male', 'MALE', 'Man']))
    elif gender == 'Female':
        gender_variations.append(random.choice(['Female', 'F', 'female', 'FEMALE', 'Woman']))
    else:
        gender_variations.append(random.choice(['Other', 'O', 'other', 'Non-Binary']))
df['gender'] = gender_variations

# 6. CGPA issues - out of range, string format
cgpa_issues = []
for cgpa in df['cgpa']:
    choice = random.random()
    if choice < 0.1:
        cgpa_issues.append(str(cgpa))  # String
    elif choice < 0.15:
        cgpa_issues.append(cgpa + 5)  # Out of range (>10)
    elif choice < 0.20:
        cgpa_issues.append(-cgpa)  # Negative
    else:
        cgpa_issues.append(cgpa)
df['cgpa'] = cgpa_issues

# 7. Attendance issues - percentages with % symbol, values > 100
attendance_issues = []
for att in df['attendance']:
    choice = random.random()
    if choice < 0.3:
        attendance_issues.append(f"{att}%")  # Add % symbol
    elif choice < 0.4:
        attendance_issues.append(att + 20)  # Over 100
    else:
        attendance_issues.append(att)
df['attendance'] = attendance_issues

# 8. State names - abbreviations mixed with full names
state_abbrev_map = {
    'Maharashtra': 'MH',
    'Karnataka': 'KA',
    'Tamil Nadu': 'TN',
    'Delhi': 'DL',
    'Gujarat': 'GJ',
    'West Bengal': 'WB',
    'Telangana': 'TS',
    'Rajasthan': 'RJ',
    'Uttar Pradesh': 'UP',
    'Kerala': 'KL'
}

state_issues = []
for state in df['state']:
    if random.random() < 0.4:
        state_issues.append(state_abbrev_map.get(state, state))
    else:
        state_issues.append(state)
df['state'] = state_issues

# 9. Admission date - mixed formats and some as strings
admission_issues = []
for date in df['admission_date']:
    choice = random.random()
    if choice < 0.3:
        # DD/MM/YYYY format
        admission_issues.append(date.strftime('%d/%m/%Y'))
    elif choice < 0.5:
        # DD-MM-YYYY format
        admission_issues.append(date.strftime('%d-%m-%Y'))
    elif choice < 0.6:
        # Month name format
        admission_issues.append(date.strftime('%d %B %Y'))
    else:
        # Keep as YYYY-MM-DD
        admission_issues.append(str(date))
df['admission_date'] = admission_issues

# 10. Fees paid - inconsistent boolean representations
fees_issues = []
for paid in df['fees_paid']:
    if paid:
        fees_issues.append(random.choice([True, 'Yes', 'yes', 'Y', '1', 1, 'True', 'TRUE']))
    else:
        fees_issues.append(random.choice([False, 'No', 'no', 'N', '0', 0, 'False', 'FALSE']))
df['fees_paid'] = fees_issues

# 11. Hostel - mixed yes/no representations with spaces
hostel_issues = []
for hostel in df['hostel']:
    if hostel == 'Yes':
        hostel_issues.append(random.choice(['Yes', 'yes', 'YES', ' Yes ', 'Y', 'y']))
    else:
        hostel_issues.append(random.choice(['No', 'no', 'NO', ' No ', 'N', 'n']))
df['hostel'] = hostel_issues

# 12. Add some missing values (5-10% in various columns)
for col in ['email', 'phone', 'city', 'cgpa', 'attendance']:
    null_indices = random.sample(range(len(df)), int(len(df) * random.uniform(0.05, 0.10)))
    df.loc[null_indices, col] = np.nan

# 13. Add duplicate records (10 duplicates)
duplicate_indices = random.sample(range(len(df)), 10)
duplicates = df.loc[duplicate_indices].copy()
df = pd.concat([df, duplicates], ignore_index=True)

# Shuffle the dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save to CSV
df.to_csv('indian_college_messy_data.csv', index=False)

print(f"Dataset created successfully!")
print(f"Total records: {len(df)}")
print(f"\nDataset preview:")
print(df.head(10))
print(f"\nData types:")
print(df.dtypes)
print(f"\nMissing values:")
print(df.isnull().sum())
