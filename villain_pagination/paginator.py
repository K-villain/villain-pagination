from sqlalchemy.orm import Session
from fastapi import HTTPException
from .page import Page


def paginate(db: Session, model: object, order_by: object, page: int, size: int):
    objects = get_objects(db, model, order_by, page, size)

    if len(objects) == 0:
        raise HTTPException(status_code=404, detail="Page not found")

    return create_page(objects, page, size)


def paginate_cursor(db: Session, model: object, order_by: object, cursor : int, size: int):
    objects = get_objects_cursor(db, model, order_by, cursor, size)

    if len(objects) == 0:
        raise HTTPException(status_code=404, detail="Page not found")

    return create_page(objects, cursor//size, size)


def get_objects(db: Session, model: object, order_by: object, page: int, size: int):

    size, page, order_by = valid_params(model, size, page, order_by)

    query = db.query(*model) if isinstance(model, list) else db.query(model)
    return query.order_by(order_by).offset(page * size).limit(size).all()


def get_objects_cursor(db: Session, model: object, order_by: object, cursor : int, size: int):

    size, page, order_by = valid_params(model, size, 0, order_by)
    if cursor == '' or size < 0 or cursor is None:
        cursor = 0

    query = db.query(*model) if isinstance(model, list) else db.query(model)
    return query.filter(order_by > cursor).order_by(order_by).limit(size).all()


def valid_params(model, size, page, order_by):
    if size == 0 or size < 0:
        size = 5

    if page < 0:
        page = 0

    if order_by == '':
        order_by = model.id

    return size, page, order_by,


def create_page(items, page: int, size: int) -> Page:
    new_page = Page.create(items, page, size)
    return new_page
