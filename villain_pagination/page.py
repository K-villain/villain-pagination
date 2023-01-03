from typing import Sequence, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class Page(BaseModel):
    items: Sequence[T]
    page: int
    size: int

    @classmethod
    def create(
            cls,
            items: Sequence[T],
            page: int,
            size: int
        ) :

        return cls(items=items, page=page, size=size)

    class Config :
        orm_mode=True

__all__ = [
    "Page"
]
