"""Session-scoped paths for Allure results, screenshots, and videos (scalable per run)."""

from __future__ import annotations

import json
import os
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class AllureSessionPaths:
    session_id: str
    stamp: str
    folder_name: str
    session_root: Path
    allure_results: Path
    media: Path
    screenshots: Path
    videos: Path

    def to_manifest(self) -> dict:
        return {
            "session_id": self.session_id,
            "stamp": self.stamp,
            "folder_name": self.folder_name,
            "session_root": str(self.session_root.resolve()),
            "allure_results": str(self.allure_results.resolve()),
            "media": str(self.media.resolve()),
            "screenshots": str(self.screenshots.resolve()),
            "videos": str(self.videos.resolve()),
            "created_utc": datetime.now(timezone.utc).isoformat(),
        }


def build_session_paths(framework_root: Path) -> AllureSessionPaths:
    """
    Build a unique folder: common/reports/sessions/<session_id>_<YYYYMMDD_HHMMSS>/

    Override session id: env ALLURE_SESSION_ID (short string, filesystem-safe).
    """
    session_id = (os.environ.get("ALLURE_SESSION_ID") or uuid.uuid4().hex[:10]).strip()
    session_id = "".join(c if c.isalnum() or c in "-_" else "_" for c in session_id)[:32] or uuid.uuid4().hex[:10]
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"{session_id}_{stamp}"
    session_root = framework_root / "common" / "reports" / "sessions" / folder_name
    allure_results = session_root / "allure-results"
    media = session_root / "media"
    screenshots = media / "screenshots"
    videos = media / "videos"

    session_root.mkdir(parents=True, exist_ok=True)
    allure_results.mkdir(parents=True, exist_ok=True)
    media.mkdir(parents=True, exist_ok=True)
    screenshots.mkdir(parents=True, exist_ok=True)
    videos.mkdir(parents=True, exist_ok=True)

    paths = AllureSessionPaths(
        session_id=session_id,
        stamp=stamp,
        folder_name=folder_name,
        session_root=session_root,
        allure_results=allure_results,
        media=media,
        screenshots=screenshots,
        videos=videos,
    )

    manifest_path = session_root / "manifest.json"
    manifest_path.write_text(json.dumps(paths.to_manifest(), indent=2), encoding="utf-8")

    latest = framework_root / "common" / "reports" / "sessions" / "LATEST_SESSION.txt"
    latest.write_text(str(session_root.resolve()), encoding="utf-8")

    return paths


def read_latest_session_root(framework_root: Path) -> Path | None:
    latest = framework_root / "common" / "reports" / "sessions" / "LATEST_SESSION.txt"
    if not latest.is_file():
        return None
    p = Path(latest.read_text(encoding="utf-8").strip())
    return p if p.is_dir() else None


def safe_node_id(nodeid: str) -> str:
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in nodeid)[:200]
