from pydantic import BaseModel

class LocationResponseModel(BaseModel):
    id: str
    name: str
    
class AreaResponseModel(LocationResponseModel):
    pass

class RegionResponseModel(LocationResponseModel):
    pass