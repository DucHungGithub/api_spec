from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from models.outlets.sql_model import Outlet
from models.promotions.sql_model import Promotion
from models.images.sql_model import Image


class OutletPromotionBase(SQLModel):
    validated_by_sa: bool = False
    validated_by_fa: bool = False
    
class OutletPromotionRead(OutletPromotionBase):
    promotion_id: str
    outlet_id: str
    promotion_name: str
    total_photos: int
    
    
class OutletPromotionCreate(OutletPromotionBase):
    outlet_id: str
    promotion_id: str


class OutletPromotion(OutletPromotionBase, table=True):
    """Junction table for outlet-promotion relationship"""
    __tablename__ = "outlet_promotions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    outlet_id: int = Field(foreign_key="outlets.id", index=True)
    promotion_id: int = Field(foreign_key="promotions.id", index=True)
    
    # Relationships
    outlet: Outlet = Relationship(back_populates="promotions")
    promotion: Promotion = Relationship(back_populates="outlet_promotions")
    images: List["Image"] = Relationship(back_populates="outlet_promotion")
    
    @property
    def total_photos(self) -> int:
        return len(self.images)


