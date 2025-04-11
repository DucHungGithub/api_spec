from typing import Optional, List
from fastapi import APIRouter, Query

from models import PromotionResponseModel, OutletResponseModel


class PromotionRouter(APIRouter):
    def __init__(self, *args, **kwargs) -> None:
        super(PromotionRouter, self).__init__(*args, **kwargs)
        
        self.add_api_route(
            "/",
            self.get_promotions,
            methods=["GET"],
            status_code=200,
            summary="Get list of outlets with optional filters"
        )
        
        self.add_api_route(
            "/{promotion_id}/outlets",
            self.get_promotion_outlets,
            methods=["GET"],
            status_code=200,
            summary="Get list of outlets of promotion"
        )
        
        
    
    
    async def get_promotions(
        self,
        region: Optional[str] = Query(None, description="Filter promotions by region"),
        zone: Optional[str] = Query(None, description="Filter promotions by zone"),
        area: Optional[str] = Query(None, description="Filter promotions by area")
    ) -> List[PromotionResponseModel]:
        """
        Returns a list of promotions, filtered by Region, Zone, and/or Area if provided.
        Only promotions available at outlets in the specified region, zone, or area will be returned.
        """
        pass
    
    
    async def get_promotion_outlets(self, promotion_id: str) -> List[OutletResponseModel]:
        """
        Returns a list of outlets that offer the specified promotion.
        """
        pass
            