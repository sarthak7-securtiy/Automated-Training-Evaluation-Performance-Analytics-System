
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import Base, Test, Evaluation, Answer, Attendance, Feedback, User

# Database connection
DB_PATH = 'sqlite:///employee_performance_new.db'
engine = create_engine(DB_PATH)
Session = sessionmaker(bind=engine)
session = Session()

def clear_all_data():
    print("Clearing all data...")
    
    try:
        # Delete in order of dependencies (child first)
        deleted_evals = session.query(Evaluation).delete()
        deleted_answers = session.query(Answer).delete()
        deleted_feedback = session.query(Feedback).delete()
        deleted_attendance = session.query(Attendance).delete()
        deleted_tests = session.query(Test).delete()
        
        session.commit()
        print(f"Cleared {deleted_evals} evaluations")
        print(f"Cleared {deleted_answers} answers")
        print(f"Cleared {deleted_feedback} feedback entries")
        print(f"Cleared {deleted_attendance} attendance records")
        print(f"Cleared {deleted_tests} tests")
        print("All sample data cleared successfully!")
        
    except Exception as e:
        session.rollback()
        print(f"Error clearing data: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    clear_all_data()
