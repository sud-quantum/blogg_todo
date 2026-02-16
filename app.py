from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
import os

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
        password = request.form['password']
        
        db = get_db()
        error = None
        
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone():
            error = f'User {username} is already registered.'
        
        if error is None:
            db.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                      (username, generate_password_hash(password)))
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
    return render_template('dashboard.html', username=session['username'])

@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    
    # Get selected date from query parameter or use today
    selected_date = request.args.get('date', date.today().isoformat())
    
    if request.method == 'POST':
        task = request.form['task']
        todo_date = request.form.get('todo_date', selected_date)
        
        db.execute('INSERT INTO todos (user_id, task, todo_date) VALUES (?, ?, ?)',
                  (session['user_id'], task, todo_date))
        db.commit()
        flash('Todo added!', 'success')
        return redirect(url_for('todo', date=selected_date))
    
    # Get todos for selected date only
    todos = db.execute(
        'SELECT * FROM todos WHERE user_id = ? AND todo_date = ? ORDER BY created_at DESC',
        (session['user_id'], selected_date)
    ).fetchall()
    
    # Get unique dates that have todos
    todo_dates = db.execute(
        'SELECT DISTINCT todo_date FROM todos WHERE user_id = ?',
        (session['user_id'],)
    ).fetchall()
    todo_dates_list = [row['todo_date'] for row in todo_dates]
    
    return render_template('todo.html', todos=todos, username=session['username'], 
                         selected_date=selected_date, todo_dates=todo_dates_list)

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
    
    selected_date = request.args.get('date', date.today().isoformat())
    return redirect(url_for('todo', date=selected_date))

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
            # Update existing blog
            db.execute('UPDATE blogs SET title = ?, content = ?, updated_at = ? WHERE id = ? AND user_id = ?',
                      (title, content, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), blog_id, session['user_id']))
            flash('Blog updated!', 'success')
        else:
            # Create new blog with current date
            db.execute('INSERT INTO blogs (user_id, title, content, blog_date) VALUES (?, ?, ?, ?)',
                      (session['user_id'], title, content, current_date))
            flash('Blog posted!', 'success')
        
        db.commit()
        return redirect(url_for('blog'))
    
    # Get selected date from query parameter or use today
    selected_date = request.args.get('date', date.today().isoformat())
    
    blogs = db.execute(
        'SELECT * FROM blogs WHERE user_id = ? AND blog_date = ? ORDER BY created_at DESC',
        (session['user_id'], selected_date)
    ).fetchall()
    
    # Get all dates that have blogs
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
