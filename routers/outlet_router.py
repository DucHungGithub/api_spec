from typing import Optional, List

from fastapi import APIRouter, Query

from models import ScoreRequestModel, OutletResponseModel, PromotionResponseModel, ImageResponseModel
from models.outlets.response_model import OutletPaginationResponseModel, PromotionByOutletPaginationResponseModel, PromotionByOutletResponseModel
from enums.validation_status import ValidationStatus




class OutletRouter(APIRouter):
    def __init__(self, *args, **kwargs) -> None:
        super(OutletRouter, self).__init__(*args, **kwargs)
        
        self.add_api_route(
            "/",
            self.get_outlets,
            methods=["GET"],
            status_code=200,
            summary="Get list of outlets with optional filters"
        )
        
        self.add_api_route(
            "/{outlet_id}",
            self.get_outlet,
            methods=["GET"],
            status_code=200,
            summary="Get details of a specific outlet"
        )
        
        self.add_api_route(
            "/{outlet_id}/promotions",
            self.get_outlet_promotions,
            methods=["GET"],
            status_code=200,
            summary="Get promotions for a specific outlet"
        )
        
        self.add_api_route(
            "/{outlet_id}/promotions/{promotion_id}",
            self.get_outlet_promotion,
            methods=["GET"],
            status_code=200,
            summary="Get details of a specific promotion for an outlet"
        )
        
        self.add_api_route(
            "/{outlet_id}/promotions/{promotion_id}/images",
            self.get_promotion_images,
            methods=["GET"],
            status_code=200,
            summary="Get images for a specific promotion"
        )
        
        self.add_api_route(
            "/{outlet_id}/promotions/{promotion_id}/images/{image_id}",
            self.get_promotion_image,
            methods=["GET"],
            status_code=200,
            summary="Get details of a specific image"
        )
        
        self.add_api_route(
            "/{outlet_id}/promotions/{promotion_id}/images/{image_id}",
            self.score_image,
            methods=["POST"],
            status_code=201,
            summary="Submit a score for an image"
        )
        

    async def get_outlets(
        self,
        region: Optional[str] = Query(None, description="Filter outlets by region"),
        zone: Optional[str] = Query(None, description="Filter outlets by zone"),
        area: Optional[str] = Query(None, description="Filter outlets by area"),
        limit: int = Query(10, description="Limit the number of outlets returned"),
        offset: int = Query(0, description="Offset for pagination")
    ) -> OutletPaginationResponseModel:
        """
        Returns a list of outlets, filtered by Region, Zone, and/or Area if provided.
        Only outlets in the specified region, zone, or area will be returned.
        """
        total = 90
        outlets = [OutletResponseModel(outlet_id=str(i), outlet_name=f"Outlet {i}", region=f"Region {i}", zone=f"Zone {i}", area=f"Area {i}") for i in range(1, total + 1)]
        return OutletPaginationResponseModel(data=outlets[offset:offset+limit], total=total)
    
    async def get_outlet(self, outlet_id: str) -> OutletResponseModel:
        """
        Returns details of a specific outlet identified by outlet_id.
        """
        return OutletResponseModel(outlet_id=outlet_id, outlet_name=f"Outlet {outlet_id}", region=f"Region {outlet_id}", zone=f"Zone {outlet_id}", area=f"Area {outlet_id}")
    
    async def get_outlet_promotions(
        self, 
        outlet_id: str, 
        limit: int = Query(10, description="Limit the number of promotions returned"),
        offset: int = Query(0, description="Offset for pagination")
    ) -> PromotionByOutletPaginationResponseModel:
        """
        Returns a list of promotions available at the specified outlet.
        """
        total = 99
        promotions = [PromotionByOutletResponseModel(
            promotion_id=str(i), 
            promotion_name=f"Promotion {i}",
            outlet_id=outlet_id,
            validated_by_sa=False,
            validated_by_fa=False,
            total_photos=10
        ) for i in range(1, total + 1)]
        return PromotionByOutletPaginationResponseModel(data=promotions[offset:offset+limit], total=total, total_photos=total//10, total_promotions=total)
    
    async def get_outlet_promotion(self, outlet_id: int, promotion_id: int) -> PromotionByOutletResponseModel:
        """
        Returns details of a specific promotion for the given outlet.
        """
        return PromotionByOutletResponseModel(
            promotion_id=str(promotion_id),
            promotion_name=f"Promotion {promotion_id}",
            outlet_id=str(outlet_id),
            validated_by_sa=False,
            validated_by_fa=False,
            total_photos=100
        )
    
    async def get_promotion_images(
        self, 
        outlet_id: int, 
        promotion_id: int, 
        limit: int = Query(10, description="Limit the number of images returned"),
        offset: int = Query(0, description="Offset for pagination")
    ) -> List[ImageResponseModel]:
        """
        Returns a list of images associated with the specified promotion at the outlet.
        """
        total = 100
        images = [ImageResponseModel(
            image_id=str(i),
            upload_time=f"2024-01-01 {i}",
            sr_validation=ValidationStatus.UNVALIDATED,
            ai_validation=ValidationStatus.UNVALIDATED,
            sa_validation=ValidationStatus.UNVALIDATED,
            fa_validation=ValidationStatus.UNVALIDATED
        ) for i in range(1, total + 1)]
        return images[offset:offset+limit]
    
    async def get_promotion_image(self, outlet_id: int, promotion_id: int, image_id: int) -> ImageResponseModel:
        """
        Returns details of a specific image for the promotion at the outlet.
        """
        return ImageResponseModel(
            image_id=str(image_id),
            upload_time=f"2024-01-01 {image_id}",
            sr_validation=ValidationStatus.UNVALIDATED,
            ai_validation=ValidationStatus.UNVALIDATED,
            sa_validation=ValidationStatus.UNVALIDATED,
            fa_validation=ValidationStatus.UNVALIDATED
        )
    
    async def score_image(self, image_id: int, score_input: ScoreRequestModel) -> None:
        """
        Submits a score for the specified image associated with a promotion at an outlet.
        Request body expects a JSON object with a 'score' field (integer).
        """
        return None
    