from typing import List, Optional, Dict, Any
from sqlmodel import Session, select, or_, and_

from models.images.sql_model import Image
from models.outlet_promotion.sql_model import OutletPromotion, OutletPromotionCreate
from models.outlets.sql_model import Outlet
from models.promotions.sql_model import Promotion


class OutletPromotionRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create_outlet_promotion(self, outlet_promotion: OutletPromotionCreate) -> OutletPromotion:
        # Get outlet and promotion IDs
        outlet = self.session.exec(
            select(Outlet).where(Outlet.outlet_id == outlet_promotion.outlet_id)
        ).first()
        
        promotion = self.session.exec(
            select(Promotion).where(Promotion.promotion_id == outlet_promotion.promotion_id)
        ).first()
        
        if not outlet or not promotion:
            raise ValueError("Outlet or Promotion not found")
        
        # Create the outlet_promotion record
        db_outlet_promotion = OutletPromotion(
            outlet_id=outlet.id,
            promotion_id=promotion.id,
            validated_by_sa=outlet_promotion.validated_by_sa,
            validated_by_fa=outlet_promotion.validated_by_fa
        )
        
        self.session.add(db_outlet_promotion)
        self.session.commit()
        self.session.refresh(db_outlet_promotion)
        return db_outlet_promotion
    
    def get_outlet_promotions(self, outlet_id: str) -> Dict[str, Any]:
        # Get the outlet
        outlet = self.session.exec(
            select(Outlet).where(Outlet.outlet_id == outlet_id)
        ).first()
        
        if not outlet:
            return {
                "data": [],
                "total": 0,
                "total_promotions": 0,
                "total_photos": 0
            }
        
        # Get promotions for this outlet
        query = (
            select(OutletPromotion, Promotion)
            .join(Promotion)
            .where(OutletPromotion.outlet_id == outlet.id)
        )
        
        results = self.session.exec(query).all()
        
        total_photos = 0
        promotions_data = []
        
        for outlet_promotion, promotion in results:
            # Get image count
            images_query = select(Image).where(Image.outlet_promotion_id == outlet_promotion.id)
            image_count = len(self.session.exec(images_query).all())
            total_photos += image_count
            
            promotion_data = {
                "promotion_id": promotion.promotion_id,
                "promotion_name": promotion.promotion_name,
                "outlet_id": outlet_id,
                "validated_by_sa": outlet_promotion.validated_by_sa,
                "validated_by_fa": outlet_promotion.validated_by_fa,
                "total_photos": image_count
            }
            promotions_data.append(promotion_data)
        
        return {
            "data": promotions_data,
            "total": len(promotions_data),
            "total_promotions": len(promotions_data),
            "total_photos": total_photos
        }
    
    def get_outlet_promotion(self, outlet_id: str, promotion_id: str) -> Optional[Dict[str, Any]]:
        # Get outlet and promotion
        outlet = self.session.exec(
            select(Outlet).where(Outlet.outlet_id == outlet_id)
        ).first()
        
        promotion = self.session.exec(
            select(Promotion).where(Promotion.promotion_id == promotion_id)
        ).first()
        
        if not outlet or not promotion:
            return None
        
        # Get the specific outlet_promotion
        outlet_promotion = self.session.exec(
            select(OutletPromotion)
            .where(
                and_(
                    OutletPromotion.outlet_id == outlet.id,
                    OutletPromotion.promotion_id == promotion.id
                )
            )
        ).first()
        
        if not outlet_promotion:
            return None
        
        # Get image count
        images_query = select(Image).where(Image.outlet_promotion_id == outlet_promotion.id)
        image_count = len(self.session.exec(images_query).all())
        
        return {
            "promotion_id": promotion.promotion_id,
            "promotion_name": promotion.promotion_name,
            "outlet_id": outlet.outlet_id,
            "validated_by_sa": outlet_promotion.validated_by_sa,
            "validated_by_fa": outlet_promotion.validated_by_fa,
            "total_photos": image_count
        }

