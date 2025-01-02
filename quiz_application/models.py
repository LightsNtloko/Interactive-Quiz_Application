from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Model to store user information
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Model for the Quiz to store quiz information
class Quiz(db.Model):
    __tablename__ = 'quizzes'
    quiz_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(100), nullable=False)
    question_data = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Model for QuickResults to store results for each user
class QuizResult(db.Model):
    __tablename__ = 'quiz_results'
    result_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    quiz_id = db.Column(UUID(as_uuid=True), db.ForeignKey('quizzes.quiz_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

# Define the relationships
User.quiz_results = db.relationship('QuizResult', backref='user', lazy=True)
Quiz.quiz_results = db.relationship('QuizResult', backref='quiz', lazy=True)
