from typing import List

from fastapi import APIRouter

from models.locations.response_model import RegionResponseModel, AreaResponseModel

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
            "/areas",
            self.get_areas,
            methods=["GET"],
            status_code=200,
            summary="Get all areas"
        )
        
        
    async def get_regions(self) -> List[RegionResponseModel]:
        return [RegionResponseModel(
            id=str(i),
            name=f"region_{i}"
        ) for i in range(100)]
    
    async def get_areas(self) -> List[AreaResponseModel]:
        return [AreaResponseModel(
            id=str(i),
            name=f"area_{i}"
        ) for i in range(100)]