#!/usr/bin/env python3
"""UserTrail — Username reconnaissance across European & international platforms."""

import argparse
import asyncio
import sys

import httpx
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.text import Text

from modules import ALL_PLATFORMS, check_platform
from modules.base import Status

BANNER = r"""
  _   _               _____          _ _
 | | | |___  ___ _ __|_   _| __ __ _(_) |
 | | | / __|/ _ \ '__| | || '__/ _` | | |
 | |_| \__ \  __/ |    | || | | (_| | | |
  \___/|___/\___|_|    |_||_|  \__,_|_|_|
"""

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
}


def build_table(
    username: str,
    results: list[tuple[str, Status, str]],
    show_all: bool,
) -> Table:
    table = Table(
        title=f"Results for [bold cyan]{username}[/bold cyan]",
        show_lines=True,
    )
    table.add_column("Platform", style="bold white", min_width=14)
    table.add_column("Status", justify="center", min_width=10)
    table.add_column("URL", style="dim")

    for name, status, url in sorted(results, key=lambda r: r[0].lower()):
        if not show_all and status != Status.FOUND:
            continue
        if status == Status.FOUND:
            style = "[bold green]Found[/bold green]"
        elif status == Status.ERROR:
            style = "[bold yellow]Error[/bold yellow]"
        else:
            style = "[dim]Not Found[/dim]"
        table.add_row(name, style, url)

    return table


async def run(username: str, timeout: float, show_all: bool) -> list[tuple[str, Status, str]]:
    console = Console()
    console.print(BANNER, style="bold cyan")
    console.print(f"Searching for username: [bold]{username}[/bold]\n")

    async with httpx.AsyncClient(
        headers=HEADERS,
        timeout=httpx.Timeout(timeout),
        follow_redirects=False,
    ) as client:
        tasks = [
            check_platform(client, platform, username)
            for platform in ALL_PLATFORMS
        ]
        results = await asyncio.gather(*tasks)

    table = build_table(username, results, show_all)
    console.print(table)

    found = sum(1 for _, s, _ in results if s == Status.FOUND)
    errors = sum(1 for _, s, _ in results if s == Status.ERROR)
    console.print(
        f"\n[bold green]{found}[/bold green] found · "
        f"[dim]{len(results) - found - errors} not found[/dim] · "
        f"[bold yellow]{errors}[/bold yellow] errors"
    )

    return results


def main():
    parser = argparse.ArgumentParser(
        description="UserTrail — Username OSINT across European & international platforms",
    )
    parser.add_argument("username", help="Username to search for")
    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Show all platforms (including not found)",
    )
    parser.add_argument(
        "-t", "--timeout",
        type=float,
        default=10.0,
        help="HTTP request timeout in seconds (default: 10)",
    )
    args = parser.parse_args()
    asyncio.run(run(args.username, args.timeout, args.all))


if __name__ == "__main__":
    main()
