import sqlite3
from flask import Flask, request, session, g, redirect, url_for, render_template, flash
from functools import wraps
import os



SECRET_KEY = 'T44\xadhs_\xaf\xb0\xf0w\xed\xa1\xed\xa1\xd5\x00$\x07\xfcD\x0c \x1a'
app = Flask(__name__)
app.secret_key = 'SECRET_KEY'


DATABASE = 'C:\\users\\bowenl2\\IS211_Assignments\\IS211_Assignment12\\hw13.db'
USERNAME = 'admin'
PASSWORD = 'password'
headings1 = ("ID", "Last Name", "First Name", "Results")
headings2 = ("ID", "Subject", "Number of Questions", "Quiz Date")
headings3 = ("Quiz ID", "Score")
students = []
quizzes = []
results = []


#(1, "Smith", "John"),
    #(2, "Sally", "Brown")
#)
#quizzes = (
    #(1, "Python Basics", 5, "February 5th, 2015"),
    #(2, "Digital Literacy", 10, "March 24th, 2024")
#)


def connect_db():
    connection = sqlite3.connect('DATABASE')
    return connection


def init_db():
    con = connect_db()
    with open('schema.sql', mode='r') as f:
        con.executescript(f.read())
        con.commit()
        con.close()
        print("database initialized")

def get_db_connection():
    conn = sqlite3.connect('DATABASE')
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db




@app.teardown_request
def teardown_request(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def hello_world():
    return redirect(url_for('login'))

# Ensure user is logged in before being able to access pages after login page.
def login_required(test):
    @wraps(test)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


# Login page for class app
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        username_check = 'admin'
        password_check = 'password'

        if not username:
            error = 'Please enter a username.'
        elif not password:
            error = 'Please enter a password.'
        elif username != username_check:
            error = 'Incorrect username. Please enter a valid username.'
        elif password != password_check:
            error = 'Incorrect password. Please enter a valid password.'
        if error is not None:
            flash(error)
        else:
            session['logged_in'] = True
            return redirect('/dashboard')

    return render_template('login.html')

# Dashboard for Class Information
@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
        students.clear()
        conn = get_db_connection()
        cur = conn.execute("SELECT id, last_name, first_name FROM students").fetchall()
        for row in cur:
            students_row = (row[0], row[1], row[2])
            students.append(students_row)

        quizzes.clear()
        cur_1 = conn.execute("SELECT id, subject, number_of_questions, date_given FROM quizzes").fetchall()
        for row in cur_1:
            quizzes_row = (row[0]), (row[1]), (row[2]), (row[3])
            quizzes.append(quizzes_row)
        return render_template('dashboard.html', headings1=headings1, students=students, headings2=headings2, quizzes=quizzes)

# Add students to class
@app.route('/student/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'GET':
        return render_template('addstudent.html')
    elif request.method == 'POST':
        add_name = request.form['first_name'], request.form['last_name']
        conn = get_db_connection()
        conn.execute("INSERT INTO students (first_name, last_name) VALUES (?, ?)", add_name)
        conn.commit()

    flash('New student successfully added')
    return redirect(url_for('dashboard'))

# Add quizzes
@app.route('/quiz/add', methods=['GET', 'POST'])
@login_required
def add_quiz():
    if request.method == 'GET':
        return render_template('addquiz.html')
    elif request.method == 'POST':
        add_quiz = request.form['subject'], request.form['number_of_questions'], request.form['date_given']
        conn = get_db_connection()
        conn.execute("INSERT INTO quizzes (subject, number_of_questions, date_given) VALUES (?, ?, ?)", add_quiz)
        conn.commit()

    flash('New quiz successfully added')
    return redirect(url_for('dashboard'))

# View quiz results. Search by looking up a student's ID in the database
@app.route('/student/<id>', methods=['GET'])
@login_required
def view_results(id):
    results.clear()
    conn = get_db_connection()
    cur_2 = conn.execute("SELECT quiz_id, score FROM students_result WHERE student_id = ?", id).fetchall()
    print(cur_2)
    if cur_2 == []:
        flash('No Results')
        return render_template('viewresults.html')
    else:
        for row in cur_2:
            results_row = (row[0], row[1])
            results.append(results_row)
    return render_template('viewresults.html', headings3=headings3, results=results)

# Add quiz results
@app.route('/results/add', methods=['GET', 'POST'])
@login_required
def add_results():
    quizzes_1 = []
    students_1 = []
    quizzes_1.clear()
    students_1.clear()
    conn = get_db_connection()
    if request.method == 'GET':
        cur_3 = conn.execute("SELECT id, subject FROM Quizzes").fetchall()
        for row in cur_3:
            quizzes_row = (row[0]), (row[1])
            quizzes_1.append(quizzes_row)
        cur_4 = conn.execute("SELECT id, first_name, last_name FROM students").fetchall()
        for row in cur_4:
            students_row = (row[0], '{}, {}'.format(row[2], row[1]))
            students_1.append(students_row)
        return render_template('addresults.html', quizzes_1=quizzes_1, students_1=students_1)
    elif request.method == 'POST':
            cur_5 = conn.execute("SELECT id, subject FROM Quizzes").fetchall() # Get quiz id for selected quiz
            for row in cur_5:
                if row[1] == request.form['Quiz']:
                   add_quiz_id = row[0]
            cur_6 = conn.execute("SELECT id, first_name, last_name FROM students").fetchall() # Get student id for selected student
            for row in cur_6:
                row_name = (f"{row[2]}, {row[1]}")
                if row_name == request.form['Student']:
                    add_student_id = row[0]
                    conn.execute("INSERT INTO students_result (student_id, quiz_id, score) VALUES (?, ?, ?)", (add_student_id, add_quiz_id, request.form['grade']))
                    conn.commit()
            flash("Quiz results updated")
            return redirect('/dashboard')
    else:
        flash("Could Not Update Record")
        return redirect('/results/add')


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('login'))




if __name__ == '__main__':
    app.run(debug=True)
