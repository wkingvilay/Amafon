from pydantic import BaseModel

class Categories(BaseModel):
    category_id: int
    category_name: str
    