# CREATE/DEFINE MODELS:

from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Column
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


# = ASSOCIATION TABLE: 
service_mechanic = db.Table(
    'service_mechanic', 
    Base.metadata, 
    Column('ticket_id', ForeignKey('service_tickets.id')),
    Column('mechanic_id', ForeignKey('mechanics.id'))
) # Many-to-Many relationship btwn Mechanics & Service Tickets:




# = 1. CUSTOMERS:
class Customer(Base):
    __tablename__ = 'customers'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(250), nullable=False)
    email: Mapped[str] = mapped_column(db.String(350), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)

    # One-to-Many relationship w/ Service Tickets:
    service_tickets: Mapped[List['Service_Ticket']] = relationship(back_populates='customer', cascade='all, delete-orphan')




# = 2. SERVICE TICKETS:
class Service_Ticket(Base):
    __tablename__ = 'service_tickets'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(50), nullable=False, unique=True)
    service_date: Mapped[str] = mapped_column(db.String(100), nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(350), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))
    
# Relationships:
    # Many-to-One relationship w/ Customer:
    customer: Mapped['Customer'] = relationship(back_populates='service_tickets')
    
    # Many-to-Many relationship w/ Mechanics:
    mechanics: Mapped[List['Mechanic']] = relationship(secondary=service_mechanic, back_populates='service_tickets')
    


# = 3. MECHANICS:
class Mechanic(Base):
    __tablename__ = 'mechanics'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(250), nullable=False)
    email: Mapped[str] = mapped_column(db.String(350), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(15), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)


    # Many-to-Many relationship w/ Service Tickets:
    service_tickets: Mapped[List['Service_Ticket']] = relationship(secondary=service_mechanic, back_populates='mechanics')
    