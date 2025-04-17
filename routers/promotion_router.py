from typing import Optional, List
from fastapi import APIRouter, Query

from models import PromotionResponseModel, OutletResponseModel
from models.promotions.response_model import OutletJoinedPromotionPaginationResponseModel, OutletJoinedPromotionResponseModel, PromotionPaginationResponseModel


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
        area: Optional[str] = Query(None, description="Filter promotions by area"),
        limit: int = Query(10, description="Limit the number of outlets returned"),
        offset: int = Query(0, description="Offset for pagination")
    ) -> PromotionPaginationResponseModel:
        """
        Returns a list of promotions, filtered by Region, Zone, and/or Area if provided.
        Only promotions available at outlets in the specified region, zone, or area will be returned.
        """
        total = 100
        promotions = [PromotionResponseModel(
            promotion_id=str(i),
            promotion_name=f"Promotion {i}",
            region=f"Region {i}",
            zone=f"Zone {i}",
            area=f"Area {i}"
        ) for i in range(1, total + 1)]
        return PromotionPaginationResponseModel(data=promotions[offset:offset+limit], total=total)
    
    
    async def get_promotion_outlets(
        self, 
        promotion_id: str, 
        limit: int = Query(10, description="Limit the number of outlets returned"),
        offset: int = Query(0, description="Offset for pagination")
    ) -> OutletJoinedPromotionPaginationResponseModel:
        """
        Returns a list of outlets that offer the specified promotion.
        """
        total = 100
        outlets = [OutletJoinedPromotionResponseModel(
            outlet_id=str(i), 
            promotion_id=promotion_id,
            outlet_name=f"Outlet {i}", 
            region=f"Region {i}", 
            zone=f"Zone {i}", 
            area=f"Area {i}",
            total_photos=10
        ) for i in range(1, total + 1)]
        return OutletJoinedPromotionPaginationResponseModel(
            data=outlets[offset:offset+limit], 
            total=total,
            total_outlets=total,
            total_photos=total
        )
            