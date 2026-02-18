import sqlite3

DATABASE = 'blog_todo.db'

def migrate():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        # Add new columns to users table
        cursor.execute('ALTER TABLE users ADD COLUMN email TEXT')
        print("Added email column")
    except sqlite3.OperationalError:
        print("email column already exists")
    
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN dob DATE')
        print("Added dob column")
    except sqlite3.OperationalError:
        print("dob column already exists")
    
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN phone TEXT')
        print("Added phone column")
    except sqlite3.OperationalError:
        print("phone column already exists")
    
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN gender TEXT')
        print("Added gender column")
    except sqlite3.OperationalError:
        print("gender column already exists")
    
    conn.commit()
    conn.close()
    print("\nMigration completed successfully!")

if __name__ == '__main__':
    migrate()
