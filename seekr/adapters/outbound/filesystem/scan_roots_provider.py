from pathlib import Path

from platformdirs import PlatformDirs

from seekr.application.ports.path_scanner import ScanRootsProvider
from seekr.domain.entities.scan import ScanRoot


class PlatformScanRootsProvider(ScanRootsProvider):
    def __init__(self, application_name: str = "seekr", company: str = "Pedroaba Tech"):
        self._dirs = PlatformDirs(application_name, company)

    def get(self) -> list[ScanRoot]:
        return [
            self._root(self._dirs.user_downloads_dir, "downloads"),
            self._root(self._dirs.user_documents_dir, "documents"),
            self._root(self._dirs.user_desktop_dir, "desktop"),
            self._root(self._dirs.user_pictures_dir, "pictures"),
            self._root(self._dirs.user_videos_dir, "videos"),
            self._root(self._dirs.user_music_dir, "music"),
        ]

    @staticmethod
    def _root(resource: str, alias: str) -> ScanRoot:
        return ScanRoot(resource=str(Path(resource).resolve()), alias=alias)
