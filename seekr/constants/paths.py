from dataclasses import dataclass
from pathlib import Path

from seekr.config import SeekrConfig


@dataclass
class SeekrPath:
    path: Path
    name: str


class DefaultToScan:
    def __init__(self):
        self.__platformdirs = SeekrConfig.get_dirs()

        self.__default_paths = [
            SeekrPath(
                    Path(self.__platformdirs.user_downloads_dir), "download"),
            SeekrPath(
                    Path(self.__platformdirs.user_documents_dir), "documents"),
            SeekrPath(
                    Path(self.__platformdirs.user_desktop_dir), "desktop"),
            SeekrPath(
                    Path(self.__platformdirs.user_pictures_dir), "pictures"),
            SeekrPath(
                    Path(self.__platformdirs.user_videos_dir), "videos"),
            SeekrPath(
                    Path(self.__platformdirs.user_music_dir), "music")
        ]
