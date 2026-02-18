# Blog & Todo Website - Enhanced Edition

A comprehensive Flask-based website combining blogging and advanced todo management with analytics, priority levels, categories, and productivity tracking.

## 🌟 Features

### 📋 Advanced Todo Management
- **Priority Levels (1-5)**: Color-coded priority system (1=Highest/Red, 5=Lowest/Green)
- **Categories**: User-defined categories with custom colors
- **Recurring Todos**: Daily, weekly, or monthly recurring tasks
- **Due Time**: Set specific times for tasks (default 23:59)
- **Comments**: Add optional notes to tasks
- **Search & Filter**: Search by keyword and filter by category
- **Date Navigation**: View todos from any date
- **Smart Reminders**: Notification system for overdue and upcoming tasks

### 📝 Blog Features
- **Rich Text Editor**: Bold, headings (H1, H2, H3), text highlighting
- **Date-Based Organization**: View blogs by specific dates
- **Preview Mode**: View blog content in a modal
- **Edit & Update**: Modify existing blog posts
- **Time Tracking**: Shows created and updated timestamps

### 📊 Dashboard & Analytics
- **Statistics Overview**: Total todos, completion rate, today's progress
- **Activity Calendar**: 90-day heatmap showing daily completions
- **Streak Counter**: Track consecutive days of completing tasks
- **Priority Breakdown**: Visual circles showing tasks by priority
- **Weekly/Monthly Reports**: Completion stats for different time periods
- **Productivity Insights**: Comprehensive analytics

### 👤 User Profile
- **Category Management**: Create, edit, and delete custom categories
- **Progress Tracking**: View overall completion rates and statistics
- **Personal Dashboard**: Centralized view of your productivity

### 🎨 UI/UX Features
- **Dark/Light Theme**: Toggle between themes with persistent preference
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Toast Notifications**: Non-intrusive success/error messages
- **Smooth Animations**: Polished transitions and interactions
- **Accessibility**: WCAG-compliant color contrasts

## 🚀 Installation

### Prerequisites
- Python 3.7+
- pip

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Initialize/Migrate Database
For new installation:
```bash
python app.py
```

For existing database (upgrade):
```bash
python migrate_db.py
```

### Step 3: Run the Application
```bash
python app.py
```

### Step 4: Access the Website
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## 📖 Usage Guide

### Getting Started
1. **Register**: Create a new account
2. **Login**: Access your dashboard
3. **Setup Categories**: Go to Profile → Add categories for organizing todos
4. **Start Adding Todos**: Use the todo page to create tasks with priorities

### Todo Management

#### Adding a Todo
1. Enter task description
2. Select priority level (1-5)
3. Choose a category (optional)
4. Set due time (default 23:59)
5. Select recurring type if needed (daily/weekly/monthly)
6. Click "Add Todo"

#### Managing Todos
- **Complete**: Check the checkbox to mark as done
- **Add Comments**: Click "Comments" button to add notes
- **Delete**: Click trash icon to remove
- **Filter**: Use search bar and category dropdown
- **View Different Dates**: Use date picker at top

### Blog Management

#### Writing a Blog
1. Enter title
2. Use formatting toolbar for rich text
3. Write content in the editor
4. Click "Publish Blog"

#### Managing Blogs
- **Preview**: Click eye icon to view in modal
- **Edit**: Click edit icon to modify
- **Delete**: Click trash icon to remove
- **View by Date**: Use date picker to see blogs from specific dates

### Dashboard Features

#### Statistics
- View total todos, completion rate, and progress
- See today's task completion
- Track weekly and monthly achievements

#### Activity Calendar
- Heatmap shows last 90 days of activity
- Darker colors = more tasks completed
- Hover to see exact counts

#### Streak Counter
- Shows consecutive days of completing tasks
- Motivates daily productivity

#### Priority Breakdown
- Circular progress indicators for each priority level
- Shows distribution of active tasks

### Profile Management

#### Categories
1. Go to Profile page
2. Enter category name
3. Choose a color
4. Click "Add"
5. Delete categories as needed (todos won't be deleted)

#### Progress Tracking
- View overall completion rate
- See total tasks and completed count
- Monitor blog post count

### Reminders

#### Notification Bell
- Located in header next to theme switcher
- Shows count of pending/overdue tasks
- Hover to see reminder list
- Click items to navigate to that date

## 🎨 Priority System

| Priority | Color  | Use Case |
|----------|--------|----------|
| 1        | Red    | Urgent, critical tasks |
| 2        | Orange | High priority, important |
| 3        | Blue   | Medium priority (default) |
| 4        | Purple | Low priority |
| 5        | Green  | Lowest priority, nice-to-have |

## 🔄 Recurring Todos

When you mark a recurring todo as complete:
- **Daily**: Creates a new task for tomorrow
- **Weekly**: Creates a new task for next week (7 days)
- **Monthly**: Creates a new task for next month (30 days)

The new task inherits:
- Task description
- Priority level
- Category
- Due time
- Recurring type

## 🗄️ Database Structure

### Tables
- **users**: User accounts
- **categories**: User-defined categories
- **todos**: Tasks with priority, category, recurring, etc.
- **blogs**: Blog posts with date-based organization

### Key Fields
- **todos.priority**: 1-5 (1=highest)
- **todos.category_id**: Links to categories
- **todos.recurring_type**: 'daily', 'weekly', 'monthly', or NULL
- **todos.due_time**: Time in HH:MM format
- **todos.comments**: Optional notes
- **todos.completed_at**: Timestamp when completed

## 🎯 Keyboard Shortcuts

- **Enter** in search box: Apply filters
- **Tab**: Navigate between form fields

## 🌙 Theme System

### Light Theme
- Clean white backgrounds
- Blue accents
- High contrast for readability

### Dark Theme
- Dark slate backgrounds
- Bright blue accents
- Optimized for low-light environments
- All text clearly visible

Theme preference is saved in browser localStorage.

## 📱 Responsive Design

- **Desktop**: Full feature set with optimal layout
- **Tablet**: Adapted columns and spacing
- **Mobile**: Stacked layout, touch-friendly buttons

## 🔒 Security Features

- Password hashing with Werkzeug
- Session-based authentication
- User data isolation
- SQL injection prevention

## 🐛 Troubleshooting

### Database Issues
```bash
# Reset database (WARNING: Deletes all data)
rm blog_todo.db
python app.py
```

### Migration Issues
```bash
# Run migration script
python migrate_db.py
```

### Port Already in Use
```bash
# Change port in app.py
app.run(debug=True, port=5001)
```

## 📊 Analytics Explained

### Completion Rate
- Percentage of all todos that have been completed
- Formula: (completed_todos / total_todos) × 100

### Streak
- Consecutive days with at least one completed task
- Resets if a day is missed

### Activity Heatmap
- Green intensity shows completion count
- Darker = more tasks completed
- Covers last 90 days

## 🎓 Best Practices

1. **Use Priorities Wisely**: Reserve priority 1 for truly urgent tasks
2. **Categorize Consistently**: Create categories that match your workflow
3. **Set Realistic Due Times**: Don't overload yourself
4. **Review Daily**: Check dashboard for insights
5. **Maintain Streak**: Complete at least one task daily
6. **Add Comments**: Document progress and blockers
7. **Use Recurring**: Automate repetitive tasks

## 🔮 Future Enhancements

Potential features for future versions:
- Subtasks
- File attachments
- Email notifications
- Data export (CSV, JSON)
- Collaboration features
- Mobile app
- Calendar integration

## 📄 License

This project is open source and available for personal and educational use.

## 🤝 Contributing

Feel free to fork, modify, and enhance this project for your needs!

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the usage guide
3. Examine the implementation summary

## 🎉 Enjoy Your Productivity Journey!

Stay organized, track your progress, and achieve your goals with this comprehensive todo and blogging system!
