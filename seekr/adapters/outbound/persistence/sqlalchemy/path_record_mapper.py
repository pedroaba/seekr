from seekr.adapters.outbound.persistence.sqlalchemy.models import PathRecord
from seekr.domain.entities.indexed_path import IndexedPath


class PathRecordMapper:
    @staticmethod
    def from_indexed_path(path: IndexedPath) -> PathRecord:
        return PathRecord(
            filepath=path.filepath,
            parent_path=path.parent_path,
            normalized_filepath=path.normalized_filepath,
            is_folder=path.is_folder,
            is_file=path.is_file,
            is_able_to_watch=path.is_able_to_watch,
            modified_path_at=path.modified_path_at,
            modified_content_at=path.modified_content_at,
            version=path.version,
        )

    @staticmethod
    def to_indexed_path(record: PathRecord) -> IndexedPath:
        return IndexedPath(
            filepath=record.filepath,
            parent_path=record.parent_path,
            normalized_filepath=record.normalized_filepath,
            is_folder=record.is_folder,
            is_file=record.is_file,
            is_able_to_watch=record.is_able_to_watch,
            modified_path_at=record.modified_path_at,
            modified_content_at=record.modified_content_at,
            version=record.version,
        )
