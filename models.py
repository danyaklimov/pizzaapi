from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    password = Column(Text, nullable=True)
    email = Column(String(100), unique=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"


class Order(Base):

    ORDER_STATUSES = (
        ("PENDING", "pending"),
        ("IN-TRANSIT", "in-transit"),
        ("DELIVERED", "delivered")
    )

    PIZZA_SIZES = (
        ("SMALL", "small"),
        ("MEDIUM", "medium"),
        ("LARGE", "large"),
        ("EXTRA-LARGE", "extra-large")
    )

    FLAVOURS = (
        ("PEPERONI", "peperoni"),
        ("FOUR-CHEESE", "four-cheese"),
        ("PINEAPPLE", "pineapple")
    )

    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices=ORDER_STATUSES), default="PENDING")
    pizza_size = Column(ChoiceType(choices=PIZZA_SIZES), default="SMALL")
    flavour = Column(ChoiceType(choices=FLAVOURS), default="PEPERONI")
    user = relationship("User", back_populates="orders")
    user_id = Column(Integer, ForeignKey("user.id"))

    def __repr__(self):
        return f"<Order {self.id}>"
