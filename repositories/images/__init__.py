from typing import List, Optional, Dict, Any
from sqlmodel import Session, select, or_, and_

from models.images.sql_model import Image, ImageCreate, ScoreUpdate
from models.outlet_promotion.sql_model import OutletPromotion
from models.outlets.sql_model import Outlet
from models.promotions.sql_model import Promotion



class ImageRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create_image(self, image: ImageCreate) -> Image:
        # Get outlet and promotion
        outlet = self.session.exec(
            select(Outlet).where(Outlet.outlet_id == image.outlet_id)
        ).first()
        
        promotion = self.session.exec(
            select(Promotion).where(Promotion.promotion_id == image.promotion_id)
        ).first()
        
        if not outlet or not promotion:
            raise ValueError("Outlet or Promotion not found")
        
        # Get outlet_promotion
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
            raise ValueError("Outlet-Promotion relationship not found")
        
        # Generate image_id (in production, use UUID or other unique identifier)
        import uuid
        image_id = f"img_{uuid.uuid4().hex[:8]}"
        
        # Create the image record
        db_image = Image(
            image_id=image_id,
            outlet_promotion_id=outlet_promotion.id,
            upload_time=image.upload_time,
            sr_validation=image.sr_validation,
            ai_validation=image.ai_validation,
            sa_validation=image.sa_validation,
            fa_validation=image.fa_validation,
            file_path=image.file_path
        )
        
        self.session.add(db_image)
        self.session.commit()
        self.session.refresh(db_image)
        return db_image
    
    def get_promotion_images(self, outlet_id: str, promotion_id: str) -> List[Image]:
        # Get outlet and promotion
        outlet = self.session.exec(
            select(Outlet).where(Outlet.outlet_id == outlet_id)
        ).first()
        
        promotion = self.session.exec(
            select(Promotion).where(Promotion.promotion_id == promotion_id)
        ).first()
        
        if not outlet or not promotion:
            return []
        
        # Get outlet_promotion
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
            return []
        
        # Get images
        images = self.session.exec(
            select(Image).where(Image.outlet_promotion_id == outlet_promotion.id)
        ).all()
        
        return images
    
    def get_promotion_image(self, outlet_id: str, promotion_id: str, image_id: str) -> Optional[Image]:
        # Get outlet and promotion
        outlet = self.session.exec(
            select(Outlet).where(Outlet.outlet_id == outlet_id)
        ).first()
        
        promotion = self.session.exec(
            select(Promotion).where(Promotion.promotion_id == promotion_id)
        ).first()
        
        if not outlet or not promotion:
            return None
        
        # Get outlet_promotion
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
        
        # Get specific image
        image = self.session.exec(
            select(Image)
            .where(
                and_(
                    Image.outlet_promotion_id == outlet_promotion.id,
                    Image.image_id == image_id
                )
            )
        ).first()
        
        return image
    
    def score_image(self, outlet_id: str, promotion_id: str, image_id: str, score: ScoreUpdate) -> Optional[Image]:
        # Get the image
        image = self.get_promotion_image(outlet_id, promotion_id, image_id)
        
        if not image:
            return None
        
        # Update validation scores
        image.sr_validation = score.sr_validation
        image.ai_validation = score.ai_validation
        image.sa_validation = score.sa_validation
        image.fa_validation = score.fa_validation
        
        # Check if we need to update promotion validation status
        outlet_promotion = image.outlet_promotion
        
        # Get all images for this outlet_promotion
        all_images = self.session.exec(
            select(Image).where(Image.outlet_promotion_id == outlet_promotion.id)
        ).all()
        
        # Check if all images have SA validation
        outlet_promotion.validated_by_sa = all(img.sa_validation == "PASSED" for img in all_images)
        
        # Check if all images have FA validation
        outlet_promotion.validated_by_fa = all(img.fa_validation == "PASSED" for img in all_images)
        
        # Commit changes
        self.session.commit()
        self.session.refresh(image)
        
        return image