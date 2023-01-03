# Cursor Paginate

## Installation
First of all, you need to install villain-pagination on your local to start.
```
pip install villain-pagination
```

## Minimal Example
`Villain Paginator` uses SQLAlchemy ORM. 

Let's start with a simple example below.
You need to import `page` and `paginator` function from `villain-pagination`.

- `page` : is a class which used as `response_model` in your route declaration.
- `paginator` : is main functions that will paginate your data.

To use paginate, 5 params required.

- `db` : is a SQLAlchemy session.
- `model` : is a object which you want to paginate.
- `cursor` : is a position of a page requested to show.
- `order_by` : is a column of the model.
- `size` : is a number of data which will shown in one page.

And Here is an example.

```python
from typing import Iterator, Any
from faker import Faker
from fastapi import Depends, FastAPI
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from villain import page, paginator

engine = create_engine("sqlite:///.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=True, autoflush=True, bind=engine)

Base = declarative_base(bind=engine)

fake = Faker()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

Base.metadata.create_all()

app = FastAPI()

@app.on_event("startup")
def on_startup() -> None:
    session = SessionLocal()
    session.add_all([User(name=fake.name()) for _ in range(100)])
    session.flush()
    session.close()

def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/", response_model=page.Page)
def get_users(db: Session = Depends(get_db)) -> Any:
    return paginator.paginate_cursor(db = db, model = User, cursor = 10,order_by= User.id, page = 0, size = 10)

```