from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.dashboard import Dashboard
from app.schemas.dashboard import DashboardCreate, DashboardUpdate


class CRUDDashboard(CRUDBase[Dashboard, DashboardCreate, DashboardUpdate]):
    """CRUD operations for Dashboard model."""
    
    async def create_with_user(
        self,
        db: AsyncSession,
        *,
        obj_in: DashboardCreate,
        user_id: int
    ) -> Dashboard:
        """Create dashboard with user ID."""
        obj_data = obj_in.model_dump(exclude_unset=True)
        obj_data["user_id"] = user_id
        
        # Convert widgets to dict if needed
        if "widgets" in obj_data and obj_data["widgets"]:
            obj_data["widgets"] = [
                w.model_dump() if hasattr(w, "model_dump") else w
                for w in obj_data["widgets"]
            ]
        
        db_obj = Dashboard(**obj_data)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    async def get_by_user(
        self,
        db: AsyncSession,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dashboard]:
        """Get dashboards by user."""
        query = (
            select(Dashboard)
            .where(Dashboard.user_id == user_id)
            .order_by(Dashboard.is_default.desc(), Dashboard.name.asc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_default(
        self,
        db: AsyncSession,
        *,
        user_id: int
    ) -> Optional[Dashboard]:
        """Get user's default dashboard."""
        query = (
            select(Dashboard)
            .where(
                Dashboard.user_id == user_id,
                Dashboard.is_default == True
            )
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_public(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dashboard]:
        """Get public dashboards."""
        query = (
            select(Dashboard)
            .where(Dashboard.is_public == True)
            .order_by(Dashboard.name.asc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def set_default(
        self,
        db: AsyncSession,
        *,
        dashboard_id: int,
        user_id: int
    ) -> Optional[Dashboard]:
        """Set a dashboard as default, unsetting any previous default."""
        # Unset current default
        current_default = await self.get_default(db, user_id=user_id)
        if current_default and current_default.id != dashboard_id:
            current_default.is_default = False
            db.add(current_default)
        
        # Set new default
        dashboard = await self.get(db, dashboard_id)
        if not dashboard or dashboard.user_id != user_id:
            return None
        
        dashboard.is_default = True
        db.add(dashboard)
        await db.flush()
        await db.refresh(dashboard)
        return dashboard
    
    async def duplicate(
        self,
        db: AsyncSession,
        *,
        dashboard_id: int,
        user_id: int,
        new_name: str
    ) -> Optional[Dashboard]:
        """Duplicate a dashboard."""
        original = await self.get(db, dashboard_id)
        if not original:
            return None
        
        new_dashboard = Dashboard(
            name=new_name,
            description=original.description,
            layout=original.layout,
            widgets=original.widgets,
            filters=original.filters,
            refresh_interval=original.refresh_interval,
            is_default=False,
            is_public=False,
            user_id=user_id
        )
        
        db.add(new_dashboard)
        await db.flush()
        await db.refresh(new_dashboard)
        return new_dashboard
    
    async def update_widgets(
        self,
        db: AsyncSession,
        *,
        dashboard_id: int,
        widgets: list
    ) -> Optional[Dashboard]:
        """Update dashboard widgets."""
        dashboard = await self.get(db, dashboard_id)
        if not dashboard:
            return None
        
        dashboard.widgets = widgets
        db.add(dashboard)
        await db.flush()
        await db.refresh(dashboard)
        return dashboard
    
    async def update_layout(
        self,
        db: AsyncSession,
        *,
        dashboard_id: int,
        layout: dict
    ) -> Optional[Dashboard]:
        """Update dashboard layout."""
        dashboard = await self.get(db, dashboard_id)
        if not dashboard:
            return None
        
        dashboard.layout = layout
        db.add(dashboard)
        await db.flush()
        await db.refresh(dashboard)
        return dashboard


# Create singleton instance
dashboard = CRUDDashboard(Dashboard)
