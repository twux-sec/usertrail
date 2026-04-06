"""Platform definitions — one entry per service."""

import httpx
from hashlib import md5

from modules.base import Platform, Status


# ── Custom check functions ──────────────────────────────────────────

async def check_leboncoin(client: httpx.AsyncClient, username: str) -> Status:
    """Leboncoin profiles are not directly accessible by username.
    We check the search-like endpoint that redirects if the user exists."""
    url = f"https://www.leboncoin.fr/profil/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        return Status.FOUND if resp.status_code == 200 else Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_gravatar(client: httpx.AsyncClient, username: str) -> Status:
    """Gravatar uses an MD5 hash of the email, but also exposes profiles
    by username at gravatar.com/{username}."""
    url = f"https://gravatar.com/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "Profile not found" not in resp.text:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_telegram(client: httpx.AsyncClient, username: str) -> Status:
    """Telegram exposes a public preview page for usernames."""
    url = f"https://t.me/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "tgme_page_title" in resp.text:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_steam(client: httpx.AsyncClient, username: str) -> Status:
    """Steam community profile by custom URL."""
    url = f"https://steamcommunity.com/id/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "error_ctn" not in resp.text:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_reddit(client: httpx.AsyncClient, username: str) -> Status:
    """Reddit user check via old.reddit which gives clean 404s."""
    url = f"https://old.reddit.com/user/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_dockerhub(client: httpx.AsyncClient, username: str) -> Status:
    """DockerHub exposes a JSON API for users."""
    url = f"https://hub.docker.com/v2/users/{username}/"
    try:
        resp = await client.get(url)
        return Status.FOUND if resp.status_code == 200 else Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_medium(client: httpx.AsyncClient, username: str) -> Status:
    """Medium profiles at medium.com/@username."""
    url = f"https://medium.com/@{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "error" not in resp.url.path:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_twitch(client: httpx.AsyncClient, username: str) -> Status:
    """Twitch channel page — returns 200 even for missing users but page
    content differs."""
    url = f"https://www.twitch.tv/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and f"/{username}" in str(resp.url).lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


# ── Platform registry ───────────────────────────────────────────────

ALL_PLATFORMS: list[Platform] = [
    # French / European
    Platform(
        name="Leboncoin",
        url_template="https://www.leboncoin.fr/profil/{username}",
        check=check_leboncoin,
    ),
    Platform(
        name="Vinted",
        url_template="https://www.vinted.fr/member/{username}",
    ),
    Platform(
        name="Blablacar",
        url_template="https://www.blablacar.fr/user/show/{username}",
    ),
    Platform(
        name="Dealabs",
        url_template="https://www.dealabs.com/profile/{username}",
    ),
    Platform(
        name="Marmiton",
        url_template="https://www.marmiton.org/profil/{username}",
    ),
    Platform(
        name="Jeuxvideo.com",
        url_template="https://www.jeuxvideo.com/profil/{username}",
    ),
    # International
    Platform(
        name="Skool",
        url_template="https://www.skool.com/@{username}",
    ),
    Platform(
        name="Letterboxd",
        url_template="https://letterboxd.com/{username}",
    ),
    Platform(
        name="Flickr",
        url_template="https://www.flickr.com/people/{username}",
    ),
    Platform(
        name="Gravatar",
        url_template="https://gravatar.com/{username}",
        check=check_gravatar,
    ),
    Platform(
        name="Medium",
        url_template="https://medium.com/@{username}",
        check=check_medium,
    ),
    Platform(
        name="Reddit",
        url_template="https://www.reddit.com/user/{username}",
        check=check_reddit,
    ),
    # Developer
    Platform(
        name="GitHub",
        url_template="https://github.com/{username}",
    ),
    Platform(
        name="GitLab",
        url_template="https://gitlab.com/{username}",
    ),
    Platform(
        name="DockerHub",
        url_template="https://hub.docker.com/u/{username}",
        check=check_dockerhub,
    ),
    # Gaming / Social
    Platform(
        name="Steam",
        url_template="https://steamcommunity.com/id/{username}",
        check=check_steam,
    ),
    Platform(
        name="Twitch",
        url_template="https://www.twitch.tv/{username}",
        check=check_twitch,
    ),
    Platform(
        name="Telegram",
        url_template="https://t.me/{username}",
        check=check_telegram,
    ),
]
