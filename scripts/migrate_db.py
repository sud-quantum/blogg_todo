import sqlite3
import os

DATABASE = 'blog_todo.db'

def migrate_database():
    """Migrate database to add new columns and tables"""
    if not os.path.exists(DATABASE):
        print("No existing database found. Run app.py to create a new one.")
        return
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Check todos table columns
    cursor.execute("PRAGMA table_info(todos)")
    todo_columns = [column[1] for column in cursor.fetchall()]
    
    migrations_done = []
    
    if 'completed_at' not in todo_columns:
        cursor.execute("ALTER TABLE todos ADD COLUMN completed_at TIMESTAMP")
        migrations_done.append("todos.completed_at")
    
    if 'comments' not in todo_columns:
        cursor.execute("ALTER TABLE todos ADD COLUMN comments TEXT")
        migrations_done.append("todos.comments")
    
    if 'priority' not in todo_columns:
        cursor.execute("ALTER TABLE todos ADD COLUMN priority INTEGER DEFAULT 3")
        migrations_done.append("todos.priority")
    
    if 'category_id' not in todo_columns:
        cursor.execute("ALTER TABLE todos ADD COLUMN category_id INTEGER")
        migrations_done.append("todos.category_id")
    
    if 'recurring_type' not in todo_columns:
        cursor.execute("ALTER TABLE todos ADD COLUMN recurring_type TEXT")
        migrations_done.append("todos.recurring_type")
    
    if 'due_time' not in todo_columns:
        cursor.execute("ALTER TABLE todos ADD COLUMN due_time TIME DEFAULT '23:59'")
        migrations_done.append("todos.due_time")
    
    # Check blogs table columns
    cursor.execute("PRAGMA table_info(blogs)")
    blog_columns = [column[1] for column in cursor.fetchall()]
    
    if 'updated_at' not in blog_columns:
        cursor.execute("ALTER TABLE blogs ADD COLUMN updated_at TIMESTAMP")
        migrations_done.append("blogs.updated_at")
    
    if 'blog_date' not in blog_columns:
        cursor.execute("ALTER TABLE blogs ADD COLUMN blog_date DATE")
        from datetime import date
        cursor.execute("UPDATE blogs SET blog_date = ? WHERE blog_date IS NULL", (date.today().isoformat(),))
        migrations_done.append("blogs.blog_date")
    
    # Create categories table if it doesn't exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='categories'")
    if not cursor.fetchone():
        cursor.execute("""
            CREATE TABLE categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                color TEXT DEFAULT '#3498db',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id, name)
            )
        """)
        migrations_done.append("categories table created")
    
    conn.commit()
    
    if migrations_done:
        print("Migrations completed:")
        for migration in migrations_done:
            print(f"  ✓ {migration}")
    else:
        print("Database is already up to date.")
    
    conn.close()

if __name__ == '__main__':
    migrate_database()
