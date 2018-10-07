from sqlalchemy import (
    Table,
    ForeignKey,
    Column,
    Integer,
    Text,
    DateTime,
    Numeric,
    func
)

from sqlalchemy.orm import relationship

from .meta import Base

# join table between orders and its components
association_table = Table('association', Base.metadata,
                          Column('order_id', Integer, ForeignKey('orders.id')),
                          Column('component_id', Integer, ForeignKey('components.id'))
                          )


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, nullable=False)
    created = Column(DateTime, default=func.now(), nullable=False)
    preferred_delivery_datetime = Column(DateTime)
    components = relationship("Component", secondary=association_table)


class Component(Base):
    __tablename__ = 'components'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    price = Column(Numeric, nullable=False)



