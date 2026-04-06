# UserTrail

**French & European platform OSINT — what Sherlock misses.**

Sherlock covers the big international platforms. UserTrail fills the gap with 29 French and European services: marketplaces, forums, business registries, freelance platforms, and niche communities that fly under the radar of standard OSINT tools.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Basic search (shows found results only)
python usertrail.py johndoe

# Show all platforms including not found
python usertrail.py johndoe --all

# Export results
python usertrail.py johndoe --json results.json
python usertrail.py johndoe --csv results.csv

# Batch mode (one username per line)
python usertrail.py --batch usernames.txt --json results.json

# Open found profiles in browser for manual verification
python usertrail.py johndoe --verify

# Custom timeout
python usertrail.py johndoe --timeout 15
```

## Supported Platforms (29)

| Category | Platforms |
|---|---|
| Commerce & annonces | Leboncoin, Vinted.fr, Dealabs |
| Transports & sorties | Blablacar, LaFourchette/TheFork, OnVaSortir, Couchsurfing |
| Forums & communautés | Jeuxvideo.com, Doctissimo, CCM (Comment Ça Marche), Marmiton, Skool |
| Culture & avis | Allocine, Babelio, Trustpilot.fr |
| Emploi & freelance | LinkedIn.fr, Malt.fr, Welcome to the Jungle, France Travail, Viadeo, Copains d'avant |
| Entreprises & registres | Pappers.fr, Societe.com, Infogreffe, Pages Jaunes |
| Finance | BoursoBank |
| Créateurs & financement | MYM.fans, Ulule, KissKissBankBank |

## Adding a New Platform

1. Open `modules/platforms.py`
2. If the site returns clean 404s for missing users, just add:
   ```python
   Platform(name="SiteName", url_template="https://example.fr/user/{username}"),
   ```
3. If the site needs custom logic (auth walls, soft 404s, etc.), write a check function:
   ```python
   async def check_sitename(client: httpx.AsyncClient, username: str) -> Status:
       ...

   Platform(name="SiteName", url_template="...", check=check_sitename),
   ```
4. Done — no other file needs to change.

## Sherlock + UserTrail

Use both tools together for comprehensive coverage:

```bash
# International platforms
sherlock johndoe

# French & European platforms
python usertrail.py johndoe --json french_results.json
```

## Disclaimer

This tool is intended for legitimate OSINT research, security auditing, and educational purposes only. Respect the terms of service of each platform and applicable privacy laws (GDPR).
