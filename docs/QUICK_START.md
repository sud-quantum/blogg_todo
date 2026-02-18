# 🚀 Quick Start Guide

## Installation (3 Steps)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migration (if upgrading existing database)
```bash
python migrate_db.py
```

### 3. Start the App
```bash
python app.py
```

Visit: **http://localhost:5000**

---

## First Time Setup

### 1. Register Account
- Click "Register here"
- Enter username and password
- Click "Register"

### 2. Setup Categories (Optional but Recommended)
- Click your username → Profile
- Add categories like: "Work", "Personal", "Shopping", "Health"
- Choose colors for each

### 3. Create Your First Todo
- Go to "My Todos"
- Fill in task description
- Select priority (1-5)
- Choose category
- Set due time
- Click "Add Todo"

---

## Key Features at a Glance

### 📋 Todos
- **Priority**: 1 (Red/Urgent) to 5 (Green/Low)
- **Categories**: Organize by type
- **Recurring**: Auto-create daily/weekly/monthly
- **Due Time**: Set specific deadlines
- **Comments**: Add notes to tasks
- **Search**: Find tasks quickly
- **Filter**: View by category

### 📊 Dashboard
- **Statistics**: Total, completed, today's progress
- **Activity Calendar**: 90-day heatmap
- **Streak**: Consecutive completion days
- **Priority Breakdown**: Visual task distribution

### 📝 Blog
- **Rich Editor**: Bold, headings, highlights
- **Date-Based**: Organize by date
- **Preview**: View before editing
- **Edit**: Update anytime

### 🔔 Reminders
- **Bell Icon**: Shows pending tasks
- **Hover**: See reminder list
- **Badge**: Count of reminders

### 🌙 Theme
- **Toggle**: Sun/moon icon in header
- **Auto-Save**: Preference remembered

---

## Common Tasks

### Add a High Priority Todo
1. Go to Todos
2. Enter task
3. Select Priority 1 (red)
4. Set due time
5. Add

### Create Recurring Task
1. Add todo
2. Select "Daily", "Weekly", or "Monthly"
3. When completed, next task auto-creates

### Filter Todos by Category
1. Use category dropdown
2. Click "Filter"
3. View filtered results

### View Analytics
1. Go to Dashboard
2. See completion rate
3. Check activity calendar
4. View streak counter

### Write a Blog
1. Go to Blog
2. Enter title
3. Use toolbar for formatting
4. Write content
5. Publish

---

## Tips for Success

✅ **Start Small**: Add 3-5 todos for today
✅ **Use Priorities**: Reserve 1 for urgent only
✅ **Create Categories**: Organize your workflow
✅ **Check Dashboard**: Review progress daily
✅ **Maintain Streak**: Complete at least 1 task/day
✅ **Add Comments**: Document progress
✅ **Use Recurring**: Automate repetitive tasks

---

## Troubleshooting

### Can't Login?
- Check username/password
- Try registering new account

### Database Error?
```bash
python migrate_db.py
```

### Port Busy?
Edit app.py, change port:
```python
app.run(debug=True, port=5001)
```

---

## Need Help?

1. Read full README.md
2. Check IMPLEMENTATION_SUMMARY.md
3. Review usage guide in README

---

## 🎉 You're Ready!

Start organizing your tasks and tracking your productivity!
