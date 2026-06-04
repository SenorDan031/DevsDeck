#IMPORTS
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for,session,flash
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
import os


#================================================================================================

#CONFIGS HERE

application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///application.db')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.secret_key = "supersecretkey"

db= SQLAlchemy(application)

#================================================================================================

#MODELS here
class User(db.Model) :
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    contact_no: Mapped[str] = mapped_column(String(16), unique=False, nullable=True)
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
        db.ForeignKey('users.id'),
        unique=True
    )

    background_color: Mapped[str] = mapped_column(
        String(50)
    )
    
    OS_name: Mapped[str] = mapped_column(
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
    
    background_type: Mapped[str] = mapped_column(
    String(20)
  )

    animations_enabled: Mapped[bool] = mapped_column(
    Boolean,
    default=True
    )
    
class DevWindow(db.Model):

    __tablename__ = 'dev_windows'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        db.ForeignKey('users.id')
    )

    folder_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    tab_link: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

#================================================================================================

with application.app_context():
    db.create_all()
    
#ROUTES here

@application.route('/') 
def HOME() :
    return render_template('WELCOME.html')


@application.route('/signup', methods=['GET','POST']) 
def SIGNUP() :
    errors = {}
    values = {}
    
    if request.method == 'POST':
        Uname  = request.form.get('username', '').strip()
        Ucon = request.form.get('contact_no', '').strip()
        Uemail = request.form.get('email', '').strip()
        Upass  = request.form.get('password', '').strip()
        
        values = {
            'User_name': Uname, 
            
            'User_email': Uemail, 
            
            'User_contact': Ucon
        }

        # validations
        if len(Uname) < 3:
            errors['username'] = "Username must be at least 3 characters"

        if '@' not in Uemail or '.' not in Uemail:
            errors['email'] = "Enter a valid email address"

        if len(Upass) < 6:
            errors['password'] = "Password must be at least 6 characters"
            
        if Ucon and len(Ucon) < 10:
            errors['contact_no'] = "Contact number must be at least 10 digits"

        if errors:
            return render_template('signup.html', errors=errors, values=values)

        hide = generate_password_hash(Upass)
        
        try :
            
            user_details= User(username=Uname, contact_no=Ucon, email=Uemail, password=hide)
            db.session.add(user_details)
            db.session.commit()

            flash(f"Congrats {user_details.username} 🎉, your account has been created successfully", "success")
            
            session['user_id']= user_details.id
            session['username']= user_details.username
            return redirect(url_for('BUILD_MY_OS'))
        
        except IntegrityError as e:

            db.session.rollback()

            error_message = str(e)

            if 'users.email' in error_message:

                errors['email'] = "Email already exists"

            elif 'users.username' in error_message:

                errors['username'] = "Username already exists"

            elif 'users.contact_no' in error_message:

                errors['contact_no'] = "Contact number already exists"

            else:

                errors['general'] = "Something went wrong"

            return render_template(
                'signup.html',
                errors=errors,
                values=values
            )
            
            
                
    return render_template('signup.html', errors=errors, values=values)

@application.route('/create_os', methods=['GET','POST'])
def BUILD_MY_OS() :
    
    if request.method == "POST" :
        background_color = request.form.get('background_color')
        OS_name = request.form.get('OS_name')
        wallpaper_url = request.form.get('wallpaper_url')
        font_size = request.form.get('font_size')
        primary_color = request.form.get('primary_color')
        background_type = request.form.get('background_type')
        animations_enabled = bool(request.form.get('animations_enabled'))
             
        user_id = session.get('user_id')
        
        deck_theme = DeckTheme(
            user_id=session['user_id'],
            background_color=background_color,
            OS_name=OS_name,
            wallpaper_url=wallpaper_url,
            font_size=int(font_size),
            primary_color=primary_color,
            background_type=background_type,
            animations_enabled=animations_enabled
        )
        
        db.session.add(deck_theme)
        db.session.commit()
        
        flash("Your OS has been created successfully!", "success")
        
        return render_template('Page.html')
        
    return render_template('create_os.html')
    

@application.route('/login', methods=['GET', 'POST'])

def LOGIN():

    errors = {}

    if request.method == 'POST':

        username = request.form.get('username')

        password = request.form.get('password')

        
        user = User.query.filter_by(
            username=username
        ).first()

        

        if user:

          

            if check_password_hash(
                user.password,
                password
            ):

                
                session['user_id'] = user.id

                session['username'] = user.username

                return render_template('Page.html')

            else:

                flash(
                    "Auth-Error: Admin not recognised",
                    "error"
                )

        else:

            flash(
                "Auth-Error: Admin not recognised",
                "error"
            )

    return render_template(
        'login.html',
        errors=errors
    )
            
            

            
            
            
            
#MAIN here
        
if __name__ == '__main__':
    application.run(debug=True)
    
#================================================================================================

