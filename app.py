from flask import Flask, request, jsonify, render_template
from models import db, Employee

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

with app.app_context():
    db.create_all()

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Add employee
@app.route('/add', methods=['POST'])
def add_employee():
    data = request.get_json()

    emp = Employee(
        name=data['name'],
        role=data['role'],
        salary=data['salary']
    )

    db.session.add(emp)
    db.session.commit()

    return jsonify({"message": "Employee added"})

# Get all employees
@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    result = []

    for emp in employees:
        result.append({
            "id": emp.id,
            "name": emp.name,
            "role": emp.role,
            "salary": emp.salary
        })

    return jsonify(result)

# Update employee
@app.route('/update/<int:id>', methods=['PUT'])
def update_employee(id):
    emp = Employee.query.get(id)
    data = request.get_json()

    emp.name = data['name']
    emp.role = data['role']
    emp.salary = data['salary']

    db.session.commit()

    return jsonify({"message": "Updated"})

# Delete employee
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_employee(id):
    emp = Employee.query.get(id)
    db.session.delete(emp)
    db.session.commit()

    return jsonify({"message": "Deleted"})

if __name__ == '__main__':
    app.run(debug=True)