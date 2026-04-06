"""Base class and runner for platform checks."""

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Awaitable

import httpx


class Status(str, Enum):
    FOUND = "Found"
    NOT_FOUND = "Not Found"
    ERROR = "Error"


@dataclass
class Platform:
    name: str
    url_template: str  # must contain {username}
    check: Callable[[httpx.AsyncClient, str], Awaitable[Status]] | None = None

    def profile_url(self, username: str) -> str:
        return self.url_template.format(username=username)


async def _default_check(client: httpx.AsyncClient, url: str) -> Status:
    """GET the profile URL and return Found if 200, Not Found if 404."""
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        if resp.status_code in (301, 302, 404, 410):
            return Status.NOT_FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_platform(
    client: httpx.AsyncClient, platform: Platform, username: str
) -> tuple[str, Status, str]:
    """Check one platform. Returns (name, status, profile_url)."""
    url = platform.profile_url(username)
    if platform.check:
        status = await platform.check(client, username)
    else:
        status = await _default_check(client, url)
    return platform.name, status, url
