# Reminder Troubleshooting Guide

## Issue: "No reminders" showing even when you have todos

### Step 1: Check Browser Console
1. Open your browser
2. Press F12 to open Developer Tools
3. Go to the "Console" tab
4. Look for the debug output that looks like:

```
=== FRONTEND REMINDER DEBUG ===
Current time: 2:30:45 PM
Reminders received: []
Count: 0
================================
```

### Step 2: Check Server Console
Look at your Flask server terminal output for:

```
=== REMINDER DEBUG ===
Current time: 14:30
One hour later: 15:30
Today: 2026-02-18
Total uncompleted todos today: 5
  - Priority 1, Due: 15:00, Task: High priority task
  - Priority 3, Due: 14:45, Task: Medium priority task
  - Priority 4, Due: 16:00, Task: Low priority task
Filtered reminders (P3,4,5 due <= 15:30): 1
===================
```

### Step 3: Understand the Criteria

For a todo to appear in reminders, ALL of these must be true:

1. ✅ **Priority**: Must be 3, 4, or 5 (NOT 1 or 2)
2. ✅ **Date**: Must be TODAY's date
3. ✅ **Status**: Must NOT be completed
4. ✅ **Time**: Due time must be within the next hour

### Step 4: Common Reasons for "No reminders"

#### Reason 1: Wrong Priority
❌ **Problem**: Your todos are priority 1 or 2
✅ **Solution**: Create todos with priority 3, 4, or 5

#### Reason 2: Wrong Time
❌ **Problem**: Your todos are due more than 1 hour from now
✅ **Solution**: 
- If current time is 2:00 PM, todos must be due by 3:00 PM
- Create a todo with due time within the next hour

#### Reason 3: Wrong Date
❌ **Problem**: Your todos are for yesterday or tomorrow
✅ **Solution**: Make sure todos are for TODAY's date

#### Reason 4: Already Completed
❌ **Problem**: Your todos are marked as completed
✅ **Solution**: Uncheck the todos to mark them as incomplete

### Step 5: Test with a Sample Todo

Create a test todo with these exact settings:

1. **Task**: "Test reminder"
2. **Priority**: 3 (or 4 or 5)
3. **Date**: Today's date
4. **Due Time**: 15 minutes from now
5. **Status**: Unchecked (not completed)

Wait a few seconds and check the bell icon. You should see:
- Red badge with "1"
- Hover shows the todo in the dropdown

### Step 6: Check the API Directly

1. Open your browser
2. Go to: `http://127.0.0.1:5000/api/reminders`
3. You should see JSON like:

```json
{
  "reminders": [
    {
      "id": 1,
      "task": "Test reminder",
      "priority": 3,
      "due_time": "14:45",
      "todo_date": "2026-02-18",
      "category_name": null,
      "category_color": null
    }
  ]
}
```

If you see `"reminders": []`, then no todos match the criteria.

### Step 7: Time Format Check

Make sure your due times are in 24-hour format:
- ✅ Correct: "14:30" (2:30 PM)
- ✅ Correct: "09:15" (9:15 AM)
- ❌ Wrong: "2:30 PM"
- ❌ Wrong: "9:15 AM"

### Step 8: Database Check

If you're comfortable with SQL, check the database directly:

```sql
SELECT id, task, priority, todo_date, due_time, completed 
FROM todos 
WHERE completed = 0 
AND todo_date = date('now', 'localtime')
AND priority IN (3, 4, 5);
```

### Example Scenarios

#### Scenario 1: Current time is 2:00 PM

✅ **Will show in reminders:**
- Priority 3, Due 2:30 PM (30 min away)
- Priority 4, Due 2:45 PM (45 min away)
- Priority 5, Due 3:00 PM (1 hour away)
- Priority 3, Due 1:30 PM (already passed)

❌ **Will NOT show:**
- Priority 1, Due 2:30 PM (wrong priority)
- Priority 3, Due 4:00 PM (too far in future)
- Priority 3, Due 2:30 PM, Completed (already done)
- Priority 3, Due 2:30 PM, Tomorrow (wrong date)

#### Scenario 2: Current time is 11:00 PM (23:00)

✅ **Will show in reminders:**
- Priority 3, Due 11:30 PM (23:30)
- Priority 4, Due 11:59 PM (23:59)
- Priority 5, Due 10:00 PM (already passed)

❌ **Will NOT show:**
- Priority 3, Due 12:30 AM (00:30) - This is tomorrow!

### Quick Fix Checklist

- [ ] Created todo with priority 3, 4, or 5
- [ ] Set due time within next hour
- [ ] Set date to today
- [ ] Todo is not completed (unchecked)
- [ ] Refreshed the page or waited 60 seconds
- [ ] Checked browser console for errors
- [ ] Checked server console for debug output

### Still Not Working?

If you've checked everything and it's still not working:

1. **Restart Flask server**: Stop and start `python app.py`
2. **Clear browser cache**: Ctrl+Shift+Delete
3. **Check time zone**: Make sure server and browser are in same timezone
4. **Check database**: Verify todos are actually saved

### Debug Output Interpretation

**Server Console:**
```
Total uncompleted todos today: 0
```
→ You have no uncompleted todos for today. Create some!

```
Total uncompleted todos today: 5
  - Priority 1, Due: 15:00, Task: ...
  - Priority 2, Due: 16:00, Task: ...
Filtered reminders (P3,4,5 due <= 15:30): 0
```
→ You have todos, but they're all priority 1 or 2. Create priority 3, 4, or 5 todos!

```
Total uncompleted todos today: 5
  - Priority 3, Due: 18:00, Task: ...
  - Priority 4, Due: 19:00, Task: ...
Filtered reminders (P3,4,5 due <= 15:30): 0
```
→ You have priority 3-5 todos, but they're due too far in the future. Create todos due within the next hour!

**Browser Console:**
```
Reminders received: []
Count: 0
```
→ API returned no reminders. Check server console to see why.

```
Error loading reminders: ...
```
→ Network error or API error. Check if Flask server is running.
