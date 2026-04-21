#!/usr/bin/env python3
"""Diagnose broken platforms: fetch real vs fake and show diffs."""

import asyncio
import re
import secrets

import httpx
from rich.console import Console

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

console = Console()

# Broken platforms — format: (name, url_template)
BROKEN = [
    ("Leboncoin", "https://www.leboncoin.fr/profil/{u}"),
    ("Blablacar", "https://www.blablacar.fr/user/show/{u}"),
    ("Allocine", "https://www.allocine.fr/communaute/membre-{u}/"),
    ("Babelio", "https://www.babelio.com/monprofil.php?id_user={u}"),
    ("WTTJ", "https://www.welcometothejungle.com/fr/companies/{u}"),
    ("Dailymotion", "https://www.dailymotion.com/{u}"),
    ("SensCritique", "https://www.senscritique.com/{u}"),
    ("OpenClassrooms", "https://openclassrooms.com/fr/members/{u}"),
    ("Wallapop", "https://es.wallapop.com/app/user/{u}"),
    ("Milanuncios", "https://www.milanuncios.com/anuncios-de/{u}/"),
    ("Blablacar.es", "https://www.blablacar.es/user/show/{u}"),
    ("Blablacar.de", "https://www.blablacar.de/user/show/{u}"),
    ("Blablacar.it", "https://www.blablacar.it/user/show/{u}"),
    ("Immoweb", "https://www.immoweb.be/fr/agence/{u}"),
    ("OLX.pl", "https://www.olx.pl/oferty/uzytkownik/{u}/"),
]


def extract(text: str) -> dict:
    title = re.search(r"<title[^>]*>(.*?)</title>", text, re.IGNORECASE | re.DOTALL)
    og_title = re.search(
        r'<meta\s+property=["\']og:title["\']\s+content=["\']([^"\']+)', text
    )
    canon = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', text
    )
    return {
        "title": (title.group(1).strip()[:80] if title else ""),
        "og_title": (og_title.group(1)[:80] if og_title else ""),
        "canonical": (canon.group(1)[:100] if canon else ""),
        "size": len(text),
    }


async def probe(client: httpx.AsyncClient, url: str) -> dict:
    try:
        resp = await client.get(url, follow_redirects=True)
        noredir = await client.get(url, follow_redirects=False)
        info = extract(resp.text)
        info["final_url"] = str(resp.url)[:100]
        info["status_followed"] = resp.status_code
        info["status_noredir"] = noredir.status_code
        info["location"] = noredir.headers.get("location", "")[:100]
        return info
    except httpx.HTTPError as e:
        return {"error": str(e)[:80]}


async def diagnose_one(client: httpx.AsyncClient, name: str, tmpl: str, real: str):
    fake = "zq" + secrets.token_hex(5) + "xy"
    url_fake = tmpl.format(u=fake)
    url_real = tmpl.format(u=real)

    fake_data = await probe(client, url_fake)
    real_data = await probe(client, url_real)

    console.print(f"\n[bold cyan]═══ {name} ═══[/bold cyan]")
    console.print(f"[dim]tmpl:[/dim] {tmpl}")
    console.print(f"[yellow]FAKE ({fake}):[/yellow]")
    for k, v in fake_data.items():
        console.print(f"  {k}: {v}")
    console.print(f"[green]REAL ({real}):[/green]")
    for k, v in real_data.items():
        console.print(f"  {k}: {v}")


async def main():
    async with httpx.AsyncClient(
        headers=HEADERS, timeout=15.0, follow_redirects=False
    ) as client:
        for name, tmpl in BROKEN:
            await diagnose_one(client, name, tmpl, "admin")


if __name__ == "__main__":
    asyncio.run(main())
