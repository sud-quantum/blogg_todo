import sqlite3
import os

DATABASE = 'blog_todo.db'

def migrate_database():
    """Add completed_at column to todos table, updated_at column to blogs table, and blog_date column to blogs table"""
    if not os.path.exists(DATABASE):
        print("No existing database found. Run app.py to create a new one.")
        return
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Check if completed_at column exists in todos
    cursor.execute("PRAGMA table_info(todos)")
    todo_columns = [column[1] for column in cursor.fetchall()]
    
    if 'completed_at' not in todo_columns:
        print("Adding completed_at column to todos table...")
        cursor.execute("ALTER TABLE todos ADD COLUMN completed_at TIMESTAMP")
        conn.commit()
        print("Todos table migration completed!")
    else:
        print("Todos table is already up to date.")
    
    # Check if updated_at column exists in blogs
    cursor.execute("PRAGMA table_info(blogs)")
    blog_columns = [column[1] for column in cursor.fetchall()]
    
    if 'updated_at' not in blog_columns:
        print("Adding updated_at column to blogs table...")
        cursor.execute("ALTER TABLE blogs ADD COLUMN updated_at TIMESTAMP")
        conn.commit()
        print("Blogs table updated_at migration completed!")
    else:
        print("Blogs table updated_at is already up to date.")
    
    # Check if blog_date column exists in blogs
    if 'blog_date' not in blog_columns:
        print("Adding blog_date column to blogs table...")
        cursor.execute("ALTER TABLE blogs ADD COLUMN blog_date DATE")
        # Set default date for existing blogs
        from datetime import date
        cursor.execute("UPDATE blogs SET blog_date = ? WHERE blog_date IS NULL", (date.today().isoformat(),))
        conn.commit()
        print("Blogs table blog_date migration completed!")
    else:
        print("Blogs table blog_date is already up to date.")
    
    print("All migrations completed successfully!")
    conn.close()

if __name__ == '__main__':
    migrate_database()
