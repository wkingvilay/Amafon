from pydantic import BaseModel

class Categories(BaseModel):
    category_name: str

class CategoriesRead(Categories):
    category_id: int