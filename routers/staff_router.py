from fastapi import APIRouter

from models.staffs.response_model import FAResponseModel, SAResponseModel

class StaffRouter(APIRouter):
    def __init__(self, *args, **kwargs) -> None:
        super(StaffRouter, self).__init__(*args, **kwargs)
        
        self.add_api_route(
            "/sa",
            self.get_sa,
            methods=["GET"],
            status_code=200,
            summary="Get the list sa"
        )
        
        self.add_api_route(
            "/fa",
            self.get_fa,
            methods=["GET"],
            status_code=200,
            summary="Get the list fa"
        )
        
    
    async def get_sa(self):
        return [SAResponseModel(
            id=str(i),
            name=f"sa_{i}"
        ) for i in range(100)]
    
    async def get_fa(self):
        return [FAResponseModel(
            id=str(i),
            name=f"fa_{i}"
        ) for i in range(100)]
    