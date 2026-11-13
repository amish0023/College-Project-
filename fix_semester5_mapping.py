#!/usr/bin/env python
"""Fix Semester 5 subject mapping"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from utils.database import connection

def execute_sql_file(filename):
    """Read and execute SQL file line by line"""
    try:
        with open(filename, 'r') as f:
            sql_content = '\n'.join(
                line for line in f if not line.lstrip().startswith('--')
            )
        
        # Split by ';' to separate statements
        statements = sql_content.split(';')
        
        executed = 0
        with connection() as conn:
            with conn.cursor() as cursor:
                for statement in statements:
                    statement = statement.strip()
                    if statement:
                        try:
                            cursor.execute(statement)
                            # If it's a SELECT statement, print results
                            if 'SELECT' in statement.upper():
                                results = cursor.fetchall()
                                for row in results:
                                    print(row)
                            executed += 1
                        except Exception as e:
                            print(f"Warning: {e}")
                            print(f"Statement: {statement[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file = os.path.join(script_dir, 'fix_semester5_mapping.sql')
    
    if not os.path.exists(sql_file):
        print(f"SQL file not found: {sql_file}")
        sys.exit(1)
    
    print("Fixing Semester 5 subject mapping...\n")
    success = execute_sql_file(sql_file)
    sys.exit(0 if success else 1)
