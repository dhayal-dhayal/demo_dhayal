import employee
from employee import Employee

#calc_employee= employee.Employee ('abc',105,106)
#print(type(calc_employee))
#print (isinstance(calc_employee,Employee))
#print(calc_employee.display_employee_details())

def add(x, y):
    return x + y
def subtract(x, y):
    return x - y
def division (x , y):
    return round(x/y)
print("Select calc operation:")
print("1. Add")
print("2. Subtract")
print("3. Division")
choice =  (input("Enter choice (1 or 2 or 3): "))

if choice in ['1', '2','3']:
    num1 = int(input("Enter first number: "))
    num2 = int(input("Enter second number: "))
    if choice == '1':
       # value = add(num1,num2)
        print (add(num1,num2))


