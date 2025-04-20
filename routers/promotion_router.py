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
            "/{promotion_id}/outlets/{outlet_id}",
            self.get_promotion_outlet,
            methods=["GET"],
            status_code=200,
            summary="Get detail of a specific outlet of promotion"
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
        area: Optional[str] = Query(None, description="Filter promotions by area"),
        id: Optional[str] = Query(None, description="Filter promotions by id"),
        name: Optional[str] = Query(None, description="Filter promotions by name"),
        limit: int = Query(10, description="Limit the number of outlets returned"),
        offset: int = Query(0, description="Offset for pagination")
    ) -> PromotionPaginationResponseModel:
        """
        Returns a list of promotions, filtered by Region, and/or Area if provided.
        Only promotions available at outlets in the specified region, or area will be returned.
        """
        total = 100
        promotions = [PromotionResponseModel(
            promotion_id=str(i),
            promotion_name=f"Promotion {i}",
            region=f"Region {i}",
            area=f"Area {i}",
            sa_kpi_progress=0.8,
            fa_kpi_progress=0.8
        ) for i in range(1, total + 1)]
        return PromotionPaginationResponseModel(data=promotions[offset:offset+limit], total=total)
    
    
    async def get_promotion_outlets(
        self, 
        promotion_id: str, 
        validate_by_ai: Optional[ValidationStatus] = Query(None, description="Filter outlets validated by AI"),
        validate_by_sa: Optional[ValidationStatus] = Query(None, description="Filter outlets validated by SA"),
        validate_by_fa: Optional[ValidationStatus] = Query(None, description="Filter outlets validated by FA"),
        limit: int = Query(10, description="Limit the number of outlets returned"),
        offset: int = Query(0, description="Offset for pagination")
    ) -> OutletJoinedPromotionPaginationResponseModel:
        """
        Returns a list of outlets that offer the specified promotion.
        """
        total_outlets = 100
        outlets = [
            OutletJoinedPromotionResponseModel(
                outlet_id=str(i), 
                promotion_id=promotion_id,
                outlet_name=f"Outlet {i}", 
                region=f"Region {i}", 
                area=f"Area {i}",
                ai_validation_result=ValidationStatus.FAILED,
                fa_validated_result=ValidationStatus.PASSED,
                sa_validated_result=ValidationStatus.FAILED,
                total_photos=10
            ) for i in range(1, total_outlets + 1)
        ]
        
        outlets.extend([
            OutletJoinedPromotionResponseModel(
                outlet_id=str(i), 
                promotion_id=promotion_id,
                outlet_name=f"Outlet {i}", 
                region=f"Region {i}", 
                area=f"Area {i}",
                ai_validation_result=ValidationStatus.PASSED,
                fa_validated_result=ValidationStatus.FAILED,
                sa_validated_result=ValidationStatus.PASSED,
                total_photos=10
            ) for i in range(100, 150)
        ]) 
        
        outlets.extend([
            OutletJoinedPromotionResponseModel(
                outlet_id=str(i), 
                promotion_id=promotion_id,
                outlet_name=f"Outlet {i}", 
                region=f"Region {i}", 
                area=f"Area {i}",
                ai_validation_result=ValidationStatus.UNVALIDATED,
                fa_validated_result=ValidationStatus.FAILED,
                sa_validated_result=ValidationStatus.FAILED,
                total_photos=10
            ) for i in range(150, 200)
        ]) 

        # Apply filters
        if validate_by_ai is not None:
            outlets = [o for o in outlets if o.ai_validation_result == validate_by_ai]

        if validate_by_sa is not None:
            outlets = [o for o in outlets if o.sa_validated_result == validate_by_sa]
            
        if validate_by_fa is not None:
            outlets = [o for o in outlets if o.fa_validated_result == validate_by_fa]

        paginated_outlets = outlets[offset:offset + limit]
        total_photos = sum(o.total_photos for o in outlets)

        return OutletJoinedPromotionPaginationResponseModel(
            data=paginated_outlets, 
            total=len(outlets),
            total_outlets=len(outlets),
            total_photos=total_photos
        )
                
        
    async def get_promotion_outlet(
        self,
        promotion_id: str,
        outlet_id: str
    ) -> OutletJoinedPromotionResponseModel:
        return  OutletJoinedPromotionResponseModel(
                outlet_id=outlet_id, 
                promotion_id=promotion_id,
                outlet_name=f"Outlet sample", 
                region=f"Region sample", 
                area=f"Area Sample",
                ai_validation_result=ValidationStatus.FAILED,
                fa_validated_result=ValidationStatus.PASSED,
                sa_validated_result=ValidationStatus.FAILED,
                total_photos=10
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
    