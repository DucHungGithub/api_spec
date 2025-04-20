from typing import List
from pydantic import BaseModel

from enums.validation_status import ValidationStatus

class PromotionResponseModel(BaseModel):
    promotion_id: str 
    promotion_name: str
    region: str
    zone: str
    area: str
    sa_kpi_progress: float
    fa_kpi_progress: float

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
    ai_validation_result: ValidationStatus
    sa_validated_result: ValidationStatus
    fa_validated_result: ValidationStatus
    total_photos: int

class OutletJoinedPromotionPaginationResponseModel(BaseModel):
    data: List[OutletJoinedPromotionResponseModel]
    total: int
    total_outlets: int
    total_photos: int
