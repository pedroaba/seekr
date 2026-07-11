from pathlib import Path

from seekr.config import SeekrConfig
from seekr.models.path import PathModel


class DefaultToScan:
    def __init__(self):
        self.__platformdirs = SeekrConfig.get_dirs()

        self.__default_paths = [
            PathModel(
                resource=str(Path(self.__platformdirs.user_downloads_dir).resolve()),
                is_system_path=True,
                path_alias="downloads",
            ),
            PathModel(
                resource=str(Path(self.__platformdirs.user_documents_dir).resolve()),
                is_system_path=True,
                path_alias="documents",
            ),
            PathModel(
                resource=str(Path(self.__platformdirs.user_desktop_dir).resolve()),
                is_system_path=True,
                path_alias="desktop",
            ),
            PathModel(
                resource=str(Path(self.__platformdirs.user_pictures_dir).resolve()),
                is_system_path=True,
                path_alias="pictures",
            ),
            PathModel(
                resource=str(Path(self.__platformdirs.user_videos_dir).resolve()),
                is_system_path=True,
                path_alias="videos",
            ),
            PathModel(
                resource=str(Path(self.__platformdirs.user_music_dir).resolve()),
                is_system_path=True,
                path_alias="music",
            ),
        ]
