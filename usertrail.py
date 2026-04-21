#!/usr/bin/env python3
"""UserTrail — French & European platform OSINT — what Sherlock misses."""

import argparse
import asyncio
import csv
import json
import sys
import webbrowser

import httpx
from rich.console import Console
from rich.table import Table

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

console = Console()


# ── Output helpers ──────────────────────────────────────────────────

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


def results_to_dicts(
    username: str, results: list[tuple[str, Status, str]]
) -> list[dict]:
    return [
        {"username": username, "platform": name, "status": status.value, "url": url}
        for name, status, url in sorted(results, key=lambda r: r[0].lower())
    ]


def export_json(all_results: dict[str, list[tuple[str, Status, str]]], path: str):
    data = {}
    for username, results in all_results.items():
        data[username] = results_to_dicts(username, results)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    console.print(f"[bold green]JSON saved to {path}[/bold green]")


def export_csv(all_results: dict[str, list[tuple[str, Status, str]]], path: str):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["username", "platform", "status", "url"])
        writer.writeheader()
        for username, results in all_results.items():
            writer.writerows(results_to_dicts(username, results))
    console.print(f"[bold green]CSV saved to {path}[/bold green]")


def verify_in_browser(results: list[tuple[str, Status, str]]):
    found = [(name, url) for name, status, url in results if status == Status.FOUND]
    if not found:
        console.print("[dim]No found profiles to verify.[/dim]")
        return
    console.print(f"\n[bold]Opening {len(found)} profile(s) in browser...[/bold]")
    for name, url in found:
        console.print(f"  -> {name}: {url}")
        webbrowser.open(url)


# ── Core scan logic ─────────────────────────────────────────────────

async def scan_username(
    username: str, timeout: float, show_all: bool, verify: bool
) -> list[tuple[str, Status, str]]:
    console.print(f"\nSearching for username: [bold]{username}[/bold]")

    async with httpx.AsyncClient(
        headers=HEADERS,
        timeout=httpx.Timeout(timeout),
        follow_redirects=False,
    ) as client:
        tasks = [
            check_platform(client, platform, username)
            for platform in ALL_PLATFORMS
            if platform.enabled
        ]
        results = await asyncio.gather(*tasks)

    table = build_table(username, results, show_all)
    console.print(table)

    found = sum(1 for _, s, _ in results if s == Status.FOUND)
    errors = sum(1 for _, s, _ in results if s == Status.ERROR)
    console.print(
        f"[bold green]{found}[/bold green] found · "
        f"[dim]{len(results) - found - errors} not found[/dim] · "
        f"[bold yellow]{errors}[/bold yellow] errors"
    )

    if verify:
        verify_in_browser(results)

    return results


async def run(args: argparse.Namespace):
    console.print(BANNER, style="bold cyan")

    # Collect usernames: single or batch
    usernames = []
    if args.batch:
        with open(args.batch, encoding="utf-8") as f:
            for line in f:
                name = line.strip()
                if name and not name.startswith("#"):
                    usernames.append(name)
        console.print(
            f"[bold]Batch mode:[/bold] {len(usernames)} username(s) "
            f"loaded from {args.batch}"
        )
    else:
        usernames.append(args.username)

    # Scan each username
    all_results: dict[str, list[tuple[str, Status, str]]] = {}
    for username in usernames:
        all_results[username] = await scan_username(
            username, args.timeout, args.all, args.verify
        )

    # Export if requested
    if args.json:
        export_json(all_results, args.json)
    if args.csv:
        export_csv(all_results, args.csv)


def main():
    parser = argparse.ArgumentParser(
        description="UserTrail — French & European platform OSINT — what Sherlock misses",
    )
    parser.add_argument(
        "username",
        nargs="?",
        default=None,
        help="Username to search for",
    )
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
    parser.add_argument(
        "--json",
        metavar="FILE",
        help="Export results to a JSON file",
    )
    parser.add_argument(
        "--csv",
        metavar="FILE",
        help="Export results to a CSV file",
    )
    parser.add_argument(
        "--batch",
        metavar="FILE",
        help="Read usernames from a file (one per line)",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Open found profile URLs in the default browser",
    )

    args = parser.parse_args()

    if not args.username and not args.batch:
        parser.error("provide a username or use --batch FILE")

    asyncio.run(run(args))


if __name__ == "__main__":
    main()
