from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Table, Column, Integer, Text, String, Date, ForeignKey, TIMESTAMP, MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin



convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention = convention)

db = SQLAlchemy(metadata=metadata)

order_clothes_association = Table('order_clothes', db.Model.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('clothes_id', Integer, ForeignKey('clothes.id'))
)

class Customer(db.Model, SerializerMixin):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(Text, nullable=False, unique=True)
    created_at = Column(TIMESTAMP)

    orders = relationship('Order', back_populates="customer")

    serialize_rules = ('-orders.customer',)

class Order(db.Model, SerializerMixin):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    order_date = Column(Date, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'))

    customer = relationship('Customer', back_populates="orders")
    clothes = relationship('Clothes', secondary=order_clothes_association, back_populates="orders")

    serialize_rules = ('-customer.orders', '-clothes.orders')
    serialize_only = ('id', 'order_date', 'customer', 'clothes')

class Clothes(db.Model, SerializerMixin):
    __tablename__ = "clothes"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    size = Column(Text, nullable=False)
    color = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(Date)

    orders = relationship('Order', secondary=order_clothes_association, back_populates="clothes")
    customers = association_proxy('orders', 'customer', creator=lambda customer: Order(customer=customer))

    serialize_rules = ('-orders.clothes',)
