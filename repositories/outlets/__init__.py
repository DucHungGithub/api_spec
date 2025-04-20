
from typing import Any, Dict, Optional
from sqlmodel import Session, select

from models.outlets.sql_model import Outlet, OutletCreate


class OutletRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create_outlet(self, outlet: OutletCreate) -> Outlet:
        db_outlet = Outlet.from_orm(outlet)
        self.session.add(db_outlet)
        self.session.commit()
        self.session.refresh(db_outlet)
        return db_outlet
    
    def get_outlet(self, outlet_id: str) -> Optional[Outlet]:
        return self.session.exec(
            select(Outlet).where(Outlet.outlet_id == outlet_id)
        ).first()
    
    def get_outlets(
        self,
        region: Optional[str] = None,
        area: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> Dict[str, Any]:
        query = select(Outlet)
        
        # Apply filters
        if region:
            query = query.where(Outlet.region == region)
        if area:
            query = query.where(Outlet.area == area)
            
        # Get total count
        total_query = select(Outlet)
        if region:
            total_query = total_query.where(Outlet.region == region)
        if area:
            total_query = total_query.where(Outlet.area == area)
            
        total = len(self.session.exec(total_query).all())
        
        # Apply pagination
        query = query.offset(offset).limit(limit)
        
        # Execute query
        outlets = self.session.exec(query).all()
        
        return {
            "data": outlets,
            "total": total
        }

