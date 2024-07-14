from pydantic import BaseModel


class FavoriteSchema(BaseModel):
    id:int
    user_id:int
    product_id:int