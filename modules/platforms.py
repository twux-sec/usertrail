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


# ── New French platforms ────────────────────────────────────────────

async def check_senscritique(client: httpx.AsyncClient, username: str) -> Status:
    """SensCritique — French review platform for movies, games, music."""
    url = f"https://www.senscritique.com/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "collection" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_deezer(client: httpx.AsyncClient, username: str) -> Status:
    """Deezer — French music streaming, public user profiles."""
    url = f"https://www.deezer.com/fr/profile/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "profile" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_dailymotion(client: httpx.AsyncClient, username: str) -> Status:
    """Dailymotion — French video platform."""
    url = f"https://www.dailymotion.com/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "channel" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_skyrock(client: httpx.AsyncClient, username: str) -> Status:
    """Skyrock — French blogging platform."""
    url = f"https://{username}.skyrock.com/"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "skyrock" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_canalblog(client: httpx.AsyncClient, username: str) -> Status:
    """Canalblog — French blogging platform."""
    url = f"https://{username}.canalblog.com/"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_openclassrooms(client: httpx.AsyncClient, username: str) -> Status:
    """OpenClassrooms — French e-learning platform."""
    url = f"https://openclassrooms.com/fr/members/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "profil" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_tipeee(client: httpx.AsyncClient, username: str) -> Status:
    """Tipeee — French creator tipping platform."""
    url = f"https://fr.tipeee.com/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "tipeee" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_utip(client: httpx.AsyncClient, username: str) -> Status:
    """uTip — French creator support platform."""
    url = f"https://utip.io/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_helloasso(client: httpx.AsyncClient, username: str) -> Status:
    """HelloAsso — French association fundraising."""
    url = f"https://www.helloasso.com/associations/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_leetchi(client: httpx.AsyncClient, username: str) -> Status:
    """Leetchi — French crowdfunding / money pots."""
    url = f"https://www.leetchi.com/fr/c/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_caradisiac(client: httpx.AsyncClient, username: str) -> Status:
    """Caradisiac — French automotive forum."""
    url = f"https://www.caradisiac.com/profil/{username}/"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "profil" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_hardwarefr(client: httpx.AsyncClient, username: str) -> Status:
    """Hardware.fr (HFR) — major French tech forum."""
    url = f"https://forum.hardware.fr/hfr/profil-{username}.htm"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "profil" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_aufeminin(client: httpx.AsyncClient, username: str) -> Status:
    """Aufeminin — French women's community forum."""
    url = f"https://www.aufeminin.com/profil/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "profil" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_koreus(client: httpx.AsyncClient, username: str) -> Status:
    """Koreus — French humor/viral content community."""
    url = f"https://www.koreus.com/membre/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "membre" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_jeuxonline(client: httpx.AsyncClient, username: str) -> Status:
    """JeuxOnLine — French MMORPG community."""
    url = f"https://www.jeuxonline.info/profil/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "profil" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_gamekult(client: httpx.AsyncClient, username: str) -> Status:
    """Gamekult — French video game reviews & community."""
    url = f"https://www.gamekult.com/membre/{username}.html"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "profil" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_rakuten_fr(client: httpx.AsyncClient, username: str) -> Status:
    """Rakuten.fr (ex PriceMinister) — French marketplace."""
    url = f"https://fr.shopping.rakuten.com/boutique/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "boutique" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_backmarket(client: httpx.AsyncClient, username: str) -> Status:
    """Back Market — French refurbished electronics marketplace."""
    url = f"https://www.backmarket.fr/fr-fr/seller/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_selency(client: httpx.AsyncClient, username: str) -> Status:
    """Selency — French vintage/design furniture marketplace."""
    url = f"https://www.selency.com/vendeur/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_seloger(client: httpx.AsyncClient, username: str) -> Status:
    """SeLoger — French real estate, agency profiles."""
    url = f"https://www.seloger.com/professionnels/agences/{username}/"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "agence" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_apec(client: httpx.AsyncClient, username: str) -> Status:
    """APEC — French executive job board profiles."""
    url = f"https://www.apec.fr/recruteur/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_cadremploi(client: httpx.AsyncClient, username: str) -> Status:
    """Cadremploi — French job board."""
    url = f"https://www.cadremploi.fr/entreprises/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


# ── European platforms ──────────────────────────────────────────────

async def check_wallapop(client: httpx.AsyncClient, username: str) -> Status:
    """Wallapop — Spanish secondhand marketplace."""
    url = f"https://es.wallapop.com/app/user/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_kleinanzeigen(client: httpx.AsyncClient, username: str) -> Status:
    """Kleinanzeigen.de (ex eBay Kleinanzeigen) — German classifieds."""
    url = f"https://www.kleinanzeigen.de/s-bestandsliste.html?userId={username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "anzeigen" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_marktplaats(client: httpx.AsyncClient, username: str) -> Status:
    """Marktplaats — Dutch classifieds marketplace."""
    url = f"https://www.marktplaats.nl/u/{username}/"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_subito(client: httpx.AsyncClient, username: str) -> Status:
    """Subito.it — Italian classifieds marketplace."""
    url = f"https://www.subito.it/shop/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_ricardo(client: httpx.AsyncClient, username: str) -> Status:
    """Ricardo.ch — Swiss auction/marketplace."""
    url = f"https://www.ricardo.ch/de/shop/{username}/"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_tutti(client: httpx.AsyncClient, username: str) -> Status:
    """Tutti.ch — Swiss classifieds."""
    url = f"https://www.tutti.ch/de/li/user/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_willhaben(client: httpx.AsyncClient, username: str) -> Status:
    """Willhaben.at — Austrian classifieds marketplace."""
    url = f"https://www.willhaben.at/iad/kaufen-und-verkaufen/verkaeuferprofil/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_allegro(client: httpx.AsyncClient, username: str) -> Status:
    """Allegro.pl — Polish marketplace."""
    url = f"https://allegro.pl/uzytkownik/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_olx_pl(client: httpx.AsyncClient, username: str) -> Status:
    """OLX.pl — Polish classifieds."""
    url = f"https://www.olx.pl/oferty/uzytkownik/{username}/"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_2dehands(client: httpx.AsyncClient, username: str) -> Status:
    """2dehands.be / 2ememain.be — Belgian classifieds."""
    url = f"https://www.2dehands.be/u/{username}/"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_immoweb(client: httpx.AsyncClient, username: str) -> Status:
    """Immoweb.be — Belgian real estate agency profiles."""
    url = f"https://www.immoweb.be/fr/agence/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_autoscout24(client: httpx.AsyncClient, username: str) -> Status:
    """AutoScout24 — European car marketplace dealer profiles."""
    url = f"https://www.autoscout24.fr/concessionnaires/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_milanuncios(client: httpx.AsyncClient, username: str) -> Status:
    """Milanuncios — Spanish classifieds."""
    url = f"https://www.milanuncios.com/anuncios-de/{username}/"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_vinted_de(client: httpx.AsyncClient, username: str) -> Status:
    """Vinted.de — German Vinted."""
    url = f"https://www.vinted.de/member/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "closet-empty" not in resp.text:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_vinted_es(client: httpx.AsyncClient, username: str) -> Status:
    """Vinted.es — Spanish Vinted."""
    url = f"https://www.vinted.es/member/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "closet-empty" not in resp.text:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_vinted_it(client: httpx.AsyncClient, username: str) -> Status:
    """Vinted.it — Italian Vinted."""
    url = f"https://www.vinted.it/member/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "closet-empty" not in resp.text:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_pap(client: httpx.AsyncClient, username: str) -> Status:
    """PAP.fr — French private real estate ads."""
    url = f"https://www.pap.fr/annonceur/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_overblog(client: httpx.AsyncClient, username: str) -> Status:
    """Over-blog — French blogging platform."""
    url = f"https://{username}.over-blog.com/"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_trictrac(client: httpx.AsyncClient, username: str) -> Status:
    """Tric Trac — French board game community."""
    url = f"https://www.trictrac.net/utilisateur/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "profil" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_cdiscount(client: httpx.AsyncClient, username: str) -> Status:
    """Cdiscount — French e-commerce seller profiles."""
    url = f"https://www.cdiscount.com/mpv-{username}.html"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and "vendeur" in resp.text.lower():
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_blablacar_es(client: httpx.AsyncClient, username: str) -> Status:
    """Blablacar.es — Spanish Blablacar."""
    url = f"https://www.blablacar.es/user/show/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_blablacar_de(client: httpx.AsyncClient, username: str) -> Status:
    """Blablacar.de — German Blablacar."""
    url = f"https://www.blablacar.de/user/show/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            return Status.FOUND
        return Status.NOT_FOUND
    except httpx.HTTPError:
        return Status.ERROR


async def check_blablacar_it(client: httpx.AsyncClient, username: str) -> Status:
    """Blablacar.it — Italian Blablacar."""
    url = f"https://www.blablacar.it/user/show/{username}"
    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
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
    # ── Médias & vidéo FR ───────────────────────────────────────────
    Platform(
        name="Dailymotion",
        url_template="https://www.dailymotion.com/{username}",
        check=check_dailymotion,
    ),
    Platform(
        name="Deezer",
        url_template="https://www.deezer.com/fr/profile/{username}",
        check=check_deezer,
    ),
    # ── Reviews & culture FR ────────────────────────────────────────
    Platform(
        name="SensCritique",
        url_template="https://www.senscritique.com/{username}",
        check=check_senscritique,
    ),
    # ── Blogs FR ────────────────────────────────────────────────────
    Platform(
        name="Skyrock",
        url_template="https://{username}.skyrock.com/",
        check=check_skyrock,
    ),
    Platform(
        name="Canalblog",
        url_template="https://{username}.canalblog.com/",
        check=check_canalblog,
    ),
    Platform(
        name="Over-blog",
        url_template="https://{username}.over-blog.com/",
        check=check_overblog,
    ),
    # ── Éducation FR ────────────────────────────────────────────────
    Platform(
        name="OpenClassrooms",
        url_template="https://openclassrooms.com/fr/members/{username}",
        check=check_openclassrooms,
    ),
    # ── Créateurs & tips FR ─────────────────────────────────────────
    Platform(
        name="Tipeee",
        url_template="https://fr.tipeee.com/{username}",
        check=check_tipeee,
    ),
    Platform(
        name="uTip",
        url_template="https://utip.io/{username}",
        check=check_utip,
    ),
    # ── Associations & cagnottes FR ─────────────────────────────────
    Platform(
        name="HelloAsso",
        url_template="https://www.helloasso.com/associations/{username}",
        check=check_helloasso,
    ),
    Platform(
        name="Leetchi",
        url_template="https://www.leetchi.com/fr/c/{username}",
        check=check_leetchi,
    ),
    # ── Forums tech & gaming FR ─────────────────────────────────────
    Platform(
        name="Hardware.fr (HFR)",
        url_template="https://forum.hardware.fr/hfr/profil-{username}.htm",
        check=check_hardwarefr,
    ),
    Platform(
        name="Caradisiac",
        url_template="https://www.caradisiac.com/profil/{username}/",
        check=check_caradisiac,
    ),
    Platform(
        name="Aufeminin",
        url_template="https://www.aufeminin.com/profil/{username}",
        check=check_aufeminin,
    ),
    Platform(
        name="Koreus",
        url_template="https://www.koreus.com/membre/{username}",
        check=check_koreus,
    ),
    Platform(
        name="JeuxOnLine",
        url_template="https://www.jeuxonline.info/profil/{username}",
        check=check_jeuxonline,
    ),
    Platform(
        name="Gamekult",
        url_template="https://www.gamekult.com/membre/{username}.html",
        check=check_gamekult,
    ),
    Platform(
        name="Tric Trac",
        url_template="https://www.trictrac.net/utilisateur/{username}",
        check=check_trictrac,
    ),
    # ── Commerce FR ─────────────────────────────────────────────────
    Platform(
        name="Rakuten.fr",
        url_template="https://fr.shopping.rakuten.com/boutique/{username}",
        check=check_rakuten_fr,
    ),
    Platform(
        name="Back Market",
        url_template="https://www.backmarket.fr/fr-fr/seller/{username}",
        check=check_backmarket,
    ),
    Platform(
        name="Cdiscount",
        url_template="https://www.cdiscount.com/mpv-{username}.html",
        check=check_cdiscount,
    ),
    Platform(
        name="Selency",
        url_template="https://www.selency.com/vendeur/{username}",
        check=check_selency,
    ),
    # ── Immobilier FR ───────────────────────────────────────────────
    Platform(
        name="SeLoger",
        url_template="https://www.seloger.com/professionnels/agences/{username}/",
        check=check_seloger,
    ),
    Platform(
        name="PAP.fr",
        url_template="https://www.pap.fr/annonceur/{username}",
        check=check_pap,
    ),
    # ── Emploi FR ───────────────────────────────────────────────────
    Platform(
        name="APEC",
        url_template="https://www.apec.fr/recruteur/{username}",
        check=check_apec,
    ),
    Platform(
        name="Cadremploi",
        url_template="https://www.cadremploi.fr/entreprises/{username}",
        check=check_cadremploi,
    ),
    # ── Européen : Espagne ──────────────────────────────────────────
    Platform(
        name="Wallapop (ES)",
        url_template="https://es.wallapop.com/app/user/{username}",
        check=check_wallapop,
    ),
    Platform(
        name="Milanuncios (ES)",
        url_template="https://www.milanuncios.com/anuncios-de/{username}/",
        check=check_milanuncios,
    ),
    Platform(
        name="Vinted.es",
        url_template="https://www.vinted.es/member/{username}",
        check=check_vinted_es,
    ),
    Platform(
        name="Blablacar.es",
        url_template="https://www.blablacar.es/user/show/{username}",
        check=check_blablacar_es,
    ),
    # ── Européen : Allemagne ────────────────────────────────────────
    Platform(
        name="Kleinanzeigen.de",
        url_template="https://www.kleinanzeigen.de/s-bestandsliste.html?userId={username}",
        check=check_kleinanzeigen,
    ),
    Platform(
        name="Vinted.de",
        url_template="https://www.vinted.de/member/{username}",
        check=check_vinted_de,
    ),
    Platform(
        name="Blablacar.de",
        url_template="https://www.blablacar.de/user/show/{username}",
        check=check_blablacar_de,
    ),
    Platform(
        name="AutoScout24 (EU)",
        url_template="https://www.autoscout24.fr/concessionnaires/{username}",
        check=check_autoscout24,
    ),
    # ── Européen : Italie ───────────────────────────────────────────
    Platform(
        name="Subito.it",
        url_template="https://www.subito.it/shop/{username}",
        check=check_subito,
    ),
    Platform(
        name="Vinted.it",
        url_template="https://www.vinted.it/member/{username}",
        check=check_vinted_it,
    ),
    Platform(
        name="Blablacar.it",
        url_template="https://www.blablacar.it/user/show/{username}",
        check=check_blablacar_it,
    ),
    # ── Européen : Pays-Bas ─────────────────────────────────────────
    Platform(
        name="Marktplaats (NL)",
        url_template="https://www.marktplaats.nl/u/{username}/",
        check=check_marktplaats,
    ),
    # ── Européen : Belgique ─────────────────────────────────────────
    Platform(
        name="2dehands.be",
        url_template="https://www.2dehands.be/u/{username}/",
        check=check_2dehands,
    ),
    Platform(
        name="Immoweb.be",
        url_template="https://www.immoweb.be/fr/agence/{username}",
        check=check_immoweb,
    ),
    # ── Européen : Suisse ───────────────────────────────────────────
    Platform(
        name="Ricardo.ch",
        url_template="https://www.ricardo.ch/de/shop/{username}/",
        check=check_ricardo,
    ),
    Platform(
        name="Tutti.ch",
        url_template="https://www.tutti.ch/de/li/user/{username}",
        check=check_tutti,
    ),
    # ── Européen : Autriche ─────────────────────────────────────────
    Platform(
        name="Willhaben.at",
        url_template="https://www.willhaben.at/iad/kaufen-und-verkaufen/verkaeuferprofil/{username}",
        check=check_willhaben,
    ),
    # ── Européen : Pologne ──────────────────────────────────────────
    Platform(
        name="Allegro.pl",
        url_template="https://allegro.pl/uzytkownik/{username}",
        check=check_allegro,
    ),
    Platform(
        name="OLX.pl",
        url_template="https://www.olx.pl/oferty/uzytkownik/{username}/",
        check=check_olx_pl,
    ),
]
