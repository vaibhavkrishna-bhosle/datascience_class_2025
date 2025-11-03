"""
Clear All Data from Oracle Tables
This script truncates all tables to prepare for a fresh data load.
"""

import oracledb

# Admin connection (tables are owned by SYSTEM)
ADMIN_USER = "system"
ADMIN_PASSWORD = "satyam"
DB_DSN = "192.168.1.28/XE"

def clear_all_tables():
    """Truncate all tables to remove existing data"""
    print("="*60)
    print("CLEARING ALL TABLE DATA")
    print("="*60)
    
    try:
        conn = oracledb.connect(
            user=ADMIN_USER,
            password=ADMIN_PASSWORD,
            dsn=DB_DSN
        )
        print(f"✓ Connected as {ADMIN_USER}")
        
        cursor = conn.cursor()
        
        # Disable foreign key constraints temporarily
        print("\nDisabling foreign key constraints...")
        cursor.execute("""
            BEGIN
                FOR c IN (SELECT constraint_name, table_name 
                         FROM user_constraints 
                         WHERE constraint_type = 'R'
                         AND table_name IN ('ACTIVITIES', 'FEES', 'RESULTS', 'ATTENDANCE', 
                                           'ENROLLMENTS', 'COURSES', 'STUDENTS', 'DEPARTMENTS'))
                LOOP
                    EXECUTE IMMEDIATE 'ALTER TABLE ' || c.table_name || 
                                    ' DISABLE CONSTRAINT ' || c.constraint_name;
                END LOOP;
            END;
        """)
        print("  ✓ Foreign key constraints disabled")
        
        # Truncate tables (in reverse order of dependencies)
        tables = ['ACTIVITIES', 'FEES', 'RESULTS', 'ATTENDANCE', 
                 'ENROLLMENTS', 'COURSES', 'STUDENTS', 'DEPARTMENTS']
        
        print("\nTruncating tables...")
        for table in tables:
            try:
                cursor.execute(f"TRUNCATE TABLE {table}")
                print(f"  ✓ Truncated {table}")
            except Exception as e:
                print(f"  ✗ Error truncating {table}: {e}")
        
        # Re-enable foreign key constraints
        print("\nRe-enabling foreign key constraints...")
        cursor.execute("""
            BEGIN
                FOR c IN (SELECT constraint_name, table_name 
                         FROM user_constraints 
                         WHERE constraint_type = 'R'
                         AND table_name IN ('ACTIVITIES', 'FEES', 'RESULTS', 'ATTENDANCE', 
                                           'ENROLLMENTS', 'COURSES', 'STUDENTS', 'DEPARTMENTS'))
                LOOP
                    EXECUTE IMMEDIATE 'ALTER TABLE ' || c.table_name || 
                                    ' ENABLE CONSTRAINT ' || c.constraint_name;
                END LOOP;
            END;
        """)
        print("  ✓ Foreign key constraints re-enabled")
        
        conn.commit()
        
        # Verify tables are empty
        print("\n" + "="*60)
        print("VERIFICATION")
        print("="*60)
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table:20s}: {count} rows")
        
        conn.close()
        
        print("\n" + "="*60)
        print("✓ ALL TABLES CLEARED SUCCESSFULLY!")
        print("="*60)
        print("\nYou can now run 'load_data_to_oracle.py' to load fresh data.")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False

def main():
    """Main execution"""
    print("\n" + "="*60)
    print("ORACLE TABLE DATA CLEANER")
    print("="*60)
    
    response = input("\n⚠ WARNING: This will delete ALL data from the tables.\nContinue? (yes/no): ")
    
    if response.lower() == 'yes':
        clear_all_tables()
    else:
        print("\nOperation cancelled.")

if __name__ == "__main__":
    main()
