from fastapi import APIRouter

from models.locations.response_model import RegionResponseModel, ZoneResponseModel

class LocationRouter(APIRouter):
    def __init__(self, *args, **kwargs) -> None:
        super(LocationRouter, self).__init__(*args, **kwargs)
        
        self.add_api_route(
            "/regions",
            self.get_regions,
            methods=["GET"],
            status_code=200,
            summary="Get all regions"
        )
        
        self.add_api_route(
            "/zones",
            self.get_zones,
            methods=["GET"],
            status_code=200,
            summary="Get all zones"
        )
        
        
    async def get_regions(self):
        return [RegionResponseModel(
            id=str(i),
            name=f"region_{i}"
        ) for i in range(100)]
    
    async def get_zones(self):
        return [ZoneResponseModel(
            id=str(i),
            name=f"zone_{i}"
        ) for i in range(100)]