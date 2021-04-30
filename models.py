# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Wallet(Base):
    __tablename__ = "wallet"

    idx = Column(
        Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    owner = Column(
        Integer,
        nullable=False
    )

    name = Column(
        String(30),
        nullable=False
    )

    count = Column(
        Integer,
        nullable=False,
        default=0
    )

    def __repr__(self):
        return f"<Wallet owner={self.owner!r}, name={self.name!r}, count={self.count}>"


class Coin(Base):
    __tablename__ = "coin"

    name = Column(
        String(30),
        unique=True,
        primary_key=True,
        nullable=False
    )

    price = Column(
        Integer,
        nullable=False
    )

    def __repr__(self):
        return f"<Coin name={self.name!r}, price={self.price}>"


class Point(Base):
    __tablename__ = "point"

    owner = Column(
        Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    point = Column(
        Integer,
        nullable=False
    )

    def __repr__(self):
        return f"<Point owner={self.owner}, point={self.point}>"
