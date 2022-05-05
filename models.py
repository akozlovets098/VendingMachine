from pydantic import BaseModel


class Category(BaseModel):
    name: str
    price: float
    quantity: int = 0
