from pydantic import BaseModel

class PromotionResponseModel(BaseModel):
    promotion_id: str 
    number_of_outlets: int 
    validated_by_sa: bool = False 
    validated_by_fa: bool = False 