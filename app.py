from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

# In-memory storage for employees (replace with a database in production)
employees = [
    # {"id": 1, "name": "John Doe", "mobile": "1234567890", "country": "USA", "department": "HR"},
    # {"id": 2, "name": "Jane Smith", "mobile": "0987654321", "country": "Canada", "department": "Engineering"},
]

# Function to get the next available ID (for simplicity)
def get_next_id():
    if employees:
        return max(emp["id"] for emp in employees) + 1
    return 1

# Route to display the employee table
@app.route('/')
def index():
    return render_template('index.html', employees=employees)

# Route to handle the creation of a new employee
@app.route('/create', methods=['POST'])
def create_employee():
    new_employee = {
        "id": get_next_id(),
        "name": request.form['name'],
        "mobile": request.form['mobile'],
        "country": request.form['country'],
        "department": request.form['department']  # Capture department from form
    }
    employees.append(new_employee)
    return redirect(url_for('index'))

# Route to handle deleting an employee
@app.route('/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    global employees
    employees = [emp for emp in employees if emp['id'] != id]
    return redirect(url_for('index'))

# Route to handle updating an employee
@app.route('/update/<int:id>', methods=['POST'])
def update_employee(id):
    for employee in employees:
        if employee['id'] == id:
            employee['name'] = request.form['name']
            employee['mobile'] = request.form['mobile']
            employee['country'] = request.form['country']
            employee['department'] = request.form['department']  # Update department
            break
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
