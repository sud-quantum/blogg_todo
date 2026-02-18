import sqlite3

# Connect to database
conn = sqlite3.connect('blog_todo.db')
cursor = conn.cursor()

# Update existing user with placeholder values
cursor.execute('''
    UPDATE users 
    SET email = 'user@example.com',
        dob = '2000-01-01',
        gender = 'prefer_not_to_say'
    WHERE email IS NULL
''')

conn.commit()
print(f"Updated {cursor.rowcount} user(s) with default values")

# Show updated users
cursor.execute('SELECT id, username, email, dob, phone, gender FROM users')
rows = cursor.fetchall()
print("\nUpdated users:")
for row in rows:
    print(f"ID: {row[0]}, Username: {row[1]}, Email: {row[2]}, DOB: {row[3]}, Phone: {row[4]}, Gender: {row[5]}")

conn.close()
print("\nYou can now edit your profile to update these values!")
