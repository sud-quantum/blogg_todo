# ✅ Testing Checklist

## Pre-Testing Setup

- [ ] Run `python migrate_db.py`
- [ ] Start app with `python app.py`
- [ ] Open http://localhost:5000
- [ ] Register a new account
- [ ] Login successfully

---

## 🏠 Dashboard Tests

### Statistics Display
- [ ] Total todos count shows
- [ ] Completed todos count shows
- [ ] Today's tasks count shows
- [ ] Total blogs count shows
- [ ] Completion rate percentage displays
- [ ] Progress bar shows correct percentage

### Activity Calendar
- [ ] 90-day calendar grid displays
- [ ] Hover shows date and count
- [ ] Color intensity varies with activity
- [ ] Legend shows (Less to More)

### Streak Counter
- [ ] Streak number displays
- [ ] Shows "Days in a row"
- [ ] Fire emoji visible

### Priority Breakdown
- [ ] 5 circular progress indicators show
- [ ] Each shows count of tasks
- [ ] Colors match priority levels
- [ ] Labels show "Priority 1-5"

### Quick Actions
- [ ] "My Todos" card clickable
- [ ] "My Blog" card clickable
- [ ] Hover effect works
- [ ] Navigation works

---

## 👤 Profile Tests

### User Info
- [ ] Username displays
- [ ] User icon shows
- [ ] Progress stats visible

### Category Management
- [ ] Add category form visible
- [ ] Name input works
- [ ] Color picker works
- [ ] "Add" button functional
- [ ] New category appears in list
- [ ] Category shows with color dot
- [ ] Delete button works
- [ ] Confirmation dialog appears
- [ ] Category removed from list
- [ ] Duplicate category shows error

### Progress Tracking
- [ ] Overall completion rate shows
- [ ] Total tasks count displays
- [ ] Completed tasks count displays
- [ ] Total blogs count displays

---

## 📋 Todo Tests

### Header & Navigation
- [ ] "My Todos" title shows
- [ ] Date picker displays current date
- [ ] Calendar icon button works
- [ ] Date picker opens on click

### Search & Filter Bar
- [ ] Search input visible
- [ ] Category dropdown shows categories
- [ ] "All Categories" option present
- [ ] Filter button works
- [ ] Search by keyword works
- [ ] Filter by category works
- [ ] Combined search + filter works
- [ ] Enter key triggers search

### Add Todo Form
- [ ] Task input field works
- [ ] Priority radio buttons (1-5) display
- [ ] Priority 3 selected by default
- [ ] Priority labels show colors
- [ ] Category dropdown shows categories
- [ ] "No Category" option present
- [ ] Due time input shows (default 23:59)
- [ ] Recurring dropdown shows options
- [ ] One-time, Daily, Weekly, Monthly options
- [ ] Selected date displays
- [ ] "Add Todo" button works
- [ ] Form submits successfully
- [ ] Toast notification appears
- [ ] New todo appears in list

### Past Date Restriction
- [ ] Select past date
- [ ] Form inputs disabled
- [ ] Warning message shows
- [ ] Cannot add todo to past date

### Current Todos Display
- [ ] Section title shows
- [ ] Todos list displays
- [ ] Checkbox unchecked
- [ ] Task text visible
- [ ] Priority tag shows with color
- [ ] Category tag shows (if assigned)
- [ ] Recurring icon shows (if recurring)
- [ ] Due time displays
- [ ] Added timestamp shows
- [ ] Comments button visible
- [ ] Delete button visible

### Todo Actions
- [ ] Check checkbox marks complete
- [ ] Todo moves to finished section
- [ ] Comments button opens textarea
- [ ] Can type in comments
- [ ] Save button works
- [ ] Toast shows "Comment saved"
- [ ] Clear button works
- [ ] Confirmation dialog appears
- [ ] Toast shows "Comment cleared"
- [ ] Delete button works
- [ ] Todo removed from list

### Finished Todos Display
- [ ] Section title shows
- [ ] Completed todos display
- [ ] Checkbox checked
- [ ] Task text crossed out
- [ ] Opacity reduced
- [ ] Priority tag shows
- [ ] Category tag shows
- [ ] Recurring icon shows
- [ ] Added timestamp shows
- [ ] Finished timestamp shows
- [ ] Comments display (read-only)
- [ ] Delete button works
- [ ] Uncheck moves back to current

### Recurring Todos
- [ ] Create daily recurring todo
- [ ] Mark as complete
- [ ] New todo created for tomorrow
- [ ] Create weekly recurring todo
- [ ] Mark as complete
- [ ] New todo created for next week
- [ ] Create monthly recurring todo
- [ ] Mark as complete
- [ ] New todo created for next month

---

## 📝 Blog Tests

### Header & Navigation
- [ ] "My Blog" title shows
- [ ] Date picker displays
- [ ] Calendar icon works

### Add Blog Form
- [ ] Title input visible
- [ ] Content editor visible
- [ ] Toolbar buttons display
- [ ] Bold button works
- [ ] H1, H2, H3 buttons work
- [ ] Color highlight buttons work
- [ ] Clear format button works
- [ ] Can type in editor
- [ ] Scrollbar appears when overflow
- [ ] "Publish Blog" button works
- [ ] Form submits successfully
- [ ] Toast notification appears

### Blog List Display
- [ ] Blogs display for selected date
- [ ] Title shows
- [ ] Created timestamp shows
- [ ] Updated timestamp shows (if edited)
- [ ] Preview button visible
- [ ] Edit button visible
- [ ] Delete button visible

### Blog Actions
- [ ] Preview button opens modal
- [ ] Modal shows title
- [ ] Modal shows content
- [ ] Content formatted correctly
- [ ] Close button works
- [ ] Click outside closes modal
- [ ] Background scroll disabled
- [ ] Edit button loads blog
- [ ] Form title changes to "Edit"
- [ ] Title pre-filled
- [ ] Content pre-filled
- [ ] Update button shows
- [ ] Cancel button shows
- [ ] Update works
- [ ] Cancel resets form
- [ ] Delete button works
- [ ] Confirmation dialog appears
- [ ] Blog removed

### Date Navigation
- [ ] Change date in picker
- [ ] Blogs filter by date
- [ ] Empty state shows for no blogs
- [ ] Can view past dates
- [ ] Can view future dates

---

## 🔔 Reminder Tests

### Notification Icon
- [ ] Bell icon visible in header
- [ ] Badge shows count (if reminders)
- [ ] Badge hidden (if no reminders)
- [ ] Hover shows dropdown
- [ ] Dropdown shows reminders
- [ ] Each reminder shows:
  - [ ] Priority tag
  - [ ] Task name (truncated)
  - [ ] Due time
- [ ] Click reminder navigates to date
- [ ] "No reminders" shows when empty
- [ ] Updates every minute

---

## 🌙 Theme Tests

### Theme Switcher
- [ ] Sun/moon icons visible
- [ ] Toggle switch visible
- [ ] Click toggles theme
- [ ] Dark theme applies
- [ ] Light theme applies
- [ ] Preference saved
- [ ] Refresh maintains theme

### Dark Mode Visibility
- [ ] All text clearly visible
- [ ] Navbar text readable
- [ ] Card text readable
- [ ] Input fields visible
- [ ] Buttons readable
- [ ] Tags and badges visible
- [ ] Calendar readable
- [ ] Dashboard charts visible
- [ ] No contrast issues

### Light Mode Visibility
- [ ] All text clearly visible
- [ ] Good contrast throughout
- [ ] No readability issues

---

## 🔐 Authentication Tests

### Registration
- [ ] Form displays
- [ ] Username required
- [ ] Password required
- [ ] Duplicate username rejected
- [ ] Success message shows
- [ ] Redirects to login

### Login
- [ ] Form displays
- [ ] Username required
- [ ] Password required
- [ ] Wrong username rejected
- [ ] Wrong password rejected
- [ ] Success redirects to dashboard
- [ ] Session maintained

### Logout
- [ ] Logout link in dropdown
- [ ] Click logs out
- [ ] Redirects to login
- [ ] Session cleared
- [ ] Cannot access protected pages

### Navigation
- [ ] Logged out: only login/register accessible
- [ ] Logged in: all pages accessible
- [ ] Profile link in dropdown
- [ ] Logout link in dropdown

---

## 📱 Responsive Tests

### Desktop (1920x1080)
- [ ] Layout optimal
- [ ] All features accessible
- [ ] No overflow issues

### Tablet (768x1024)
- [ ] Columns stack appropriately
- [ ] Touch targets adequate
- [ ] Navigation works

### Mobile (375x667)
- [ ] Single column layout
- [ ] Burger menu works
- [ ] Forms usable
- [ ] Buttons accessible

---

## 🎨 UI/UX Tests

### Animations
- [ ] Toast slides in/out
- [ ] Cards hover effect
- [ ] Buttons hover effect
- [ ] Smooth transitions

### Feedback
- [ ] Success toasts show
- [ ] Error toasts show
- [ ] Loading states clear
- [ ] Confirmation dialogs work

### Accessibility
- [ ] Tab navigation works
- [ ] Enter key submits forms
- [ ] Focus indicators visible
- [ ] Color contrast adequate

---

## 🐛 Edge Cases

### Empty States
- [ ] No todos message shows
- [ ] No blogs message shows
- [ ] No categories message shows
- [ ] No reminders message shows

### Data Limits
- [ ] Long task names truncate
- [ ] Long blog content scrolls
- [ ] Many categories display well
- [ ] Many todos paginate/scroll

### Date Handling
- [ ] Past dates work
- [ ] Future dates work
- [ ] Today works
- [ ] Date changes at midnight

### Error Handling
- [ ] Network errors show message
- [ ] Invalid data rejected
- [ ] Database errors handled
- [ ] Form validation works

---

## ✅ Final Checks

- [ ] All features working
- [ ] No console errors
- [ ] No visual glitches
- [ ] Performance acceptable
- [ ] Data persists correctly
- [ ] Ready for use!

---

## 📊 Test Results

**Date Tested**: ___________
**Tester**: ___________
**Pass Rate**: _____ / _____
**Issues Found**: ___________
**Status**: ⬜ Pass ⬜ Fail ⬜ Needs Work

---

## 🎉 Congratulations!

If all tests pass, your enhanced Blog & Todo website is fully functional and ready to boost your productivity!
