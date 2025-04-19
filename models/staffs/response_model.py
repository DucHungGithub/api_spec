from pydantic import BaseModel

class StaffResponseModel(BaseModel):
    id: str
    name: str
    
class SAResponseModel(StaffResponseModel):
    pass

class FAResponseModel(StaffResponseModel):
    pass