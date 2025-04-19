from pydantic import BaseModel

class LocationResponseModel(BaseModel):
    id: str
    name: str
    
class ZoneResponseModel(LocationResponseModel):
    pass

class RegionResponseModel(LocationResponseModel):
    pass