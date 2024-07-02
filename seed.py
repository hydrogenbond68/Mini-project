
from random import choice as rc
from faker import Faker
from datetime import datetime

from app import app, db  
from models import Customer, Order, Clothes, order_clothes_association

def seed_data():
    with app.app_context():
        
        fake = Faker()

        
        db.drop_all()
        db.create_all()

    
        customers = []
        for _ in range(5):
            customer = Customer(
                name=fake.name(),
                email=fake.email(),
                phone=fake.phone_number(),
                created_at=datetime.now()
            )
            customers.append(customer)
            db.session.add(customer)

        
        clothes = []
        clothing_types = ['Shirt', 'Pants', 'Dress', 'Jacket', 'Hat']
        colors = ['Red', 'Blue', 'Green', 'Yellow', 'Black']
        for _ in range(10):
            cloth = Clothes(
                name=fake.color_name() + ' ' + rc(clothing_types),
                size=rc(['S', 'M', 'L', 'XL']),
                color=rc(colors),
                price=fake.random_number(digits=2),
                quantity=fake.random_int(min=1, max=100),
                created_at=datetime.now()
            )
            clothes.append(cloth)
            db.session.add(cloth)


        orders = []
        for _ in range(10):
            order = Order(
                order_date=fake.date_this_decade(),
                customer=rc(customers)
            )
            order.clothes = rc(clothes, size=fake.random_int(min=1, max=3))
            orders.append(order)
            db.session.add(order)

        
        db.session.commit()

if __name__ == '__main__':
    seed_data()
