#!/usr/bin/env python3
"""
Utility script to clear all Excel sheet data from the Tata Motors Performance Analytics system.
This script will:
1. Delete all records from the database tables
2. Remove all uploaded Excel files from the upload directory
"""

import os
import sys
import shutil

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import Config
from models.database import init_db, User, Test, Answer, Evaluation, Attendance, Feedback

def get_database_session():
    """Create and return a database session"""
    return init_db()

def clear_database_tables():
    """Clear all data from database tables"""
    print("Clearing database tables...")
    
    try:
        db_session = get_database_session()
        
        # Delete all records from tables in the correct order (due to foreign keys)
        # Delete child tables first, then parent tables
        db_session.query(Feedback).delete()
        db_session.query(Attendance).delete()
        db_session.query(Evaluation).delete()
        db_session.query(Answer).delete()
        db_session.query(Test).delete()
        # Note: We're not deleting User records as they might be needed for the system
        
        # Commit the changes
        db_session.commit()
        db_session.close()
        
        print("✓ Database tables cleared successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error clearing database tables: {str(e)}")
        return False

def clear_upload_directory():
    """Remove all files from the upload directory"""
    print("Clearing upload directory...")
    
    try:
        upload_folder = Config.UPLOAD_FOLDER
        
        # Check if upload folder exists
        if not os.path.exists(upload_folder):
            print("✓ Upload directory doesn't exist, nothing to clear")
            return True
            
        # Remove all files in the upload directory
        for filename in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"✗ Failed to delete {file_path}. Reason: {e}")
                
        print("✓ Upload directory cleared successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error clearing upload directory: {str(e)}")
        return False

def main():
    """Main function to clear all Excel sheet data"""
    print("Tata Motors Performance Analytics - Data Clear Utility")
    print("=" * 55)
    
    # Confirm with user before proceeding
    confirmation = input("This will delete ALL Excel sheet data and uploaded files. Are you sure? (type 'YES' to confirm): ")
    
    if confirmation != 'YES':
        print("Operation cancelled.")
        return
    
    print("\nStarting data deletion process...\n")
    
    # Clear database tables
    db_success = clear_database_tables()
    
    # Clear upload directory
    upload_success = clear_upload_directory()
    
    # Report results
    print("\n" + "=" * 55)
    if db_success and upload_success:
        print("✓ All Excel sheet data has been successfully deleted!")
        print("✓ Database records cleared")
        print("✓ Uploaded files removed")
    else:
        print("✗ Some errors occurred during the deletion process.")
        if not db_success:
            print("✗ Database clearing failed")
        if not upload_success:
            print("✗ Upload directory clearing failed")

if __name__ == "__main__":
    main()