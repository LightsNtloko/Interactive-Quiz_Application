from app import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
import uuid

# User model
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Quiz model
class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(150), nullable=False)
    questions = db.Column(db.JSON, nullable=False)  # Store questions as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# QuizResult model
class QuizResult(db.Model):
    __tablename__ = 'quiz_results'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(UUID(as_uuid=True), db.ForeignKey('quizzes.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
