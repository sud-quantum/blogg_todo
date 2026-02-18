# User Profile Enhancement

## New Features Added ✅

### 1. Extended Registration Form
**New Required Fields**:
- Email (mandatory)
- Date of Birth (mandatory)
- Gender (mandatory)

**Optional Field**:
- Phone number

### 2. Enhanced Profile Card
**Displays**:
- Username
- Email
- Member since date
- Date of Birth
- Gender
- Phone (if provided)
- All statistics (tasks, streak, blogs, completion rate)

### 3. Edit Profile Functionality
**Can Edit**:
- Username
- Email
- Date of Birth
- Gender
- Phone
- Password (optional - leave blank to keep current)

## Database Changes

### New Columns Added to `users` Table
- `email` TEXT
- `dob` DATE
- `phone` TEXT
- `gender` TEXT

## Setup Instructions

### Step 1: Run Migration
Before starting the app, run the migration script:

```bash
python migrate_user_profile.py
```

This will add the new columns to your existing database.

### Step 2: Update Existing Users (If Any)
If you have existing users, they will need to:
1. Log out
2. Register again with the new fields
OR
You can manually update the database to add their information.

### Step 3: Start the App
```bash
python app.py
```

## Registration Form

### Layout
- Username (required)
- Email (required)
- Password (required)
- Date of Birth (required)
- Gender (required) - Dropdown with options:
  - Male
  - Female
  - Other
  - Prefer not to say
- Phone (optional)

### Validation
- Username must be unique
- Email must be unique
- Email must be valid format
- All required fields must be filled

## Profile Card

### Top Section
```
[User Icon]
Username
email@example.com
Member since YYYY-MM-DD

[Edit Profile Button]
```

### Personal Details Section
```
🎂 Date of Birth
   YYYY-MM-DD

⚥  Gender
   Male/Female/Other

📞 Phone
   +1 234 567 8900
```

### Statistics Section
```
📋 Total Tasks        [42]
✓  Completed          [35]
🔥 Current Streak     [7 days]
📝 Blog Posts         [12]
%  Completion Rate    [83.3%]
```

## Edit Profile Modal

### Features
- Modal popup for editing
- Pre-filled with current values
- Password field optional (leave blank to keep current)
- Validation before saving
- Success/error toast notifications
- Auto-reload after successful update

### Fields
1. Username (text input)
2. Email (email input)
3. Date of Birth (date picker)
4. Gender (dropdown)
5. Phone (tel input, optional)
6. New Password (password input, optional)

### Validation
- Username uniqueness check
- Email uniqueness check
- All required fields must be filled
- Shows error if username/email already taken

## API Endpoints

### POST /profile/edit
**Request Body**:
```json
{
  "username": "string",
  "email": "string",
  "dob": "YYYY-MM-DD",
  "gender": "string",
  "phone": "string",
  "password": "string" (optional)
}
```

**Response Success**:
```json
{
  "success": true,
  "message": "Profile updated successfully!"
}
```

**Response Error**:
```json
{
  "error": "Username already taken"
}
```

## Files Modified

1. **schema.sql** (reference only - use migration script)
   - Added new columns to users table

2. **migrate_user_profile.py** (NEW)
   - Migration script to add new columns

3. **templates/register.html**
   - Added email, dob, gender, phone fields
   - Updated layout to accommodate new fields
   - Added field validation

4. **templates/profile.html**
   - Enhanced user card with personal details
   - Added edit profile button
   - Added edit profile modal
   - Added JavaScript for modal and save functionality

5. **app.py**
   - Updated register route to handle new fields
   - Updated profile route to fetch user details
   - Added edit_profile route for updating user info

## Security Features

1. **Password Hashing**: Passwords are hashed using werkzeug
2. **Unique Constraints**: Username and email must be unique
3. **Session Management**: Only logged-in users can edit profile
4. **Validation**: Server-side validation for all fields
5. **Optional Password**: Can update profile without changing password

## User Experience

### Registration Flow
1. User fills registration form
2. All required fields validated
3. Account created
4. Redirected to login
5. Success message shown

### Profile Edit Flow
1. User clicks "Edit Profile" button
2. Modal opens with current values
3. User modifies fields
4. Clicks "Save changes"
5. Validation performed
6. Profile updated
7. Success toast shown
8. Page reloads with new data

## Testing Checklist

- [ ] Run migration script successfully
- [ ] Register new user with all fields
- [ ] Login with new user
- [ ] View profile card with all details
- [ ] Click "Edit Profile" button
- [ ] Modal opens with current values
- [ ] Edit username and save
- [ ] Edit email and save
- [ ] Edit DOB and save
- [ ] Edit gender and save
- [ ] Edit phone and save
- [ ] Change password and save
- [ ] Try duplicate username (should fail)
- [ ] Try duplicate email (should fail)
- [ ] Leave required field empty (should fail)
- [ ] Cancel edit (should close modal)

## Migration Notes

### For Existing Users
If you have existing users in the database:

**Option 1**: Manual Update
```sql
UPDATE users SET 
  email = 'user@example.com',
  dob = '1990-01-01',
  gender = 'Prefer not to say',
  phone = ''
WHERE id = 1;
```

**Option 2**: Have users re-register
- Backup existing data
- Drop users table
- Run schema.sql
- Users register again

## Future Enhancements (Optional)

1. Profile picture upload
2. Email verification
3. Phone verification
4. Two-factor authentication
5. Password strength meter
6. Password confirmation field
7. Account deletion option
8. Export user data
9. Privacy settings
10. Notification preferences
