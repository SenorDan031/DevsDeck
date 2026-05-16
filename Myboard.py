from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


myboard = Flask(__name__)

myboard.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myboard.db'
myboard.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
myboard.secret_key = "supersecretkey"

db= SQLAlchemy(myboard)

class User(db.Model) :
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    contact_no: Mapped[str] = mapped_column(String(15), unique=True, nullable=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
class DevWindow(db.Model):

    __tablename__ = 'dev_windows'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        db.ForeignKey('users.id')
    )

    window_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    window_link: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

@myboard.route('/') 
def HOME() :
    return render_template('WELCOME.html')

if __name__ == '__main__':
    myboard.run(debug=True)