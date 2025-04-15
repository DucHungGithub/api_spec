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
        
        self.promotions = [
            {
                "promotion_id": "promo1",
                "promotion_name": "Summer Sale 2025",
                "region": "North",
                "zone": "Urban",
                "area": "Downtown"
            },
            {
                "promotion_id": "promo2",
                "promotion_name": "Spring Collection Launch",
                "region": "South",
                "zone": "Urban",
                "area": "Mall"
            },
            {
                "promotion_id": "promo3",
                "promotion_name": "Holiday Special",
                "region": "East",
                "zone": "Suburban",
                "area": "Plaza"
            },
            {
                "promotion_id": "promo4",
                "promotion_name": "Weekend Discount",
                "region": "West",
                "zone": "Rural",
                "area": "Main Street"
            },
            {
                "promotion_id": "promo5",
                "promotion_name": "Clearance Sale",
                "region": "North",
                "zone": "Suburban",
                "area": "Shopping Center"
            }
        ]
        
        # Mock outlet joined promotion data
        self.outlets_by_promotion = {
            "promo1": [
                {
                    "outlet_id": "outlet1",
                    "outlet_name": "Downtown Flagship Store",
                    "promotion_id": "promo1",
                    "region": "North",
                    "zone": "Urban",
                    "area": "Downtown",
                    "total_photos": 2
                },
                {
                    "outlet_id": "outlet2",
                    "outlet_name": "Urban Center Store",
                    "promotion_id": "promo1",
                    "region": "North",
                    "zone": "Urban",
                    "area": "Downtown",
                    "total_photos": 1
                }
            ],
            "promo2": [
                {
                    "outlet_id": "outlet1",
                    "outlet_name": "Downtown Flagship Store",
                    "promotion_id": "promo2",
                    "region": "North",
                    "zone": "Urban",
                    "area": "Downtown",
                    "total_photos": 1
                },
                {
                    "outlet_id": "outlet3",
                    "outlet_name": "South Mall Store",
                    "promotion_id": "promo2",
                    "region": "South",
                    "zone": "Urban",
                    "area": "Mall",
                    "total_photos": 1
                }
            ],
            "promo3": [
                {
                    "outlet_id": "outlet2",
                    "outlet_name": "Urban Center Store",
                    "promotion_id": "promo3",
                    "region": "North",
                    "zone": "Urban",
                    "area": "Downtown",
                    "total_photos": 1
                },
                {
                    "outlet_id": "outlet4",
                    "outlet_name": "East Plaza Store",
                    "promotion_id": "promo3",
                    "region": "East",
                    "zone": "Suburban",
                    "area": "Plaza",
                    "total_photos": 1
                }
            ],
            "promo4": [
                {
                    "outlet_id": "outlet1",
                    "outlet_name": "Downtown Flagship Store",
                    "promotion_id": "promo4",
                    "region": "North",
                    "zone": "Urban",
                    "area": "Downtown",
                    "total_photos": 1
                },
                {
                    "outlet_id": "outlet5",
                    "outlet_name": "West Rural Store",
                    "promotion_id": "promo4",
                    "region": "West",
                    "zone": "Rural",
                    "area": "Main Street",
                    "total_photos": 1
                }
            ],
            "promo5": [
                {
                    "outlet_id": "outlet3",
                    "outlet_name": "South Mall Store",
                    "promotion_id": "promo5",
                    "region": "South",
                    "zone": "Urban",
                    "area": "Mall",
                    "total_photos": 1
                }
            ]
        }
        
        
    
    
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
        filtered_promotions = self.promotions
        
        if region:
            filtered_promotions = [p for p in filtered_promotions if p["region"] == region]
        
        if zone:
            filtered_promotions = [p for p in filtered_promotions if p["zone"] == zone]
        
        if area:
            filtered_promotions = [p for p in filtered_promotions if p["area"] == area]
        
        # Apply pagination
        paginated_promotions = filtered_promotions[offset:offset+limit]
        
        # Convert to response model format
        result_data = [PromotionResponseModel(**p) for p in paginated_promotions]
        
        return PromotionPaginationResponseModel(
            data=result_data,
            total=len(filtered_promotions)
        )
    
    
    async def get_promotion_outlets(self, promotion_id: str) -> OutletJoinedPromotionPaginationResponseModel:
        """
        Returns a list of outlets that offer the specified promotion.
        """
        if promotion_id not in self.outlets_by_promotion:
            # Return empty result if promotion not found
            return OutletJoinedPromotionPaginationResponseModel(
                data=[],
                total=0,
                total_outlets=0,
                total_photos=0
            )
        
        outlets = self.outlets_by_promotion[promotion_id]
        total_photos = sum(outlet["total_photos"] for outlet in outlets)
        
        # Convert to response model format
        result_data = [OutletJoinedPromotionResponseModel(**o) for o in outlets]
        
        return OutletJoinedPromotionPaginationResponseModel(
            data=result_data,
            total=len(outlets),
            total_outlets=len(outlets),
            total_photos=total_photos
        )
            