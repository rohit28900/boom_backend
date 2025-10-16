from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.database import get_session  # your DB dependency
from src.modules.orders.models import Order  # example table

class ExportRepository:
    async def get_data_by_date_range(self, start_date: datetime, end_date: datetime):
        async with get_session() as session:  # type: AsyncSession
            query = select(Order).where(Order.created_at >= start_date, Order.created_at <= end_date)
            result = await session.execute(query)
            return result.scalars().all()
