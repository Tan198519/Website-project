# import libraries
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, g, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy.orm import joinedload, backref, session
from sqlalchemy import ForeignKey, Column, DateTime, String, Integer, select, join, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# from app import models


Model = declarative_base()

# create an object app, class Flask with directory
app = Flask(__name__)

# referring to the dictionary config, use database sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company.db'
# error disappeared
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# create an object based on class SQLAlchemy and pass an object in the constructor class flask
db = SQLAlchemy(app)

migrate = Migrate(app, db)


# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

# create 1 table - department

# BD - Table1 Department - Records
# Table:
# id    title   text    date
# 1     some    some    1111
# 2     some    some    2222
# 3     some    some    3333

# create class Department with an object db.Model and fields
class Department(db.Model):
    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # without empty title
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.relationship('Employee', backref=backref('department', uselist=False))

    def __repr__(self):  # method repr
        return f" {self.title}"
        # return '<Department %r>' % self.title


# BD - Table2 Employee - Records
# Table:
# id    name   fullname  date of birth   amount   id_department
# 1     some    some        1111          100          1
# 2     some    some        2222          200          2
# 3     some    some        3333          300          3

# create class Employee with an object db.Model and fields
class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(100), nullable=False)  # without empty title
    fullname = db.Column(db.VARCHAR(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date_birth = db.Column(db.Date, nullable=False)
    dep_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    dep = db.relationship('Department', backref=backref('employees', uselist=False))

    def __repr__(self):  # method repr
        return f" {self.amount}"

        # return '<Employee %r>' % self.amount


# create database-company.db(python3,from app import db, db.create_all(),exit())
# with 2 tables Department,Employee


# track url-address, direct page transition
# create decorators - use app and function route
# main page tracking and etc.


# @app.before_request
# def init_db():
#     g.db = sqlite3.connect("company.db")
#
#
# @app.after_request
# def close_db(r):
#     g.db.close()
#     return r


@app.route('/')
@app.route('/home')
# create function main page
def index():
    return render_template("index.html")


@app.route('/about')
# create function about page
def about():
    return render_template("about.html")


@app.route('/departments')
# create function departments page
def departments():
    articles = Department.query.order_by(Department.id.asc()).all()

    # articles1 = select((func.avg(Employee.amount))).select_from(articles)
    # articles = (select(func.avg(Employee.amount)).join(Department).
    #              filter(Employee.dep_id == Department.id))
    return render_template("departments.html", articles=articles)


# @app.route('/departments')
# # create function departments page
# def departments():
#     cursor = g.db.execute("select d.id, d.title, d.text, d.date, AVG(e.amount)amount "
#                           "from department d join employee e on e.dep_id=d.id group by d.id, d.title, d.text, date")
#     articles = cursor.fetchall()
#     articles = [{"id": id_, "title": title, "text": text, "date": date, "amount": amount}
#                 for id_, title, text, date, amount in articles]
#     return render_template("departments.html", articles=articles)
#     #return jsonify(articles)


@app.route('/employees')
# create function employees page
def employees():
    articles = Employee.query.order_by(Employee.id.asc()).all()
    return render_template("employees.html", articles=articles)


@app.route("/departments/<int:id_>/del")
# create function department_delete
def department_delete(id_):
    articles = Department.query.get_or_404(id_)

    try:
        db.session.delete(articles)
        db.session.commit()
        return redirect('/departments')
    except:
        return "On error occurred while delete an department"


@app.route('/departments/<int:id_>/update', methods=['POST', 'GET'])
# create function department_update
def department_update(id_):
    articles = Department.query.get(id_)
    if request.method == 'POST':
        articles.title = request.form['title']
        articles.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/departments')
        except:
            return "On error occurred while adding an department"
    else:
        return render_template("department_update.html", articles=articles)


@app.route('/department', methods=['POST', 'GET'])
# create function department
def department():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']

        articles = Department(title=title, text=text)  # create an object articles

        try:
            db.session.add(articles)  # add an object
            db.session.commit()  # save an object
            return redirect('/departments')
        except:
            db.session.rollback()
            return "On error occurred while adding an department"
    else:
        return render_template("department.html")


@app.route('/employee', methods=['POST', 'GET'])
# create function employee
def employee():
    if request.method == "POST":
        name = request.form.get('name')
        fullname = request.form.get('fullname')
        date_birth = request.form.get('date_birth')
        amount = request.form.get('amount')
        # title = request.form['title']
        # dep_id = request.form['dep_id']
        # dep = request.form['dep']

        # create an object articles
        articles = Employee(name=name, fullname=fullname, date_birth=date_birth, amount=amount)
        try:
            db.session.add(articles)  # add an object
            db.session.commit()  # save an object
            return redirect('/employees')
        except:
            db.session.rollback()
            return "On error occurred while adding an employee"
    else:
        return render_template("employee.html")


@app.route('/employee1', methods=['POST', 'GET'])
# create function dropdown(list departments)
def employee1():
    articles = Department.query.order_by(Department.id.asc()).all()
    if request.method == "POST":
        try:
            db.session.add(articles)  # add an object
            db.session.commit()  # save an object
            return redirect('/employee1')
        except:
            db.session.rollback()
            return "On error occurred while adding an employee"
    else:
        return render_template("employee1.html", articles=articles)


# create and add format date in table employees
def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)


app.add_template_filter(datetimeformat)


@app.route("/employees/<int:id_>/del")
# create function employee_delete
def employee_delete(id_):
    articles1 = Employee.query.get_or_404(id_)

    try:
        db.session.delete(articles1)
        db.session.commit()
        return redirect('/employees')
    except:
        return "On error occurred while delete an employee"


@app.route('/employees/<int:id_>/update', methods=['POST', 'GET'])
# create function employee_update
def employee_update(id_):
    articles1 = Employee.query.get(id_)

    if request.method == 'POST':
        articles1.name = request.form.get('name')
        articles1.fullname = request.form.get('fullname')
        articles1.date_birth = request.form.get('date_birth')
        articles1.amount = request.form.get('amount')
        articles1.dep_id = request.form.get('dep_id')
        articles1.dep = request.form.get('dep')

        try:
            db.session.commit()
            return redirect('/employees')
        except:
            return "On error occurred while adding an employee"
    else:
        return render_template("employee_update.html", articles1=articles1)


# main file, start the local server, show the error

if __name__ == "__main__":
    app.run(debug=True)
    # manager.run()

# sample results:

# articles1 = db.session.query(Department).filter(Department.title) \
#     .order_by(Department.id).all()
#
# results = db.session.query(Employee, Department).join(Department).all()
# for employee, department in results:
#     print(employee.id, employee.name, department.title)
#
# results = db.session.query(Department.title, Employee.amount).join(Department). \
#     filter(Department.id).all()
# for result in results:
#     print(result)
# query = Department.query.options(joinedload('employees'))
# for department in query:
#     print(department.id, department.employees.amount)
