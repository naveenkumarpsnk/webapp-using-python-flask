from ast import Num
from distutils.text_file import TextFile
from email.headerregistry import Address
from tkinter.tix import INTEGER
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import * 
from management.models import User1, Cosignmentdetails
from sqlalchemy import *
from sqlalchemy.orm import *
from snowflake.sqlalchemy import URL


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User1.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User1.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    shipping_address = StringField(label='Shipping Address:', validators=[DataRequired()])
    mobile_number = TelField(label='Mobile Number:',validators=[Length(min=10,max=10), DataRequired()])
        
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')
class SimpleForm(FlaskForm):
    
    def validate_username(self, consignment_data_to_check):
        cd = Cosignmentdetails.query.filter_by(consignment_data=consignment_data_to_check.data).first()
        if cd:
            raise ValidationError('Type already exists! Please try a different type')

    consignment_type = StringField(label='Consignment Type:', validators=[Length(min=2, max=30), DataRequired()])
    receiver_name = StringField(label='Receiver Name:', validators=[DataRequired()])
    receiver_address = StringField(label='Receiver Address:', validators=[DataRequired()])
    receiver_mobile = TelField(label='Receiver Mobile:',validators=[Length(min=10,max=10), DataRequired()])
    submit = SubmitField(label='Add Consignment')