from dataclasses import dataclass
from typing import Any, Sequence

from sqlalchemy import Row

from app.src.infrastructure.database.models import User


@dataclass
class RatingDTO:
	users: Sequence[Row[tuple[User]]]
	from_user_place: int | str = 0
	from_user_count: int | str = 0


