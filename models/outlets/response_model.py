from typing import List
from pydantic import BaseModel

class OutletResponseModel(BaseModel):
    outlet_id: str 
    outlet_name: str  
    region: str  
    zone: str
    area: str

class OutletPaginationResponseModel(BaseModel):
    data: List[OutletResponseModel]
    total: int
    
class PromotionByOutletResponseModel(BaseModel):
    promotion_id: str 
    promotion_name: str
    outlet_id: str
    validated_by_sa: bool = False
    validated_by_fa: bool = False
    total_photos: int

class PromotionByOutletPaginationResponseModel(BaseModel):
    data: List[PromotionByOutletResponseModel]
    total: int
    total_promotions: int
    total_photos: int
