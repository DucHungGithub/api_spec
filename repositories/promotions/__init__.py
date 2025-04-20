
from typing import Any, Dict, Optional
from sqlmodel import Session, or_, select
from models.images.sql_model import Image
from models.outlet_promotion.sql_model import OutletPromotion
from models.outlets.sql_model import Outlet
from models.promotions.sql_model import Promotion, PromotionCreate


class PromotionRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create_promotion(self, promotion: PromotionCreate) -> Promotion:
        db_promotion = Promotion.from_orm(promotion)
        self.session.add(db_promotion)
        self.session.commit()
        self.session.refresh(db_promotion)
        return db_promotion
    
    def get_promotion(self, promotion_id: str) -> Optional[Promotion]:
        return self.session.exec(
            select(Promotion).where(Promotion.promotion_id == promotion_id)
        ).first()
    
    def get_promotions(
        self,
        region: Optional[str] = None,
        area: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> Dict[str, Any]:
        query = (
            select(Promotion)
            .join(OutletPromotion)
            .join(Outlet)
        )
        
        # Apply filters
        conditions = []
        if region:
            conditions.append(Outlet.region == region)
        if area:
            conditions.append(Outlet.area == area)
        
        if conditions:
            query = query.where(or_(*conditions))
            
        # Get distinct promotions
        query = query.distinct()
        
        # Get total count
        total_query = (
            select(Promotion)
            .join(OutletPromotion)
            .join(Outlet)
        )
        if conditions:
            total_query = total_query.where(or_(*conditions))
        total_query = total_query.distinct()
        
        total = len(self.session.exec(total_query).all())
        
        # Apply pagination
        query = query.offset(offset).limit(limit)
        
        # Execute query
        promotions = self.session.exec(query).all()
        
        return {
            "data": promotions,
            "total": total
        }
    
    def get_promotion_outlets(self, promotion_id: str) -> Dict[str, Any]:
        # Get the promotion
        promotion = self.get_promotion(promotion_id)
        if not promotion:
            return {
                "data": [],
                "total": 0,
                "total_outlets": 0,
                "total_photos": 0
            }
        
        # Get outlets with this promotion
        query = (
            select(Outlet, OutletPromotion)
            .join(OutletPromotion)
            .join(Promotion)
            .where(Promotion.promotion_id == promotion_id)
        )
        
        results = self.session.exec(query).all()
        
        # Count photos for this promotion
        total_photos = 0
        outlet_promotions = []
        
        for outlet, outlet_promotion in results:
            # Get image count for this outlet-promotion
            images_query = select(Image).where(Image.outlet_promotion_id == outlet_promotion.id)
            image_count = len(self.session.exec(images_query).all())
            total_photos += image_count
            
            outlet_promotion_data = {
                "outlet_id": outlet.outlet_id,
                "outlet_name": outlet.outlet_name,
                "promotion_id": promotion_id,
                "region": outlet.region,
                "area": outlet.area,
                "total_photos": image_count
            }
            outlet_promotions.append(outlet_promotion_data)
        
        return {
            "data": outlet_promotions,
            "total": len(outlet_promotions),
            "total_outlets": len(outlet_promotions),
            "total_photos": total_photos
        }

