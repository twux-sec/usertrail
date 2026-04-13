# UserTrail

**French & European platform OSINT — what Sherlock misses.**

Sherlock covers the big international platforms. UserTrail fills the gap with 65+ French and European services: marketplaces, forums, business registries, freelance platforms, blogs, and niche communities that fly under the radar of standard OSINT tools.

> Built with AI-assisted coding. Architecture, methodology, and decisions by the author. All output reviewed, tested, and validated manually.

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

## Supported Platforms (65+)

### France (42)

| Category | Platforms |
|---|---|
| Commerce & annonces | Leboncoin, Vinted.fr, Dealabs, Rakuten.fr, Back Market, Cdiscount, Selency |
| Transports & sorties | Blablacar, LaFourchette/TheFork, OnVaSortir, Couchsurfing |
| Forums & communautés | Jeuxvideo.com, Doctissimo, CCM (Comment Ça Marche), Marmiton, Skool |
| Tech & gaming | Hardware.fr (HFR), Caradisiac, Koreus, JeuxOnLine, Gamekult, Tric Trac |
| Femme & lifestyle | Aufeminin |
| Culture & avis | Allocine, Babelio, SensCritique, Trustpilot.fr |
| Blogs | Skyrock, Canalblog, Over-blog |
| Médias & musique | Dailymotion, Deezer |
| Éducation | OpenClassrooms |
| Emploi & freelance | LinkedIn.fr, Malt.fr, Welcome to the Jungle, France Travail, APEC, Cadremploi, Viadeo, Copains d'avant |
| Entreprises & registres | Pappers.fr, Societe.com, Infogreffe, Pages Jaunes |
| Immobilier | SeLoger, PAP.fr |
| Finance | BoursoBank |
| Créateurs & financement | MYM.fans, Ulule, KissKissBankBank, Tipeee, uTip, HelloAsso, Leetchi |

### Europe (23)

| Country | Platforms |
|---|---|
| Espagne | Wallapop, Milanuncios, Vinted.es, Blablacar.es |
| Allemagne | Kleinanzeigen.de, Vinted.de, Blablacar.de, AutoScout24 |
| Italie | Subito.it, Vinted.it, Blablacar.it |
| Pays-Bas | Marktplaats |
| Belgique | 2dehands.be, Immoweb.be |
| Suisse | Ricardo.ch, Tutti.ch |
| Autriche | Willhaben.at |
| Pologne | Allegro.pl, OLX.pl |

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
