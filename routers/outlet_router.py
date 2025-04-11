from typing import Optional, List

from fastapi import APIRouter, Query

from models import ScoreRequestModel, OutletResponseModel, PromotionResponseModel, ImageResponseModel




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
        area: Optional[str] = Query(None, description="Filter outlets by area")
    ) -> List[OutletResponseModel]:
        """
        Returns a list of outlets, filtered by Region, Zone, and/or Area if provided.
        Only outlets in the specified region, zone, or area will be returned.
        """
        pass
    
    async def get_outlet(self, outlet_id: str) -> OutletResponseModel:
        """
        Returns details of a specific outlet identified by outlet_id.
        """
        pass
    
    async def get_outlet_promotions(self, outlet_id: str) -> List[PromotionResponseModel]:
        """
        Returns a list of promotions available at the specified outlet.
        """
        pass
    
    async def get_outlet_promotion(self, outlet_id: int, promotion_id: int) -> PromotionResponseModel:
        """
        Returns details of a specific promotion for the given outlet.
        """
        pass
    
    async def get_promotion_images(self, outlet_id: int, promotion_id: int) -> List[ImageResponseModel]:
        """
        Returns a list of images associated with the specified promotion at the outlet.
        """
        pass
    
    async def get_promotion_image(self, outlet_id: int, promotion_id: int, image_id: int) -> ImageResponseModel:
        """
        Returns details of a specific image for the promotion at the outlet.
        """
        pass
    
    async def score_image(self, outlet_id: int, promotion_id: int, image_id: int, score_input: ScoreRequestModel) -> None:
        """
        Submits a score for the specified image associated with a promotion at an outlet.
        Request body expects a JSON object with a 'score' field (integer).
        """
        pass
    