from pydantic import BaseModel, ConfigDict


class Product(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str | int
    name: str
    price: float


class ProductPage(BaseModel):
    model_config = ConfigDict(extra="ignore")
    current_page: int
    data: list[Product]
    total: int