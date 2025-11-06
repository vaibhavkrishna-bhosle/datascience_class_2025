"""
Check and Fix User Access to Tables
This script checks which user owns the tables and grants access if needed.
"""

import oracledb

# Connection parameters
DB_USER = "c##student"
DB_PASSWORD = "student123"
DB_DSN = "192.168.1.28/XE"

# Admin connection (to check and grant access)
ADMIN_USER = "system"
ADMIN_PASSWORD = "satyam"  # Change this to your SYSTEM password

def check_user_tables():
    """Check what tables the user can see"""
    print("="*60)
    print("CHECKING USER ACCESS")
    print("="*60)
    
    try:
        conn = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=DB_DSN
        )
        print(f"✓ Connected as {DB_USER}")
        
        cursor = conn.cursor()
        
        # Check tables owned by this user
        print("\nTables owned by this user:")
        cursor.execute("SELECT table_name FROM user_tables ORDER BY table_name")
        tables = cursor.fetchall()
        
        if tables:
            for table in tables:
                print(f"  ✓ {table[0]}")
        else:
            print("  ✗ No tables found!")
        
        # Check all accessible tables
        print("\nAll accessible tables:")
        cursor.execute("SELECT owner, table_name FROM all_tables WHERE owner IN ('C##STUDENT', 'SYSTEM', 'SYS') ORDER BY owner, table_name")
        all_tables = cursor.fetchall()
        
        for owner, table_name in all_tables:
            print(f"  - {owner}.{table_name}")
        
        conn.close()
        
        return len(tables) > 0
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def find_table_owner():
    """Find who owns the college management tables"""
    print("\n" + "="*60)
    print("FINDING TABLE OWNERS")
    print("="*60)
    
    try:
        conn = oracledb.connect(
            user=ADMIN_USER,
            password=ADMIN_PASSWORD,
            dsn=DB_DSN
        )
        print(f"✓ Connected as {ADMIN_USER}")
        
        cursor = conn.cursor()
        
        # Find the college management tables
        table_names = ['DEPARTMENTS', 'STUDENTS', 'COURSES', 'ENROLLMENTS',
                      'ATTENDANCE', 'RESULTS', 'FEES', 'ACTIVITIES']
        
        print("\nSearching for college management tables:")
        found_tables = {}
        
        for table_name in table_names:
            cursor.execute("""
                SELECT owner, table_name 
                FROM all_tables 
                WHERE table_name = :1
            """, [table_name])
            
            result = cursor.fetchone()
            if result:
                owner, tname = result
                found_tables[tname] = owner
                print(f"  ✓ {tname} owned by {owner}")
            else:
                print(f"  ✗ {table_name} not found")
        
        conn.close()
        
        return found_tables
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return {}

def grant_access_to_tables(table_owner):
    """Grant access to tables owned by another user"""
    print("\n" + "="*60)
    print("GRANTING ACCESS TO TABLES")
    print("="*60)
    
    try:
        conn = oracledb.connect(
            user=ADMIN_USER,
            password=ADMIN_PASSWORD,
            dsn=DB_DSN
        )
        print(f"✓ Connected as {ADMIN_USER}")
        
        cursor = conn.cursor()
        
        # First, grant CREATE SYNONYM privilege
        try:
            cursor.execute(f"GRANT CREATE SYNONYM TO {DB_USER}")
            print(f"  ✓ Granted CREATE SYNONYM privilege to {DB_USER}")
        except Exception as e:
            print(f"  ⚠ Warning granting CREATE SYNONYM: {e}")
        
        table_names = ['DEPARTMENTS', 'STUDENTS', 'COURSES', 'ENROLLMENTS',
                      'ATTENDANCE', 'RESULTS', 'FEES', 'ACTIVITIES']
        
        for table_name in table_names:
            try:
                grant_sql = f"GRANT ALL ON {table_owner}.{table_name} TO {DB_USER}"
                cursor.execute(grant_sql)
                print(f"  ✓ Granted access to {table_owner}.{table_name}")
            except Exception as e:
                print(f"  ✗ Error granting access to {table_name}: {e}")
        
        conn.commit()
        conn.close()
        
        print("\n✓ Access granted!")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def create_synonyms(table_owner):
    """Create synonyms so user can access tables without schema prefix"""
    print("\n" + "="*60)
    print("CREATING SYNONYMS")
    print("="*60)
    
    try:
        conn = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=DB_DSN
        )
        print(f"✓ Connected as {DB_USER}")
        
        cursor = conn.cursor()
        
        table_names = ['DEPARTMENTS', 'STUDENTS', 'COURSES', 'ENROLLMENTS',
                      'ATTENDANCE', 'RESULTS', 'FEES', 'ACTIVITIES']
        
        for table_name in table_names:
            try:
                # Drop existing synonym if it exists
                cursor.execute(f"DROP SYNONYM {table_name}")
            except:
                pass
            
            try:
                synonym_sql = f"CREATE SYNONYM {table_name} FOR {table_owner}.{table_name}"
                cursor.execute(synonym_sql)
                print(f"  ✓ Created synonym for {table_name}")
            except Exception as e:
                print(f"  ✗ Error creating synonym for {table_name}: {e}")
        
        conn.commit()
        conn.close()
        
        print("\n✓ Synonyms created!")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def verify_access():
    """Verify that user can now access the tables"""
    print("\n" + "="*60)
    print("VERIFYING ACCESS")
    print("="*60)
    
    try:
        conn = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=DB_DSN
        )
        print(f"✓ Connected as {DB_USER}")
        
        cursor = conn.cursor()
        
        table_names = ['DEPARTMENTS', 'STUDENTS', 'COURSES', 'ENROLLMENTS',
                      'ATTENDANCE', 'RESULTS', 'FEES', 'ACTIVITIES']
        
        print("\nTesting table access:")
        all_ok = True
        
        for table_name in table_names:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"  ✓ {table_name}: {count} rows")
            except Exception as e:
                print(f"  ✗ {table_name}: Cannot access - {e}")
                all_ok = False
        
        conn.close()
        
        return all_ok
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Main execution"""
    print("\n" + "="*60)
    print("ORACLE USER ACCESS TROUBLESHOOTING")
    print("="*60)
    
    # Step 1: Check current user access
    has_tables = check_user_tables()
    
    if has_tables:
        print("\n✓ User already has access to tables!")
        return
    
    # Step 2: Find who owns the tables
    found_tables = find_table_owner()
    
    if not found_tables:
        print("\n✗ Tables not found in database!")
        print("Please run the table creation script first.")
        return
    
    # Get the owner (should be the same for all tables)
    table_owner = list(found_tables.values())[0]
    
    # Step 3: Grant access
    if table_owner != DB_USER.upper():
        print(f"\nTables are owned by {table_owner}, not by {DB_USER}")
        print("Granting access...")
        
        if grant_access_to_tables(table_owner):
            # Step 4: Create synonyms
            create_synonyms(table_owner)
        else:
            print("\n✗ Failed to grant access. Check admin credentials.")
            return
    
    # Step 5: Verify
    if verify_access():
        print("\n" + "="*60)
        print("✓ ACCESS FIXED SUCCESSFULLY!")
        print("="*60)
        print("\nYou can now run 'load_data_to_oracle.py' to load the CSV data.")
    else:
        print("\n✗ Still having access issues. Please check the errors above.")

if __name__ == "__main__":
    main()
