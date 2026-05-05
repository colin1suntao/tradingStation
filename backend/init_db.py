import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.database import Base
from app.core.config import get_settings
from app.models.master import Exchange, DataSource

async def init_db():
    settings = get_settings()
    engine = create_async_engine(settings.database_url)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())
