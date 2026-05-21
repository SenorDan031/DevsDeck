#imports
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for,session,flash
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///application.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.secret_key = "supersecretkey"

db= SQLAlchemy(application)

class User(db.Model) :
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    contact_no: Mapped[str] = mapped_column(String(16), unique=True, nullable=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
    default=datetime.utcnow,
    onupdate=datetime.utcnow
)
class DeckTheme(db.Model):

    __tablename__ = 'deck_themes'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        db.ForeignKey('users.id')
    )

    background_color: Mapped[str] = mapped_column(
        String(50)
    )

    wallpaper_url: Mapped[str] = mapped_column(
        String(500)
    )

    font_size: Mapped[int] = mapped_column(
        Integer
    )

    primary_color: Mapped[str] = mapped_column(
        String(50)
    )

    animations_enabled: Mapped[bool]
    
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

@application.route('/') 
def HOME() :
    return render_template('WELCOME.html')


@application.route('/signup', methods=['GET','POST']) 
def SIGNUP() :
    errors = {}
    values = {}
    
    if request.method == 'POST':
        Uid  = request.form.get('id', '').strip()
        Uname  = request.form.get('username', '').strip()
        Ucon = request.form.get('contact_no', '').strip()
        Uemail = request.form.get('email', '').strip()
        Upass  = request.form.get('password', '').strip()
        
        values = {'User_name': Uname, 'User_email': Uemail}

        # validations
        if len(Uname) < 3:
            errors['name'] = "Username must be at least 3 characters"

        if '@' not in Uemail or '.' not in Uemail:
            errors['email'] = "Enter a valid email address"

        if len(Upass) < 6:
            errors['password'] = "Password must be at least 6 characters"
            
        if len(Ucon) < 6:
            errors['contact_no'] = "contact number must be at least of 10 digits (Excluding country code)"

        if errors:
            return render_template('signup.html', errors=errors, values=values)

        hide = generate_password_hash(Upass)
        
        try :
            
            user_details= User(username=Uname, contact_no=Ucon, email=Uemail, password=hide)
            db.session.add(user_details)
            db.session.commit()

            flash(f"Congrats {user_details.username} 🎉, your account has been created successfully", "success")
            return redirect('/select-role')
        
        except IntegrityError:
            db.session.rollback()
            errors['email'] = "Email or username already exists"
            return render_template('signup.html', errors=errors, values=values)
            
    return render_template('signup.html', errors=errors, values=values)
            
            
            
            
            
            
if __name__ == '__main__':
    application.run(debug=True)
