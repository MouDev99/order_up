from dotenv import load_dotenv

load_dotenv()


from app import app, db
from app.models import Employee, Menu, MenuItem, MenuItemType, Table


with app.app_context():
    db.drop_all()
    db.create_all()

    employee = Employee(name="Margon", employee_number="1234", password="password")
    db.session.add(employee)
    db.session.commit()

    beverages = MenuItemType(name="Beverages")
    entrees = MenuItemType(name="Entrees")
    sides = MenuItemType(name="Sides")

    dinner = Menu(name="Dinner")

    fries = MenuItem(name="French fries", price=3.50, type=sides, menu=dinner)
    drp = MenuItem(name="Dr. Pepper", price=1.0, type=beverages, menu=dinner)
    jambalaya = MenuItem(name="Jambalaya", price=21.98, type=entrees, menu=dinner)

    db.session.add(dinner)
    db.session.commit()

    tables = [
    Table(number=1, capacity=4),
    Table(number=2, capacity=6),
    Table(number=3, capacity=2),
    Table(number=4, capacity=8),
    Table(number=5, capacity=3),
    Table(number=6, capacity=7),
    Table(number=7, capacity=2),
    Table(number=8, capacity=8),
    Table(number=9, capacity=5),
    Table(number=10, capacity=6)
    ]

    for table in tables:
        db.session.add(table)

    db.session.commit()
