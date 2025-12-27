from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import Config

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    role = Column(String(50), nullable=False)  # Admin, Trainer, HR, Employee
    department = Column(String(100))
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with tests
    tests = relationship("Test", back_populates="user")

class Test(Base):
    __tablename__ = 'tests'
    
    test_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    test_type = Column(String(20), nullable=False)  # Pre-Test, Post-Test, Sectional
    training_name = Column(String(100))
    faculty_name = Column(String(100))  # Faculty/Trainer name
    date_uploaded = Column(DateTime, default=datetime.utcnow)
    date_conducted = Column(DateTime)
    file_path = Column(String(255))
    status = Column(String(20), default='uploaded')  # uploaded, processing, completed
    batch_ticket_no = Column(String(100))  # For tracking batches of related tests    
    # Relationships
    user = relationship("User", back_populates="tests")
    answers = relationship("Answer", back_populates="test")
    evaluations = relationship("Evaluation", back_populates="test")

class Answer(Base):
    __tablename__ = 'answers'
    
    answer_id = Column(Integer, primary_key=True)
    candidate_id = Column(String(50), nullable=False)
    candidate_name = Column(String(100))
    test_id = Column(Integer, ForeignKey('tests.test_id'), nullable=False)
    question_number = Column(Integer, nullable=False)
    selected_option = Column(String(10))
    is_correct = Column(Boolean, default=False)
    score = Column(Float, default=0.0)
    
    # Relationship
    test = relationship("Test", back_populates="answers")

class Evaluation(Base):
    __tablename__ = 'evaluations'
    
    evaluation_id = Column(Integer, primary_key=True)
    test_id = Column(Integer, ForeignKey('tests.test_id'), nullable=False)
    candidate_id = Column(String(50), nullable=False)
    total_score = Column(Float, default=0.0)
    percentage = Column(Float, default=0.0)
    status = Column(String(20))  # pass, fail
    evaluated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    test = relationship("Test", back_populates="evaluations")

class Attendance(Base):
    __tablename__ = 'attendance'
    
    attendance_id = Column(Integer, primary_key=True)
    employee_id = Column(String(50), nullable=False)
    punch_in = Column(DateTime)
    punch_out = Column(DateTime)
    date = Column(DateTime, default=datetime.utcnow)

class Feedback(Base):
    __tablename__ = 'feedback'
    
    feedback_id = Column(Integer, primary_key=True)
    trainer_id = Column(Integer, ForeignKey('users.user_id'))
    employee_id = Column(String(50), nullable=False)
    rating = Column(Integer)  # 1-5 scale
    comments = Column(String(500))
    submitted_at = Column(DateTime, default=datetime.utcnow)

# Create the database
def init_db():
    # Use the database URI from config
    engine_uri = Config.DATABASE_URI
    
    engine = create_engine(engine_uri)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    return Session()

# Initialize the database
if __name__ == "__main__":
    session = init_db()
    print("Database initialized successfully!")