from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

DATABASE = 'blog_todo.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        dob = request.form['dob']
        gender = request.form['gender']
        phone = request.form.get('phone', '')
        
        db = get_db()
        error = None
        
        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif not dob:
            error = 'Date of birth is required.'
        elif not gender:
            error = 'Gender is required.'
        elif db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone():
            error = f'User {username} is already registered.'
        elif db.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone():
            error = f'Email {email} is already registered.'
        
        if error is None:
            db.execute('INSERT INTO users (username, email, password, dob, gender, phone) VALUES (?, ?, ?, ?, ?, ?)',
                      (username, email, generate_password_hash(password), dob, gender, phone))
            db.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        
        flash(error, 'danger')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        
        flash(error, 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    
    # Get statistics
    stats = get_dashboard_stats(db, session['user_id'])
    
    # Get activity calendar data (last 90 days)
    activity_data = get_activity_calendar(db, session['user_id'])
    
    # Get streak
    streak = calculate_streak(db, session['user_id'])
    
    return render_template('dashboard.html', 
                         username=session['username'],
                         stats=stats,
                         activity_data=activity_data,
                         streak=streak)

def get_dashboard_stats(db, user_id):
    today = date.today().isoformat()
    week_ago = (date.today() - timedelta(days=7)).isoformat()
    month_ago = (date.today() - timedelta(days=30)).isoformat()
    
    # Total todos
    total_todos = db.execute('SELECT COUNT(*) as count FROM todos WHERE user_id = ?', 
                            (user_id,)).fetchone()['count']
    
    # Completed todos
    completed_todos = db.execute('SELECT COUNT(*) as count FROM todos WHERE user_id = ? AND completed = 1', 
                                (user_id,)).fetchone()['count']
    
    # Today's todos
    today_todos = db.execute('SELECT COUNT(*) as count FROM todos WHERE user_id = ? AND todo_date = ?', 
                            (user_id, today)).fetchone()['count']
    
    # Today's completed
    today_completed = db.execute('SELECT COUNT(*) as count FROM todos WHERE user_id = ? AND todo_date = ? AND completed = 1', 
                                (user_id, today)).fetchone()['count']
    
    # This week stats
    week_completed = db.execute('SELECT COUNT(*) as count FROM todos WHERE user_id = ? AND completed = 1 AND completed_at >= ?', 
                               (user_id, week_ago)).fetchone()['count']
    
    # This month stats
    month_completed = db.execute('SELECT COUNT(*) as count FROM todos WHERE user_id = ? AND completed = 1 AND completed_at >= ?', 
                                (user_id, month_ago)).fetchone()['count']
    
    # Total blogs
    total_blogs = db.execute('SELECT COUNT(*) as count FROM blogs WHERE user_id = ?', 
                            (user_id,)).fetchone()['count']
    
    # Priority breakdown - Active (uncompleted)
    priority_stats = {}
    for i in range(1, 6):
        count = db.execute('SELECT COUNT(*) as count FROM todos WHERE user_id = ? AND priority = ? AND completed = 0', 
                          (user_id, i)).fetchone()['count']
        priority_stats[i] = count
    
    # Priority breakdown - Completed
    priority_stats_completed = {}
    for i in range(1, 6):
        count = db.execute('SELECT COUNT(*) as count FROM todos WHERE user_id = ? AND priority = ? AND completed = 1', 
                          (user_id, i)).fetchone()['count']
        priority_stats_completed[i] = count
    
    # Priority breakdown - Overall (all tasks)
    priority_stats_overall = {}
    for i in range(1, 6):
        count = db.execute('SELECT COUNT(*) as count FROM todos WHERE user_id = ? AND priority = ?', 
                          (user_id, i)).fetchone()['count']
        priority_stats_overall[i] = count
    
    completion_rate = (completed_todos / total_todos * 100) if total_todos > 0 else 0
    
    return {
        'total_todos': total_todos,
        'completed_todos': completed_todos,
        'today_todos': today_todos,
        'today_completed': today_completed,
        'week_completed': week_completed,
        'month_completed': month_completed,
        'total_blogs': total_blogs,
        'completion_rate': round(completion_rate, 1),
        'priority_stats': priority_stats,
        'priority_stats_completed': priority_stats_completed,
        'priority_stats_overall': priority_stats_overall
    }

def get_activity_calendar(db, user_id):
    end_date = date.today()
    start_date = end_date - timedelta(days=89)
    
    activities = db.execute('''
        SELECT DATE(completed_at) as date, COUNT(*) as count 
        FROM todos 
        WHERE user_id = ? AND completed = 1 AND completed_at >= ? 
        GROUP BY DATE(completed_at)
    ''', (user_id, start_date.isoformat())).fetchall()
    
    activity_dict = {row['date']: row['count'] for row in activities}
    
    calendar_data = []
    current = start_date
    while current <= end_date:
        date_str = current.isoformat()
        calendar_data.append({
            'date': date_str,
            'count': activity_dict.get(date_str, 0)
        })
        current += timedelta(days=1)
    
    return calendar_data

def calculate_streak(db, user_id):
    today = date.today()
    current_date = today
    streak = 0
    
    while True:
        date_str = current_date.isoformat()
        completed = db.execute('''
            SELECT COUNT(*) as count FROM todos 
            WHERE user_id = ? AND DATE(completed_at) = ? AND completed = 1
        ''', (user_id, date_str)).fetchone()['count']
        
        if completed > 0:
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break
        
        if streak > 365:  # Safety limit
            break
    
    return streak

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    
    # Get user details
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    
    # Get categories
    categories = db.execute('SELECT * FROM categories WHERE user_id = ? ORDER BY name', 
                          (session['user_id'],)).fetchall()
    
    # Get progress stats
    stats = get_dashboard_stats(db, session['user_id'])
    
    # Get activity calendar data
    activity_data = get_activity_calendar(db, session['user_id'])
    
    # Get streak
    streak = calculate_streak(db, session['user_id'])
    
    return render_template('profile.html', 
                         username=session['username'],
                         user=user,
                         categories=categories,
                         stats=stats,
                         activity_data=activity_data,
                         streak=streak)

@app.route('/profile/edit', methods=['POST'])
def edit_profile():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    db = get_db()
    
    username = request.json.get('username')
    email = request.json.get('email')
    dob = request.json.get('dob')
    gender = request.json.get('gender')
    phone = request.json.get('phone', '')
    current_password = request.json.get('current_password', '')
    new_password = request.json.get('new_password', '')
    
    # Check if username is taken by another user
    existing_user = db.execute('SELECT id FROM users WHERE username = ? AND id != ?', 
                               (username, session['user_id'])).fetchone()
    if existing_user:
        return jsonify({'error': 'Username already taken'}), 400
    
    # Check if email is taken by another user
    existing_email = db.execute('SELECT id FROM users WHERE email = ? AND id != ?', 
                                (email, session['user_id'])).fetchone()
    if existing_email:
        return jsonify({'error': 'Email already registered'}), 400
    
    # Get current user data
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    
    # Handle password change
    if new_password:
        if not current_password:
            return jsonify({'error': 'Current password is required to change password'}), 400
        
        # Verify current password
        if not check_password_hash(user['password'], current_password):
            return jsonify({'error': 'Current password is incorrect'}), 400
        
        # Update with new password
        db.execute('''UPDATE users SET username = ?, email = ?, dob = ?, gender = ?, phone = ?, password = ? 
                     WHERE id = ?''',
                  (username, email, dob, gender, phone, generate_password_hash(new_password), session['user_id']))
    else:
        # Update without changing password
        db.execute('''UPDATE users SET username = ?, email = ?, dob = ?, gender = ?, phone = ? 
                     WHERE id = ?''',
                  (username, email, dob, gender, phone, session['user_id']))
    
    db.commit()
    
    # Update session username
    session['username'] = username
    
    return jsonify({'success': True, 'message': 'Profile updated successfully!'})

@app.route('/category/add', methods=['POST'])
def add_category():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    name = request.json.get('name')
    color = request.json.get('color', '#3498db')
    
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    
    db = get_db()
    try:
        cursor = db.execute('INSERT INTO categories (user_id, name, color) VALUES (?, ?, ?)',
                          (session['user_id'], name, color))
        db.commit()
        return jsonify({'success': True, 'id': cursor.lastrowid, 'name': name, 'color': color})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Category already exists'}), 400

@app.route('/category/delete/<int:id>', methods=['POST'])
def delete_category(id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    db = get_db()
    # Set category_id to NULL for todos with this category
    db.execute('UPDATE todos SET category_id = NULL WHERE category_id = ? AND user_id = ?',
              (id, session['user_id']))
    db.execute('DELETE FROM categories WHERE id = ? AND user_id = ?', 
              (id, session['user_id']))
    db.commit()
    
    return jsonify({'success': True})

@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    
    # Get selected date and category filter
    selected_date = request.args.get('date', date.today().isoformat())
    category_filter = request.args.get('category', '')
    search_query = request.args.get('search', '')
    
    if request.method == 'POST':
        task = request.form['task']
        todo_date = request.form.get('todo_date', selected_date)
        priority = request.form.get('priority', 3)
        category_id = request.form.get('category_id') or None
        recurring_type = request.form.get('recurring_type') or None
        due_time = request.form.get('due_time', '23:59')
        
        db.execute('''INSERT INTO todos (user_id, task, todo_date, priority, category_id, recurring_type, due_time) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (session['user_id'], task, todo_date, priority, category_id, recurring_type, due_time))
        db.commit()
        flash('Todo added!', 'success')
        return redirect(url_for('todo', date=selected_date))
    
    # Build query with filters
    query = '''SELECT t.*, c.name as category_name, c.color as category_color 
               FROM todos t 
               LEFT JOIN categories c ON t.category_id = c.id 
               WHERE t.user_id = ? AND t.todo_date = ?'''
    params = [session['user_id'], selected_date]
    
    if category_filter:
        query += ' AND t.category_id = ?'
        params.append(category_filter)
    
    if search_query:
        query += ' AND t.task LIKE ?'
        params.append(f'%{search_query}%')
    
    query += ' ORDER BY t.priority ASC, t.created_at DESC'
    
    todos = db.execute(query, params).fetchall()
    
    # Get categories
    categories = db.execute('SELECT * FROM categories WHERE user_id = ? ORDER BY name', 
                          (session['user_id'],)).fetchall()
    
    # Get unique dates that have todos
    todo_dates = db.execute('SELECT DISTINCT todo_date FROM todos WHERE user_id = ?',
                          (session['user_id'],)).fetchall()
    todo_dates_list = [row['todo_date'] for row in todo_dates]
    
    # Get priority stats for reminders
    priority_stats = {}
    for i in range(1, 6):
        count = db.execute('SELECT COUNT(*) as count FROM todos WHERE user_id = ? AND priority = ? AND completed = 0', 
                          (session['user_id'], i)).fetchone()['count']
        priority_stats[i] = count
    
    # Get current time for overdue check
    current_time = datetime.now().strftime('%H:%M')
    is_today = selected_date == date.today().isoformat()
    
    return render_template('todo.html', 
                         todos=todos, 
                         username=session['username'], 
                         selected_date=selected_date,
                         todo_dates=todo_dates_list,
                         categories=categories,
                         category_filter=category_filter,
                         search_query=search_query,
                         priority_stats=priority_stats,
                         current_time=current_time,
                         is_today=is_today)

@app.route('/todo/toggle/<int:id>')
def toggle_todo(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    todo = db.execute('SELECT * FROM todos WHERE id = ? AND user_id = ?',
                     (id, session['user_id'])).fetchone()
    
    if todo:
        new_status = 0 if todo['completed'] else 1
        completed_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S') if new_status else None
        db.execute('UPDATE todos SET completed = ?, completed_at = ? WHERE id = ?', 
                  (new_status, completed_at, id))
        db.commit()
        
        # Handle recurring todos
        if new_status == 1 and todo['recurring_type']:
            create_recurring_todo(db, todo)
    
    selected_date = request.args.get('date', date.today().isoformat())
    return redirect(url_for('todo', date=selected_date))

def create_recurring_todo(db, todo):
    next_date = None
    current_date = datetime.strptime(todo['todo_date'], '%Y-%m-%d').date()
    
    if todo['recurring_type'] == 'daily':
        next_date = current_date + timedelta(days=1)
    elif todo['recurring_type'] == 'weekly':
        next_date = current_date + timedelta(weeks=1)
    elif todo['recurring_type'] == 'monthly':
        next_date = current_date + timedelta(days=30)
    
    if next_date:
        db.execute('''INSERT INTO todos (user_id, task, todo_date, priority, category_id, recurring_type, due_time) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (todo['user_id'], todo['task'], next_date.isoformat(), 
                   todo['priority'], todo['category_id'], todo['recurring_type'], todo['due_time']))
        db.commit()

@app.route('/todo/delete/<int:id>')
def delete_todo(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    db.execute('DELETE FROM todos WHERE id = ? AND user_id = ?', (id, session['user_id']))
    db.commit()
    flash('Todo deleted!', 'success')
    selected_date = request.args.get('date', date.today().isoformat())
    return redirect(url_for('todo', date=selected_date))

@app.route('/todo/comment/<int:id>', methods=['POST'])
def update_todo_comment(id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    db = get_db()
    comments = request.json.get('comments', '')
    
    db.execute('UPDATE todos SET comments = ? WHERE id = ? AND user_id = ?',
              (comments, id, session['user_id']))
    db.commit()
    
    message = 'Comment cleared!' if not comments else 'Comment saved!'
    return jsonify({'success': True, 'comments': comments, 'message': message})

@app.route('/api/reminders')
def get_reminders():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    db = get_db()
    today = date.today().isoformat()
    now = datetime.now()
    current_time = now.strftime('%H:%M')
    
    # Debug: Get all uncompleted todos for today
    all_todos = db.execute('''
        SELECT t.*, c.name as category_name, c.color as category_color
        FROM todos t
        LEFT JOIN categories c ON t.category_id = c.id
        WHERE t.user_id = ? AND t.completed = 0 
        AND t.todo_date = ?
        ORDER BY t.priority ASC, t.due_time ASC
    ''', (session['user_id'], today)).fetchall()
    
    print(f"\n=== REMINDER DEBUG ===")
    print(f"Current time: {current_time}")
    print(f"Today: {today}")
    print(f"Total uncompleted todos today: {len(all_todos)}")
    
    for todo in all_todos:
        print(f"  - Priority {todo['priority']}, Due: {todo['due_time']}, Task: {todo['task'][:30]}")
    
    # Get ALL uncompleted todos for today (show all, not just within 1 hour)
    # This includes overdue and upcoming todos
    reminders = db.execute('''
        SELECT t.*, c.name as category_name, c.color as category_color
        FROM todos t
        LEFT JOIN categories c ON t.category_id = c.id
        WHERE t.user_id = ? AND t.completed = 0 
        AND t.todo_date = ?
        ORDER BY t.priority ASC, t.due_time ASC
        LIMIT 20
    ''', (session['user_id'], today)).fetchall()
    
    print(f"Total reminders (all uncompleted today): {len(reminders)}")
    print("===================\n")
    
    reminder_list = []
    for r in reminders:
        # Check if overdue
        is_overdue = r['due_time'] < current_time
        
        reminder_list.append({
            'id': r['id'],
            'task': r['task'],
            'priority': r['priority'],
            'due_time': r['due_time'],
            'todo_date': r['todo_date'],
            'category_name': r['category_name'],
            'category_color': r['category_color'],
            'is_overdue': is_overdue
        })
    
    return jsonify({'reminders': reminder_list})

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        blog_id = request.form.get('blog_id')
        current_date = date.today().isoformat()
        
        if blog_id:
            db.execute('UPDATE blogs SET title = ?, content = ?, updated_at = ? WHERE id = ? AND user_id = ?',
                      (title, content, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), blog_id, session['user_id']))
            flash('Blog updated!', 'success')
        else:
            db.execute('INSERT INTO blogs (user_id, title, content, blog_date) VALUES (?, ?, ?, ?)',
                      (session['user_id'], title, content, current_date))
            flash('Blog posted!', 'success')
        
        db.commit()
        return redirect(url_for('blog'))
    
    selected_date = request.args.get('date', date.today().isoformat())
    
    blogs = db.execute(
        'SELECT * FROM blogs WHERE user_id = ? AND blog_date = ? ORDER BY created_at DESC',
        (session['user_id'], selected_date)
    ).fetchall()
    
    blog_dates = db.execute(
        'SELECT DISTINCT blog_date FROM blogs WHERE user_id = ?',
        (session['user_id'],)
    ).fetchall()
    blog_dates_list = [row['blog_date'] for row in blog_dates]
    
    return render_template('blog.html', blogs=blogs, username=session['username'], 
                         selected_date=selected_date, blog_dates=blog_dates_list)

@app.route('/blog/get/<int:id>')
def get_blog(id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    db = get_db()
    blog = db.execute('SELECT * FROM blogs WHERE id = ? AND user_id = ?',
                     (id, session['user_id'])).fetchone()
    
    if blog:
        return jsonify({
            'id': blog['id'],
            'title': blog['title'],
            'content': blog['content'],
            'created_at': blog['created_at'],
            'updated_at': blog['updated_at']
        })
    return jsonify({'error': 'Not found'}), 404

@app.route('/blog/delete/<int:id>')
def delete_blog(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    db.execute('DELETE FROM blogs WHERE id = ? AND user_id = ?', (id, session['user_id']))
    db.commit()
    flash('Blog deleted!', 'success')
    return redirect(url_for('blog'))

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True)
