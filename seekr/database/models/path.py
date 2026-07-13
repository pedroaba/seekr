from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from seekr.database.models.base import BaseModel


class PathModel(BaseModel):
    __tablename__ = "paths"

    filepath: Mapped[str]
    parent_path: Mapped[str]

    normalized_filepath: Mapped[str]

    is_folder: Mapped[bool]
    is_file: Mapped[bool]

    is_able_to_watch: Mapped[bool] = mapped_column(default=True)

    modified_path_at: Mapped[datetime] = mapped_column(default=datetime.now)
    modified_content_at: Mapped[datetime] = mapped_column(default=datetime.now)

    version: Mapped[int]
