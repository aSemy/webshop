from sqlalchemy import (
    Table,
    ForeignKey,
    Column,
    Integer,
    Text,
    DateTime,
    func
)

from sqlalchemy.orm import relationship

from .meta import Base


# # join table between orders and its components
# class OrderedComponent(Base):
#     __tablename__ = 'ordered_components'
#     order_id = Column('order_id', Integer, ForeignKey('orders.id'), primary_key=True)
#     component_id = Column('component_id', Integer, ForeignKey('components.id'), primary_key=True)
#     component = relationship("Component")

ordered_components_table = Table('ordered_components', Base.metadata,
                                 Column('order_id', Integer, ForeignKey('orders.id')),
                                 Column('component_id', Integer, ForeignKey('components.id'))
                                 )


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, nullable=False)
    created = Column(DateTime, default=func.now(), nullable=False)
    preferred_delivery_datetime = Column(DateTime)
    components = relationship("Component", secondary=ordered_components_table)


class Component(Base):
    __tablename__ = 'components'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    price = Column(Text, nullable=False)



