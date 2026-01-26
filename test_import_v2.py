import sys
import os

print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")

try:
    import email_service
    print("email_service module imported successfully")
    from email_service import send_hr_announcement, send_update_to_candidate, send_candidate_confirmation
    print("Functions imported successfully")
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()
