from pathlib import Path
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
        
        self.outlets = [
            {
                "outlet_id": "outlet1",
                "outlet_name": "Downtown Flagship Store",
                "region": "North",
                "zone": "Urban",
                "area": "Downtown"
            },
            {
                "outlet_id": "outlet2",
                "outlet_name": "Urban Center Store",
                "region": "North",
                "zone": "Urban",
                "area": "Downtown"
            },
            {
                "outlet_id": "outlet3",
                "outlet_name": "South Mall Store",
                "region": "South",
                "zone": "Urban",
                "area": "Mall"
            },
            {
                "outlet_id": "outlet4",
                "outlet_name": "East Plaza Store",
                "region": "East",
                "zone": "Suburban",
                "area": "Plaza"
            },
            {
                "outlet_id": "outlet5",
                "outlet_name": "West Rural Store",
                "region": "West",
                "zone": "Rural",
                "area": "Main Street"
            }
        ]
        
        # Mock promotions by outlet
        self.promotions_by_outlet = {
            "outlet1": [
                {
                    "promotion_id": "promo1",
                    "promotion_name": "Summer Sale 2025",
                    "outlet_id": "outlet1",
                    "validated_by_sa": True,
                    "validated_by_fa": False,
                    "total_photos": 2
                },
                {
                    "promotion_id": "promo2",
                    "promotion_name": "Spring Collection Launch",
                    "outlet_id": "outlet1",
                    "validated_by_sa": False,
                    "validated_by_fa": False,
                    "total_photos": 1
                },
                {
                    "promotion_id": "promo4",
                    "promotion_name": "Weekend Discount",
                    "outlet_id": "outlet1",
                    "validated_by_sa": True,
                    "validated_by_fa": True,
                    "total_photos": 1
                }
            ],
            "outlet2": [
                {
                    "promotion_id": "promo1",
                    "promotion_name": "Summer Sale 2025",
                    "outlet_id": "outlet2",
                    "validated_by_sa": False,
                    "validated_by_fa": False,
                    "total_photos": 1
                },
                {
                    "promotion_id": "promo3",
                    "promotion_name": "Holiday Special",
                    "outlet_id": "outlet2",
                    "validated_by_sa": True,
                    "validated_by_fa": False,
                    "total_photos": 1
                }
            ],
            "outlet3": [
                {
                    "promotion_id": "promo2",
                    "promotion_name": "Spring Collection Launch",
                    "outlet_id": "outlet3",
                    "validated_by_sa": False,
                    "validated_by_fa": False,
                    "total_photos": 1
                },
                {
                    "promotion_id": "promo5",
                    "promotion_name": "Clearance Sale",
                    "outlet_id": "outlet3",
                    "validated_by_sa": True,
                    "validated_by_fa": True,
                    "total_photos": 1
                }
            ],
            "outlet4": [
                {
                    "promotion_id": "promo3",
                    "promotion_name": "Holiday Special",
                    "outlet_id": "outlet4",
                    "validated_by_sa": False,
                    "validated_by_fa": False,
                    "total_photos": 1
                }
            ],
            "outlet5": [
                {
                    "promotion_id": "promo4",
                    "promotion_name": "Weekend Discount",
                    "outlet_id": "outlet5",
                    "validated_by_sa": False,
                    "validated_by_fa": False,
                    "total_photos": 1
                }
            ]
        }
        
        # Mock images data
        self.images_by_promotion = {
            "outlet1_promo1": [
                {
                    "image_id": "img1",
                    "upload_time": "2025-04-01T10:00:00Z",
                    "sr_validation": ValidationStatus.PASSED,
                    "ai_validation": ValidationStatus.PASSED,
                    "sa_validation": ValidationStatus.PASSED,
                    "fa_validation": ValidationStatus.UNVALIDATED
                },
                {
                    "image_id": "img2",
                    "upload_time": "2025-04-01T11:30:00Z",
                    "sr_validation": ValidationStatus.PASSED,
                    "ai_validation": ValidationStatus.FAILED,
                    "sa_validation": ValidationStatus.PASSED,
                    "fa_validation": ValidationStatus.UNVALIDATED
                }
            ],
            "outlet1_promo2": [
                {
                    "image_id": "img4",
                    "upload_time": "2025-04-02T09:15:00Z",
                    "sr_validation": ValidationStatus.PASSED,
                    "ai_validation": ValidationStatus.PASSED,
                    "sa_validation": ValidationStatus.UNVALIDATED,
                    "fa_validation": ValidationStatus.UNVALIDATED
                }
            ],
            "outlet1_promo4": [
                {
                    "image_id": "img8",
                    "upload_time": "2025-04-05T14:20:00Z",
                    "sr_validation": ValidationStatus.PASSED,
                    "ai_validation": ValidationStatus.PASSED,
                    "sa_validation": ValidationStatus.PASSED,
                    "fa_validation": ValidationStatus.PASSED
                }
            ],
            "outlet2_promo1": [
                {
                    "image_id": "img3",
                    "upload_time": "2025-04-01T13:45:00Z",
                    "sr_validation": ValidationStatus.PASSED,
                    "ai_validation": ValidationStatus.PASSED,
                    "sa_validation": ValidationStatus.UNVALIDATED,
                    "fa_validation": ValidationStatus.UNVALIDATED
                }
            ],
            "outlet2_promo3": [
                {
                    "image_id": "img6",
                    "upload_time": "2025-04-03T16:30:00Z",
                    "sr_validation": ValidationStatus.PASSED,
                    "ai_validation": ValidationStatus.PASSED,
                    "sa_validation": ValidationStatus.PASSED,
                    "fa_validation": ValidationStatus.UNVALIDATED
                }
            ],
            "outlet3_promo2": [
                {
                    "image_id": "img5",
                    "upload_time": "2025-04-02T11:00:00Z",
                    "sr_validation": ValidationStatus.PASSED,
                    "ai_validation": ValidationStatus.PASSED,
                    "sa_validation": ValidationStatus.UNVALIDATED,
                    "fa_validation": ValidationStatus.UNVALIDATED
                }
            ],
            "outlet3_promo5": [
                {
                    "image_id": "img10",
                    "upload_time": "2025-04-10T10:45:00Z",
                    "sr_validation": ValidationStatus.PASSED,
                    "ai_validation": ValidationStatus.PASSED,
                    "sa_validation": ValidationStatus.PASSED,
                    "fa_validation": ValidationStatus.PASSED
                }
            ],
            "outlet4_promo3": [
                {
                    "image_id": "img7",
                    "upload_time": "2025-04-04T09:30:00Z",
                    "sr_validation": ValidationStatus.PASSED,
                    "ai_validation": ValidationStatus.PASSED,
                    "sa_validation": ValidationStatus.UNVALIDATED,
                    "fa_validation": ValidationStatus.UNVALIDATED
                }
            ],
            "outlet5_promo4": [
                {
                    "image_id": "img9",
                    "upload_time": "2025-04-08T15:20:00Z",
                    "sr_validation": ValidationStatus.PASSED,
                    "ai_validation": ValidationStatus.PASSED,
                    "sa_validation": ValidationStatus.UNVALIDATED,
                    "fa_validation": ValidationStatus.UNVALIDATED
                }
            ]
        }
        
        
        

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
        filtered_outlets = self.outlets
        
        if region:
            filtered_outlets = [o for o in filtered_outlets if o["region"] == region]
        
        if zone:
            filtered_outlets = [o for o in filtered_outlets if o["zone"] == zone]
        
        if area:
            filtered_outlets = [o for o in filtered_outlets if o["area"] == area]
        
        # Apply pagination
        paginated_outlets = filtered_outlets[offset:offset+limit]
        
        # Convert to response model format
        result_data = [OutletResponseModel(**o) for o in paginated_outlets]
        
        return OutletPaginationResponseModel(
            data=result_data,
            total=len(filtered_outlets)
        )
    
    async def get_outlet(self, outlet_id: str) -> OutletResponseModel:
        """
        Returns details of a specific outlet identified by outlet_id.
        """
        outlet_id = "outlet4"
        for outlet in self.outlets:
            if outlet["outlet_id"] == outlet_id:
                return OutletResponseModel(**outlet)
        
        # If outlet not found, would typically raise a 404 error
        # For mock purposes, return a placeholder
        return OutletResponseModel(
            outlet_id="not_found",
            outlet_name="Outlet Not Found",
            region="Unknown",
            zone="Unknown",
            area="Unknown"
        )
    
    async def get_outlet_promotions(self, outlet_id: str) -> PromotionByOutletPaginationResponseModel:
        """
        Returns a list of promotions available at the specified outlet.
        """
        if outlet_id not in self.promotions_by_outlet:
            # Return empty result if outlet not found
            return PromotionByOutletPaginationResponseModel(
                data=[],
                total=0,
                total_promotions=0,
                total_photos=0
            )
        
        promotions = self.promotions_by_outlet[outlet_id]
        total_photos = sum(promo["total_photos"] for promo in promotions)
        
        # Convert to response model format
        result_data = [PromotionByOutletResponseModel(**p) for p in promotions]
        
        return PromotionByOutletPaginationResponseModel(
            data=result_data,
            total=len(promotions),
            total_promotions=len(promotions),
            total_photos=total_photos
        )
    
    async def get_outlet_promotion(self, outlet_id: str, promotion_id: str) -> PromotionByOutletResponseModel:
        """
        Returns details of a specific promotion for the given outlet.
        """
        str_outlet_id = outlet_id
        str_promotion_id = promotion_id
        
        if str_outlet_id not in self.promotions_by_outlet:
            # Return placeholder if outlet not found
            return PromotionByOutletResponseModel(
                promotion_id="not_found",
                promotion_name="Promotion Not Found",
                outlet_id=str_outlet_id,
                validated_by_sa=False,
                validated_by_fa=False,
                total_photos=0
            )
        
        # Find the specific promotion
        for promotion in self.promotions_by_outlet[str_outlet_id]:
            if promotion["promotion_id"] == str_promotion_id:
                return PromotionByOutletResponseModel(**promotion)
        
        # Return placeholder if promotion not found
        return PromotionByOutletResponseModel(
            promotion_id="not_found",
            promotion_name="Promotion Not Found",
            outlet_id=str_outlet_id,
            validated_by_sa=False,
            validated_by_fa=False,
            total_photos=0
        )
    
    async def get_promotion_images(self, outlet_id: str, promotion_id: str) -> List[ImageResponseModel]:
        """
        Returns a list of images associated with the specified promotion at the outlet.
        """
        str_outlet_id = outlet_id
        str_promotion_id = promotion_id
        
        # Create key for images lookup
        key = f"{str_outlet_id}_{str_promotion_id}"
        
        if key not in self.images_by_promotion:
            # Return empty list if no images found
            return []
        
        # Convert to response model format
        return [ImageResponseModel(**img) for img in self.images_by_promotion[key]]
    
    async def get_promotion_image(self, outlet_id: int, promotion_id: int, image_id: int) -> ImageResponseModel:
        """
        Returns details of a specific image for the promotion at the outlet.
        """
        str_outlet_id = f"outlet{outlet_id}"
        str_promotion_id = f"promo{promotion_id}"
        str_image_id = f"img{image_id}"
        
        # Create key for images lookup
        key = f"{str_outlet_id}_{str_promotion_id}"
        
        if key not in self.images_by_promotion:
            # Return placeholder if no images found for this promotion/outlet
            return ImageResponseModel(
                image_id="not_found",
                upload_time="2025-01-01T00:00:00Z",
                sr_validation=ValidationStatus.UNVALIDATED,
                ai_validation=ValidationStatus.UNVALIDATED,
                sa_validation=ValidationStatus.UNVALIDATED,
                fa_validation=ValidationStatus.UNVALIDATED
            )
        
        # Find the specific image
        for image in self.images_by_promotion[key]:
            if image["image_id"] == str_image_id:
                return ImageResponseModel(**image)
        
        # Return placeholder if image not found
        return ImageResponseModel(
            image_id="not_found",
            upload_time="2025-01-01T00:00:00Z",
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
        return
    
        