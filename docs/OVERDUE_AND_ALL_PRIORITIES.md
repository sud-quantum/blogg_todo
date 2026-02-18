# Overdue Badge & All Priorities in Notifications

## Changes Made ✅

### 1. Overdue Badge Added
**Where**: Todo list and notification dropdown
**Appearance**: Red badge with clock icon and "OVERDUE" text
**Logic**: Shows when current time has passed the due time (only for today's date)

### 2. All Priorities in Notifications
**Before**: Only showed todos due within 1 hour
**After**: Shows ALL uncompleted todos for today (all priorities, all times)

## Features

### Overdue Detection

#### In Todo List
- Shows red "OVERDUE" badge next to priority tag
- Only appears for today's todos
- Only shows for uncompleted todos
- Updates when you view the page

#### In Notification Dropdown
- Shows red "OVERDUE" badge below the due time
- Appears for any todo past its due time
- Updates every 60 seconds automatically

### Notification System

#### What Shows in Notifications
- **All uncompleted todos for TODAY**
- **All priorities (1-5)**
- **All times** (not just within 1 hour)
- Up to 20 todos maximum

#### Visual Layout
```
Priority Tag | Task Name
Due: HH:MM   [OVERDUE badge if applicable]
```

## Examples

### Scenario 1: Current time is 2:30 PM

**Todo 1:**
- Priority: 1
- Due: 2:00 PM
- Status: ✅ Shows with OVERDUE badge

**Todo 2:**
- Priority: 4
- Due: 5:00 PM
- Status: ✅ Shows (no overdue badge)

**Todo 3:**
- Priority: 5
- Due: 1:00 PM
- Status: ✅ Shows with OVERDUE badge

**Todo 4:**
- Priority: 3
- Due: 2:00 PM
- Completed: ❌ Does NOT show (completed)

### Scenario 2: Viewing Yesterday's Todos

**Todo:**
- Date: Yesterday
- Due: 2:00 PM
- Current time: 3:00 PM
- Status: ❌ No OVERDUE badge (not today)

## Visual Design

### Overdue Badge in Todo List
```html
<span class="tag is-danger">
    <i class="fas fa-clock"></i>
    OVERDUE
</span>
```
- Red background
- White text
- Clock icon
- Appears after priority tag

### Overdue Badge in Notifications
```html
<span class="tag is-danger is-small ml-1">
    OVERDUE
</span>
```
- Small red badge
- Appears below due time
- Compact design for dropdown

## Technical Details

### Backend Changes (app.py)

1. **Reminder API** (`/api/reminders`):
   - Removed 1-hour time filter
   - Shows all uncompleted todos for today
   - Added `is_overdue` flag to response
   - Increased limit from 10 to 20 todos

2. **Todo Route** (`/todo`):
   - Added `current_time` to template context
   - Added `is_today` flag to template context
   - Used for overdue detection in template

### Frontend Changes

1. **templates/base.html**:
   - Updated `loadReminders()` function
   - Added overdue badge rendering
   - Changed title to "Today's Tasks"
   - Improved layout with two-line display

2. **templates/todo.html**:
   - Added overdue badge check
   - Only shows for today's date
   - Only shows for uncompleted todos
   - Positioned after priority tag

## Benefits

1. **Better Visibility**: See all tasks for today, not just upcoming ones
2. **Clear Status**: Overdue tasks are immediately visible
3. **All Priorities**: Priority 4 and 5 tasks now show in notifications
4. **No Time Limit**: Don't miss tasks due later in the day
5. **Automatic Updates**: Overdue status updates automatically

## Testing

### Test Overdue Badge

1. **Create a todo:**
   - Date: Today
   - Due time: 10 minutes ago
   - Priority: Any

2. **Check todo list:**
   - Should see red "OVERDUE" badge

3. **Check notification:**
   - Hover over bell icon
   - Should see "OVERDUE" badge below due time

### Test All Priorities

1. **Create 5 todos for today:**
   - Priority 1, Due: 9:00 AM
   - Priority 2, Due: 10:00 AM
   - Priority 3, Due: 11:00 AM
   - Priority 4, Due: 12:00 PM
   - Priority 5, Due: 1:00 PM

2. **Check notification:**
   - Should see all 5 todos
   - Each with correct priority color
   - Overdue badges where applicable

## Debug Output

**Server Console:**
```
=== REMINDER DEBUG ===
Current time: 14:30
Today: 2026-02-18
Total uncompleted todos today: 5
  - Priority 1, Due: 09:00, Task: Morning task
  - Priority 2, Due: 10:00, Task: Mid-morning task
  - Priority 3, Due: 14:00, Task: Afternoon task
  - Priority 4, Due: 16:00, Task: Evening task
  - Priority 5, Due: 20:00, Task: Night task
Total reminders (all uncompleted today): 5
```

**Browser Console:**
```
=== FRONTEND REMINDER DEBUG ===
Current time: 2:30:45 PM
Reminders received: Array(5)
Count: 5
```

## Files Modified

1. **app.py**
   - `/api/reminders`: Removed time filter, added is_overdue
   - `/todo`: Added current_time and is_today to context

2. **templates/base.html**
   - Updated loadReminders() function
   - Added overdue badge rendering

3. **templates/todo.html**
   - Added overdue badge in todo list
   - Only shows for today's uncompleted todos

## Backward Compatibility

- Fully backward compatible
- No database changes needed
- Existing todos work immediately
- No user action required
