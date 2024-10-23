from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuring SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Employee Model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    country = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Employee {self.name}>'

# Create the database and tables
with app.app_context():
    db.create_all()

# Route to display all employees and the form
@app.route('/')
def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

# Route to add a new employee
@app.route('/create', methods=['POST'])
def create_employee():
    name = request.form['name']
    mobile = request.form['mobile']
    country = request.form['country']

    new_employee = Employee(name=name, mobile=mobile, country=country)
    db.session.add(new_employee)
    db.session.commit()

    return redirect(url_for('index'))

# Route to delete an employee
@app.route('/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    
    return redirect(url_for('index'))

# Route to update an employee
@app.route('/update/<int:id>', methods=['POST'])
def update_employee(id):
    employee = Employee.query.get_or_404(id)
    employee.name = request.form['name']
    employee.mobile = request.form['mobile']
    employee.country = request.form['country']

    db.session.commit()
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
