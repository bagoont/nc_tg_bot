from sqlalchemy import select

from bot.db.models import User
from bot.db.repositories import Repository


class UserRepository(Repository[User]):
    model = User

    async def get_by_tg_id(self, tg_id: int) -> User | None:
        statement = select(self.model).where(self.model.tg_id == tg_id)
        result = await self.session.execute(statement)
        return result.unique().scalar()
