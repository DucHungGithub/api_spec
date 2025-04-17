from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel
from models.outlet_promotion.sql_model import OutletPromotion


class PromotionBase(SQLModel):
    promotion_name: str
    
class PromotionRead(PromotionBase):
    promotion_id: str
    
class PromotionCreate(PromotionBase):
    promotion_id: str


class Promotion(PromotionBase, table=True):
    """Database model for promotions"""
    __tablename__ = "promotions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    promotion_id: str = Field(index=True, unique=True)
    
    # Relationships
    outlet_promotions: List["OutletPromotion"] = Relationship(back_populates="promotion")