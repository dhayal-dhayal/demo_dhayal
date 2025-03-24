

class Employee:
    company_name = 'lenovo'
    def __init__(self, name , emp_id , salary):
        self.name = name
        self.id = emp_id
        self.salary = salary

    def display_employee_details(self):
        print(f"Employee Name: {self.name}")
        print(f"Employee ID: {self.id}")
        print(f"Employee Salary: {self.salary}")


employee_1 = Employee('navin', 101, 100)
employee_2 = Employee('kevin', 102, 200)
employee_3 = Employee(None,None,None)

print(employee_1.company_name)

