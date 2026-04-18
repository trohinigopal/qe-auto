from __future__ import annotations

from typing import Any

import requests


class ApiBaseClient:
    def __init__(self, base_url: str, timeout: int = 30, lazy: bool = False) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session() if not lazy else None

    @property
    def session(self) -> requests.Session:
        if self._session is None:
            self._session = requests.Session()
        return self._session

    def close(self) -> None:
        if self._session:
            self._session.close()
            self._session = None

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.session.get(f"{self.base_url}/{path.lstrip('/')}", timeout=self.timeout, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self.session.post(f"{self.base_url}/{path.lstrip('/')}", timeout=self.timeout, **kwargs)

    def put(self, path: str, **kwargs: Any) -> requests.Response:
        return self.session.put(f"{self.base_url}/{path.lstrip('/')}", timeout=self.timeout, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return self.session.delete(f"{self.base_url}/{path.lstrip('/')}", timeout=self.timeout, **kwargs)
