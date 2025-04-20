from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

from models.outlet_promotion.sql_model import OutletPromotion


class OutletBase(SQLModel):
    outlet_name: str
    region: str
    area: str
    
class OutletRead(OutletBase):
    outlet_id: str
    
class OutletCreate(OutletBase):
    outlet_id: str


class Outlet(OutletBase, table=True):
    """Database model for outlets"""
    __tablename__ = "outlets"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    outlet_id: str = Field(index=True, unique=True)
    
    # Relationships
    promotions: List["OutletPromotion"] = Relationship(back_populates="outlet")