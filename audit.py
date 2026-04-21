#!/usr/bin/env python3
"""Audit platform detection precision.

Runs each platform with:
  1. A random garbage username (must NOT be found)
  2. One or more real usernames (likely found on some platforms)

Flags as BROKEN any platform that returns FOUND for the garbage username.
That's the only reliable signal — false negatives are tolerable, false
positives pollute the whole tool.
"""

import argparse
import asyncio
import secrets

import httpx
from rich.console import Console
from rich.table import Table

from modules import ALL_PLATFORMS, check_platform
from modules.base import Status

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
}

console = Console()


def random_username() -> str:
    return "zq" + secrets.token_hex(6) + "xy"


async def scan(client: httpx.AsyncClient, username: str) -> dict[str, Status]:
    tasks = [
        check_platform(client, p, username)
        for p in ALL_PLATFORMS
        if p.enabled
    ]
    results = await asyncio.gather(*tasks)
    return {name: status for name, status, _ in results}


async def run(real_usernames: list[str], timeout: float):
    fake = random_username()
    console.print(f"[bold]Fake username:[/bold] [yellow]{fake}[/yellow]")
    console.print(f"[bold]Real usernames:[/bold] {', '.join(real_usernames)}\n")

    async with httpx.AsyncClient(
        headers=HEADERS,
        timeout=httpx.Timeout(timeout),
        follow_redirects=False,
    ) as client:
        console.print("[dim]Scanning fake username...[/dim]")
        fake_results = await scan(client, fake)

        real_results: list[dict[str, Status]] = []
        for u in real_usernames:
            console.print(f"[dim]Scanning {u}...[/dim]")
            real_results.append(await scan(client, u))

    broken: list[str] = []
    error_heavy: list[str] = []
    ok: list[str] = []
    discriminates: list[str] = []

    for name in fake_results:
        fake_status = fake_results[name]
        real_statuses = [r[name] for r in real_results]

        if fake_status == Status.FOUND:
            broken.append(name)
        elif fake_status == Status.ERROR:
            error_heavy.append(name)
        elif any(s == Status.FOUND for s in real_statuses):
            discriminates.append(name)
        else:
            ok.append(name)

    table = Table(title="Audit — platforms with false positives", show_lines=True)
    table.add_column("Status", min_width=16)
    table.add_column("Count", justify="right")
    table.add_column("Platforms")

    table.add_row(
        "[bold red]BROKEN (FP)[/bold red]",
        str(len(broken)),
        ", ".join(broken) or "-",
    )
    table.add_row(
        "[bold yellow]ERROR[/bold yellow]",
        str(len(error_heavy)),
        ", ".join(error_heavy) or "-",
    )
    table.add_row(
        "[bold green]DISCRIMINATES[/bold green]",
        str(len(discriminates)),
        ", ".join(discriminates) or "-",
    )
    table.add_row(
        "[dim]not-found on all tested[/dim]",
        str(len(ok)),
        ", ".join(ok) or "-",
    )
    console.print(table)

    total = len(fake_results)
    console.print(
        f"\n[bold]Summary:[/bold] {len(broken)}/{total} broken "
        f"([red]{len(broken)/total*100:.1f}%[/red] false-positive rate)"
    )
    console.print(
        f"  {len(discriminates)} platforms correctly discriminated a real user"
    )
    console.print(
        f"  {len(error_heavy)} platforms errored (bot protection, DNS, etc.)"
    )


def main():
    parser = argparse.ArgumentParser(description="UserTrail platform detection audit")
    parser.add_argument(
        "--real",
        nargs="+",
        default=["admin", "john"],
        help="Real usernames to test discrimination (default: admin john)",
    )
    parser.add_argument(
        "--timeout", type=float, default=10.0, help="Request timeout seconds"
    )
    args = parser.parse_args()
    asyncio.run(run(args.real, args.timeout))


if __name__ == "__main__":
    main()
