from typing import Optional, List
import datetime
import uuid

from fastapi import APIRouter, Query

from enums.validation_status import ValidationStatus
from models import PromotionResponseModel, OutletResponseModel
from models.images.response_model import ImageResponseModel
from models.outlets.request_model import ScoreRequestModel
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
        
        self.add_api_route(
            "/{promotion_id}/outlets/{outlet_id}/images",
            self.get_promotion_images,
            methods=["GET"],
            status_code=200,
            summary="Get images for a specific promotion"
        )
        
        self.add_api_route(
            "/{promotion_id}/outlets/{outlet_id}/images/{image_id}",
            self.get_promotion_image,
            methods=["GET"],
            status_code=200,
            summary="Get details of a specific image"
        )
        
        self.add_api_route(
            "/{promotion_id}/outlets/{outlet_id}/images/{image_id}",
            self.score_image,
            methods=["POST"],
            status_code=201,
            summary="Submit a score for an image"
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
            area=f"Area {i}",
            sa_kpi_progress=0.8,
            fa_kpi_progress=0.8
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
            ai_validation_result=ValidationStatus.FAILED,
            is_validated_by_fa=True,
            is_validated_by_sa=False,
            total_photos=10
        ) for i in range(1, total + 1)]
        return OutletJoinedPromotionPaginationResponseModel(
            data=outlets[offset:offset+limit], 
            total=total,
            total_outlets=total,
            total_photos=total
        )
            
            
       
    async def get_promotion_images(
        self, 
        promotion_id: int, 
        outlet_id: int, 
        limit: int = Query(10, description="Limit the number of images returned"),
        offset: int = Query(0, description="Offset for pagination")
    ) -> List[ImageResponseModel]:
        """
        Returns a list of images associated with the specified promotion at the outlet.
        """
        total = 100
        images = [ImageResponseModel(
            image_id=str(i),
            upload_time=datetime.datetime.now(),
            uploader_id=f"{outlet_id}",
            uploader_name=uuid.uuid4().hex,
            sr_validation=ValidationStatus.UNVALIDATED,
            ai_validation=ValidationStatus.UNVALIDATED,
            sa_validation=ValidationStatus.UNVALIDATED,
            fa_validation=ValidationStatus.UNVALIDATED
        ) for i in range(1, total + 1)]
        return images[offset:offset+limit]
    
    async def get_promotion_image(self, promotion_id: int, outlet_id: int, image_id: int) -> ImageResponseModel:
        """
        Returns details of a specific image for the promotion at the outlet.
        """
        return ImageResponseModel(
            image_id=str(image_id),
            upload_time=datetime.datetime.now(),
            uploader_id=f"{outlet_id}",
            uploader_name=uuid.uuid4().hex,
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
    