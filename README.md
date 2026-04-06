# UserTrail

Username reconnaissance across European/French and international platforms.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Search for a username (shows only found results)
python usertrail.py johndoe

# Show all platforms (including not found)
python usertrail.py johndoe --all

# Custom timeout
python usertrail.py johndoe --timeout 15
```

## Supported Platforms

| Category | Platforms |
|---|---|
| French / European | Leboncoin, Vinted, Blablacar, Dealabs, Marmiton, Jeuxvideo.com |
| International | Skool, Letterboxd, Flickr, Gravatar, Medium, Reddit |
| Developer | GitHub, GitLab, DockerHub |
| Gaming / Social | Steam, Twitch, Telegram |

## Adding a New Platform

1. Open `modules/platforms.py`
2. Add a `Platform(...)` entry to `ALL_PLATFORMS`:
   - Simple case (HTTP 200 = found, 404 = not found): just set `name` and `url_template`
   - Custom logic: write an `async def check_xxx(client, username)` function and pass it as `check=`
3. Done — no other file needs to change.

## Disclaimer

This tool is intended for legitimate OSINT research, security auditing, and educational purposes only.
