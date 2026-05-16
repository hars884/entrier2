from flask import Flask, render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
db=SQLAlchemy(app)
global eid
eid=0
class department(db.Model):
    name=db.Column(db.String(100),primary_key=True)
    dept_id=db.Column(db.Integer,nullable=False)
class Employee(db.Model):
    # employee_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False,primary_key=True)
    gmail= db.Column (db.String(100),nullable=False)
    department=db.Column(db.String(100),nullable=False)
    salary=db.Column(db.Integer,nullable=False)
    joindate=db.Column(db.String(100),nullable=False)
class user(db.Model):
    username=db.Column(db.String(100),primary_key=True)
    password=db.Column(db.String(100),nullable=False)

@app.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = user.query.filter_by(username=username, password=password).first()
        global curr_user
        curr_user=username
        
        if user_data:
            return redirect(url_for('dashboard', username=curr_user))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = user(username=username, password=password)
        
        db.session.add(new_user)
        # developer = department(name='Developer', dept_id=1)
        # manager = department(name='Manager', dept_id=2)
        # hr = department(name='HR', dept_id=3)
        # db.session.add(developer)
        # db.session.add(manager)
        # db.session.add(hr)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    employeedata=Employee.query.all()
    return render_template('dashboard.html',employeedata=employeedata,username=request.args.get('username'))

@app.route('/newemployee',methods=['GET','POST'])
def newemployee():
    if request.method == 'POST':
        name = request.form['name']
        gmail = request.form['gmail']
        department = request.form['department']
        salary = request.form['salary']
        joindate = request.form['joindate']
        new_employee = Employee(name=name, gmail=gmail, department=department, salary=salary, joindate=joindate)
        db.session.add(new_employee)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('newemployee.html')

@app.route('/delete/<string:name>', methods=['POST','GET'])
def delete_employee(name):
    employee = Employee.query.get(name)
    if employee:
        db.session.delete(employee)
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/edit/<string:name>', methods=['GET','POST'])
def edit_employee_form(name):
    employee = Employee.query.get(name)
    if request.method == 'POST':
        employee = Employee.query.get(name)
        employee.name = request.form['name']
        employee.gmail = request.form['gmail']
        employee.department = request.form['department']
        employee.salary = request.form['salary']
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('edit.html', employee=employee)

if __name__ == '__main__':  
    with app.app_context():
        db.create_all()
    app.run(debug=True)