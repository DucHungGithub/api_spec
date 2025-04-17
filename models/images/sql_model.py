from typing import Optional
from datetime import datetime


from enums.validation_status import ValidationStatus
from models.outlet_promotion.sql_model import OutletPromotion

from sqlmodel import Field, SQLModel, Relationship


class ScoreUpdate(SQLModel):
    sr_validation: ValidationStatus
    ai_validation: ValidationStatus
    sa_validation: ValidationStatus
    fa_validation: ValidationStatus

class ImageBase(SQLModel):
    upload_time: datetime = Field(default_factory=datetime.utcnow)
    sr_validation: ValidationStatus = ValidationStatus.UNVALIDATED
    ai_validation: ValidationStatus = ValidationStatus.UNVALIDATED
    sa_validation: ValidationStatus = ValidationStatus.UNVALIDATED
    fa_validation: ValidationStatus = ValidationStatus.UNVALIDATED

class ImageRead(ImageBase):
    image_id: str


class ImageCreate(ImageBase):
    outlet_id: str
    promotion_id: str
    file_path: str
    
class Image(ImageBase, table=True):
    """Database model for promotion images"""
    __tablename__ = "images"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    image_id: str = Field(index=True, unique=True)
    outlet_promotion_id: int = Field(foreign_key="outlet_promotions.id", index=True)
    file_path: str
    
    # Relationships
    outlet_promotion: OutletPromotion = Relationship(back_populates="images")


