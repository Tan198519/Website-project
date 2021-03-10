language: python
python:
- "3.9.0"
install:

pip install -r requirements/dev.txt
pip install codecov

script:

python -m unittest discover
behave
coverage erase
coverage run test_webapp.py && coverage html
pylint --output-format=text webapp.py

after_success:

codecov

deploy:
app: flask-travis-ci


1.Introduction
1.1	Purpose
1.2	Project Scope and Product Features
2.Overall Description
2.1	Product Perspective
2.2	Operating Environment
3.Interface Requirements
3.1	Main
3.2	Departments
3.2.1	Department table
3.2.2	Form create department
3.3	Employees
3.3.1	Form create employee
3.3.2	Employees
3.4	About company
3.4.1 About company with diagram
Appendix A: BD(2 tables)
