"""French & European platform definitions — what Sherlock misses."""

import httpx

from modules.base import Platform, Status


# ── Custom check functions ──────────────────────────────────────────

async def check_leboncoin(client: httpx.AsyncClient, username: str) -> Status:
    url = f"https://www.leboncoin.fr/profil/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        return Status.FOUND if resp.status_code == 200 else Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_vinted(client: httpx.AsyncClient, username: str) -> Status:
    """Vinted member pages — check .fr domain."""
    url = f"https://www.vinted.fr/member/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "closet-empty" not in resp.text:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_dealabs(client: httpx.AsyncClient, username: str) -> Status:
    url = f"https://www.dealabs.com/profile/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and username.lower() in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_jvc(client: httpx.AsyncClient, username: str) -> Status:
    """Jeuxvideo.com — profile pages return 200 with error content for missing users."""
    url = f"https://www.jeuxvideo.com/profil/{username}?mode=infos"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "Ce profil n'existe pas" not in resp.text:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_doctissimo(client: httpx.AsyncClient, username: str) -> Status:
    url = f"https://www.doctissimo.fr/membre/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "profil" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_allocine(client: httpx.AsyncClient, username: str) -> Status:
    """Allocine community member search."""
    url = f"https://www.allocine.fr/communaute/membre-{username}/"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_babelio(client: httpx.AsyncClient, username: str) -> Status:
    url = f"https://www.babelio.com/monprofil.php?id_user={username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "Ce membre n'existe pas" not in resp.text:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_malt(client: httpx.AsyncClient, username: str) -> Status:
    """Malt.fr freelancer profiles."""
    url = f"https://www.malt.fr/profile/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_wttj(client: httpx.AsyncClient, username: str) -> Status:
    """Welcome to the Jungle company pages."""
    url = f"https://www.welcometothejungle.com/fr/companies/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_trustpilot(client: httpx.AsyncClient, username: str) -> Status:
    url = f"https://fr.trustpilot.com/users/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "profile" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_pappers(client: httpx.AsyncClient, username: str) -> Status:
    """Pappers.fr — company/person search."""
    url = f"https://www.pappers.fr/recherche?q={username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "résultat" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_societe(client: httpx.AsyncClient, username: str) -> Status:
    """Societe.com — company/dirigeant search."""
    url = f"https://www.societe.com/cgi-bin/search?champs={username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "résultat" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_infogreffe(client: httpx.AsyncClient, username: str) -> Status:
    """Infogreffe — French business registry search."""
    url = f"https://www.infogreffe.fr/recherche-entreprise-dirigeants/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_linkedin(client: httpx.AsyncClient, username: str) -> Status:
    url = f"https://fr.linkedin.com/in/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "authwall" not in str(resp.url).lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_copainsdavant(client: httpx.AsyncClient, username: str) -> Status:
    """Copains d'avant — French alumni network."""
    url = f"https://copainsdavant.linternaute.com/p/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "profil" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_viadeo(client: httpx.AsyncClient, username: str) -> Status:
    url = f"https://www.viadeo.com/p/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_onvasortir(client: httpx.AsyncClient, username: str) -> Status:
    url = f"https://www.onvasortir.com/profil/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "profil" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_couchsurfing(client: httpx.AsyncClient, username: str) -> Status:
    url = f"https://www.couchsurfing.com/people/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "login" not in str(resp.url).lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_mym(client: httpx.AsyncClient, username: str) -> Status:
    """MYM.fans creator profile."""
    url = f"https://mym.fans/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "creator" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_ulule(client: httpx.AsyncClient, username: str) -> Status:
    url = f"https://fr.ulule.com/{username}/"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_kkbb(client: httpx.AsyncClient, username: str) -> Status:
    """KissKissBankBank user profile."""
    url = f"https://www.kisskissbankbank.com/fr/users/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_boursobank(client: httpx.AsyncClient, username: str) -> Status:
    """BoursoBank (ex-Boursorama) community forum profile."""
    url = f"https://www.boursorama.com/membres/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "profil" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_pagesjaunes(client: httpx.AsyncClient, username: str) -> Status:
    """Pages Jaunes / Solocal — professional listing search."""
    url = f"https://www.pagesjaunes.fr/recherche/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "résultat" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


# ── Platform registry ───────────────────────────────────────────────

ALL_PLATFORMS: list[Platform] = [
    # ── Commerce & petites annonces ─────────────────────────────────
    Platform(
        name="Leboncoin",
        url_template="https://www.leboncoin.fr/profil/{username}",
        check=check_leboncoin,
    ),
    Platform(
        name="Vinted.fr",
        url_template="https://www.vinted.fr/member/{username}",
        check=check_vinted,
    ),
    Platform(
        name="Dealabs",
        url_template="https://www.dealabs.com/profile/{username}",
        check=check_dealabs,
    ),
    # ── Transports & sorties ────────────────────────────────────────
    Platform(
        name="Blablacar",
        url_template="https://www.blablacar.fr/user/show/{username}",
    ),
    Platform(
        name="LaFourchette/TheFork",
        url_template="https://www.thefork.fr/restaurant/{username}",
    ),
    Platform(
        name="OnVaSortir",
        url_template="https://www.onvasortir.com/profil/{username}",
        check=check_onvasortir,
    ),
    Platform(
        name="Couchsurfing",
        url_template="https://www.couchsurfing.com/people/{username}",
        check=check_couchsurfing,
    ),
    # ── Forums & communautés ────────────────────────────────────────
    Platform(
        name="Jeuxvideo.com",
        url_template="https://www.jeuxvideo.com/profil/{username}?mode=infos",
        check=check_jvc,
    ),
    Platform(
        name="Doctissimo",
        url_template="https://www.doctissimo.fr/membre/{username}",
        check=check_doctissimo,
    ),
    Platform(
        name="CCM (Comment Ça Marche)",
        url_template="https://www.commentcamarche.net/profile/user/{username}",
    ),
    Platform(
        name="Marmiton",
        url_template="https://www.marmiton.org/profil/{username}",
    ),
    Platform(
        name="Skool",
        url_template="https://www.skool.com/@{username}",
    ),
    # ── Culture & avis ──────────────────────────────────────────────
    Platform(
        name="Allocine",
        url_template="https://www.allocine.fr/communaute/membre-{username}/",
        check=check_allocine,
    ),
    Platform(
        name="Babelio",
        url_template="https://www.babelio.com/monprofil.php?id_user={username}",
        check=check_babelio,
    ),
    Platform(
        name="Trustpilot.fr",
        url_template="https://fr.trustpilot.com/users/{username}",
        check=check_trustpilot,
    ),
    # ── Emploi & freelance ──────────────────────────────────────────
    Platform(
        name="LinkedIn.fr",
        url_template="https://fr.linkedin.com/in/{username}",
        check=check_linkedin,
    ),
    Platform(
        name="Malt.fr",
        url_template="https://www.malt.fr/profile/{username}",
        check=check_malt,
    ),
    Platform(
        name="Welcome to the Jungle",
        url_template="https://www.welcometothejungle.com/fr/companies/{username}",
        check=check_wttj,
    ),
    Platform(
        name="France Travail",
        url_template="https://candidat.francetravail.fr/portail-employeur/{username}",
    ),
    Platform(
        name="Viadeo",
        url_template="https://www.viadeo.com/p/{username}",
        check=check_viadeo,
    ),
    Platform(
        name="Copains d'avant",
        url_template="https://copainsdavant.linternaute.com/p/{username}",
        check=check_copainsdavant,
    ),
    # ── Entreprises & registres ─────────────────────────────────────
    Platform(
        name="Pappers.fr",
        url_template="https://www.pappers.fr/recherche?q={username}",
        check=check_pappers,
    ),
    Platform(
        name="Societe.com",
        url_template="https://www.societe.com/cgi-bin/search?champs={username}",
        check=check_societe,
    ),
    Platform(
        name="Infogreffe",
        url_template="https://www.infogreffe.fr/recherche-entreprise-dirigeants/{username}",
        check=check_infogreffe,
    ),
    Platform(
        name="Pages Jaunes",
        url_template="https://www.pagesjaunes.fr/recherche/{username}",
        check=check_pagesjaunes,
    ),
    # ── Finance ─────────────────────────────────────────────────────
    Platform(
        name="BoursoBank",
        url_template="https://www.boursorama.com/membres/{username}",
        check=check_boursobank,
    ),
    # ── Créateurs & financement ─────────────────────────────────────
    Platform(
        name="MYM.fans",
        url_template="https://mym.fans/{username}",
        check=check_mym,
    ),
    Platform(
        name="Ulule",
        url_template="https://fr.ulule.com/{username}/",
        check=check_ulule,
    ),
    Platform(
        name="KissKissBankBank",
        url_template="https://www.kisskissbankbank.com/fr/users/{username}",
        check=check_kkbb,
    ),
]
