from pydantic import BaseModel

class OutletResponseModel(BaseModel):
    outlet_id: str 
    outlet_name: str  
    region: str  
    zone: str
    area: str
    total_promotions: int 
    total_photos: int 
    validated_by_sa: bool = False 
    validated_by_fa: bool = False 
    
