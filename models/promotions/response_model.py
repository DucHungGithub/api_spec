from typing import List
from pydantic import BaseModel

class PromotionResponseModel(BaseModel):
    promotion_id: str 
    promotion_name: str
    region: str
    zone: str
    area: str

class PromotionPaginationResponseModel(BaseModel):
    data: List[PromotionResponseModel]
    total: int

class OutletJoinedPromotionResponseModel(BaseModel):
    outlet_id: str
    outlet_name: str
    promotion_id: str
    region: str
    zone: str
    area: str
    total_photos: int

class OutletJoinedPromotionPaginationResponseModel(BaseModel):
    data: List[OutletJoinedPromotionResponseModel]
    total: int
    total_outlets: int
    total_photos: int
