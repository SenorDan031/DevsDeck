from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


myboard = Flask(__name__)
myboard.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myboard.db'


@myboard.route('/') 
def HOME() :
    return render_template('WELCOME.html')

if __name__ == '__main__':
    myboard.run(debug=True)