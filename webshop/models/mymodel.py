from sqlalchemy import (
    Table,
    ForeignKey,
    Column,
    Integer,
    Text,
    DateTime,
    Enum,
    func
)

import enum
from enum import unique

from sqlalchemy.orm import relationship

from .meta import Base


@unique
class OrderStatus(enum.Enum):
    CREATED = enum.auto()
    DELIVERED = enum.auto()

# # join table between orders and its components
# TODO add this, and also add 'sale_price' and 'quantity'
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
    status = Column(Enum(OrderStatus), default=OrderStatus.CREATED)
    preferred_delivery_datetime = Column(DateTime)
    components = relationship("Component", secondary=ordered_components_table)
    # TODO add status enum (ordered, delivered)


class Component(Base):
    __tablename__ = 'components'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    price = Column(Text, nullable=False)



