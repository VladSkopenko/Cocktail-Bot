from src.database.connect import session_maker
from src.repository.repo_banner import repository_add_banner_description
from src.common.text_for_db import description_for_info_pages
import asyncio

async def main():
    async with session_maker() as session:
        await repository_add_banner_description(session, description_for_info_pages)


if __name__ == "__main__":
    asyncio.run(main())
