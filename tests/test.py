from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from typing import Sequence
import pytest
from villain_pagination import paginator
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)


db = SessionLocal()


def test_setting_page_size():
    ###
    # When parameters are set, the corresponding page is returned.
    ###

    res = paginator.paginate(db, Item, Item.id, 0, 5)
    temp = []
    for t in res.items:
        temp.append(t.id)

    assert temp == [1, 2, 3, 4, 5]


def test_setting_page_size_and_page():
    ###
    # When parameters are set, the corresponding page is returned.
    ###
    res = paginator.paginate(db, Item, Item.id, 1, 5)
    temp = []

    for t in res.items:
        temp.append(t.id)

    assert temp == [6, 7, 8, 9, 10]


def test_setting_page_size_over_maximum():
    ###
    # When the page size is set to a value greater than the maximum, the maximum is returned.
    ###
    res = paginator.paginate(db, Item, Item.id, 0, 100)
    temp = []

    for t in res.items:
        temp.append(t.id)

    assert temp == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def test_setting_page_size_to_zero():
    ###
    # When the page size is set to zero, the default is returned.
    ###
    res = paginator.paginate(db, Item, Item.id, 0, 0)
    temp = []

    for t in res.items:
        temp.append(t.id)

    assert temp == [1, 2, 3, 4, 5]


def test_empty_query_params_are_preserved():
    ###
    # When order_by object is set, the additional filter should not be activate.
    ###
    res = paginator.paginate(db, Item, '', 0, 5)
    temp = []

    if len(res.items) > 0:
        for t in res.items:
            temp.append(t.id)

    assert temp == [1, 2, 3, 4, 5]


def test_not_found_for_negative_page():
    ###
    # When requested data is empty, response empty list.
    ###
    res = paginator.paginate(db, Item, Item.id, -1, 5)
    temp = []

    if len(res.items) > 0:
        for t in res.items:
            temp.append(t.id)

    assert temp == [1, 2, 3, 4, 5]


def test_additional_query_params_are_preserved():
    with pytest.raises(Exception):
        paginator.paginate(db, Item, 'invalid', 0, 5)
