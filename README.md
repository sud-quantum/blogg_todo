# Blog & Todo Website

A modern Flask-based website combining blogging and todo management with dark/light theme support.

## Features

### Todo Management
- Interactive calendar view to select dates
- Create daily todos with selected dates
- View todos organized by date
- Separate sections for current and finished todos
- Mark todos as complete/incomplete
- Timestamps for when todos are added and finished
- Delete todos
- Visual indicators on calendar for dates with todos

### Blog
- Rich text editor with formatting options:
  - Bold text
  - 3 heading sizes (H1, H2, H3)
  - Text highlighting (Yellow, Green, Pink, Blue)
  - Clear formatting
- View all your blog posts with timestamps
- Delete blog posts
- Shows username, date, and time for each post

### User Interface
- Dark/Light theme switcher
- Modern, clean design with smooth transitions
- Profile dropdown with logout option
- Responsive layout for mobile and desktop
- Beautiful color scheme that adapts to theme

### User Authentication
- Register new account
- Login/Logout
- Each user sees only their own content

## Installation

1. Install Python dependencies:
```
pip install -r requirements.txt
```

2. Run the application:
```
python app.py
```

3. Open your browser and go to:
```
http://127.0.0.1:5000
```

## Database Migration

If you're upgrading from an older version, run the migration script:
```
python migrate_db.py
```

## Usage

1. Register a new account
2. Login with your credentials
3. Toggle between dark and light themes using the switcher in the navbar
4. Use the dashboard to navigate to Todos or Blog
5. In Todos:
   - Click on any date in the calendar to select it
   - Add a new todo for the selected date
   - View current and finished todos separately
   - Check off todos to mark them as complete
6. In Blog:
   - Write blog posts with rich text formatting
   - Use the toolbar to format your text
   - View all your posts with timestamps

## Database

The app uses SQLite database (blog_todo.db) which is created automatically on first run.

## Theme

The website supports both light and dark themes. Your preference is saved in browser localStorage and persists across sessions.
