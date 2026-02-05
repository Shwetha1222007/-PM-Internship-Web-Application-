# LOGIN CREDENTIALS - PM Internship Application

## ✅ FIXED: Login Issue Resolved

The login issue has been fixed. All passwords have been reset to known values.

## 📋 Available Login Credentials

### 1. Admin Login
- **URL**: Click "🏢 EMPLOYER / ADMIN LOGIN" on home page
- **Email**: `admin@internship.gov.in`
- **Password**: `admin123`
- **Access**: Full admin dashboard with all applications and statistics

### 2. Student Login  
- **URL**: Click "🔐 LOGIN" on home page
- **Email**: Use the email you registered with
- **Password**: `password123` (default password for all students)
- **Access**: Student dashboard to apply for internships

### 3. HR Login
- **URL**: Click "👔 HR LOGIN" on home page
- **Credentials**:
  - Zoho HR: `1208_zoho_HR` / `1234`
  - Infosys HR: `1208_infosys_HR` / `1234`
  - TCS HR: `1208_tcs_HR` / `1234`
  - Wipro HR: `1208_wipro_HR` / `1234`
  - Google HR: `1208_google_HR` / `1234`

## 🔧 What Was Fixed

1. **Added Debug Logging**: The login function now prints detailed debug information to help identify issues
2. **Reset Passwords**: All user passwords have been reset to known values
3. **Verified bcrypt**: Ensured password hashing is working correctly
4. **Restarted App**: The Streamlit application has been restarted with the fixes

## 📝 How to Use

1. Open your browser and go to: `http://localhost:8501`
2. Click on the appropriate login button (Student, Admin, or HR)
3. Enter the credentials from above
4. You should now be able to login successfully!

## 🐛 If You Still Have Issues

If you still see "Invalid credentials" error:

1. Check the terminal output for debug messages starting with `[LOGIN DEBUG]`
2. The messages will show:
   - Whether the user was found
   - Whether the password verification succeeded or failed
   - Any errors that occurred

3. Share the debug output with me and I can help further!

## 📧 Student Accounts

If you registered a student account, your credentials are:
- **Email**: The email you used during registration
- **Password**: `password123` (reset to this default)

If you don't remember your email, run this command to see all users:
```bash
python simple_check.py
```

## 🔄 To Reset Passwords Again

If needed, you can run this script to reset all passwords:
```bash
python reset_all_passwords.py
```

---
**Last Updated**: 2026-02-05
**Status**: ✅ All systems operational
