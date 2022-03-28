from distutils.command.upload import upload
from multiprocessing import context
from sqlite3 import Cursor
from tkinter.tix import Form
from unittest import result
from urllib import response
from management import app
from flask import Response, make_response, render_template, redirect, url_for, flash,render_template_string
from management.models import Cosignmentdetails, User1
from management.forms import RegisterForm, LoginForm, SimpleForm
from management import db
from flask_login import login_user, logout_user, login_required
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flaskext.mysql import MySQL
import pdfkit
import pymysql
import io
import xlwt
import pandas as pd
from fpdf import FPDF

mysql = MySQL()

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/track')
@login_required
def track_page():
    consignments = Cosignmentdetails.query.all()
    return render_template('track.html', consignments=consignments)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User1(username=form.username.data,
                              email_address=form.email_address.data,
                              shipping_address=form.shipping_address.data,
                              mobile_number=form.mobile_number.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('track_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User1.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('track_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))


@app.route('/consignment', methods=['GET','POST'])
def consignment_page():
    form = SimpleForm()
    if form.validate_on_submit():
        consignment_to_create = Cosignmentdetails(
            consignment_type=form.consignment_type.data,
                              receiver_name=form.receiver_name.data,
                              receiver_address=form.receiver_address.data,
                              receiver_mobile=form.receiver_mobile.data,
                             # pickup_type=form.option1.data,
                              )
        db.session.add(consignment_to_create)
        db.session.commit()
        flash(f"{consignment_to_create.consignment_type} Consignment added successfully!!", category='success')
        return redirect(url_for('track_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with adding a consignment: {err_msg}', category='danger')

    return render_template('consignment.html', form=form)
@app.route('/pickup')
#@login_required
def pickup_page():
    consignments = Cosignmentdetails.query.all()
    return render_template('pickup.html', consignments=consignments)
@app.route('/download')
def download_report():
    consignments = Cosignmentdetails.query.all()
    html_string=consignments
  
    pdf=pdfkit.from_url('http://127.0.0.1:5000/pickup')
    response=make_response(pdf)
    response.headers["Content-Type"]="report/pdf"
    response.headers["content-Disposition"]="inline; filename=details.pdf"
    return response
#    conn = None
#    cursor=None
#	conn=mysql.connector.connect(host="sqlite:///database.db")
#	cursor = conn.cursor(pymysql.cursors.DictCursor)	
#	cursor.execute("SELECT consignment_type, receiver_name, receiver_address, receiver_mobile FROM Consignmentdetails")
#	result = cursor.fetchall()		
#	pdf = FPDF()
#	pdf.add_page()	
#	page_width = pdf.w - 2 * pdf.l_margin		
#	pdf.set_font('Times','B',14.0) 
#	pdf.ln(10)
#	pdf.set_font('Courier', '', 12)		
#	col_width = page_width/4
#	pdf.ln(1)		
#	th = pdf.font_size		
#	for row in result:
#		pdf.cell(col_width, th, str(row['consignment_type']), border=1)
#		pdf.cell(col_width, th, row['receiver_name'], border=1)
#		pdf.cell(col_width, th, row['receiver_address'], border=1)
#		pdf.cell(col_width, th, row['receiver_'], border=1)
#		pdf.ln(th)	
#	pdf.ln(10)	
#	pdf.set_font('Times','',10.0) 
#	pdf.cell(page_width, 0.0, '- end of report -', align='C')	
#	return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=employee_report.pdf'})
