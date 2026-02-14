#!/usr/bin/env python3
"""Track S&P sector ETF 5D performance to mirror Google Finance's 5D change.

Method:
- Pull recent daily candles from Yahoo Finance chart API.
- Use adjusted close prices.
- Compute 5D % as: (latest_close / close_5_trading_days_ago - 1) * 100
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Iterable

DEFAULT_TICKERS = [
    "XLV",  # Health Care
    "XLK",  # Technology
    "XLF",  # Financials
    "XLI",  # Industrials
    "XLRE",  # Real Estate
    "XLE",  # Energy
    "XLP",  # Consumer Staples
    "XLY",  # Consumer Discretionary
    "XLB",  # Materials
    "XLU",  # Utilities
    "XLC",  # Communication Services
]

YAHOO_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"


@dataclass
class SectorPerformance:
    ticker: str
    latest_close: float
    base_close_5d: float
    performance_5d_pct: float


def fetch_adjusted_closes(ticker: str, range_period: str = "1mo", interval: str = "1d") -> list[float]:
    """Return adjusted close series for ticker from Yahoo Finance."""
    params = urllib.parse.urlencode({"range": range_period, "interval": interval})
    url = f"{YAHOO_CHART_URL.format(ticker=ticker)}?{params}"

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            )
        },
    )

    with urllib.request.urlopen(req, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))

    result = payload.get("chart", {}).get("result")
    if not result:
        error = payload.get("chart", {}).get("error")
        raise ValueError(f"No chart data for {ticker}: {error}")

    quote = result[0]
    indicators = quote.get("indicators", {})
    adjusted = indicators.get("adjclose", [])
    if not adjusted:
        raise ValueError(f"No adjusted-close series found for {ticker}")

    closes = adjusted[0].get("adjclose", [])
    clean_closes = [float(v) for v in closes if v is not None]
    if len(clean_closes) < 6:
        raise ValueError(f"Not enough daily candles to compute 5D for {ticker}")

    return clean_closes


def compute_5d_performance(ticker: str) -> SectorPerformance:
    closes = fetch_adjusted_closes(ticker)
    latest = closes[-1]
    base_5d = closes[-6]
    perf = (latest / base_5d - 1.0) * 100.0
    return SectorPerformance(
        ticker=ticker,
        latest_close=latest,
        base_close_5d=base_5d,
        performance_5d_pct=perf,
    )


def format_table(rows: Iterable[SectorPerformance]) -> str:
    rows = list(rows)
    header = f"{'Ticker':<8}{'5D %':>10}{'Base(5D ago)':>16}{'Latest':>12}"
    sep = "-" * len(header)
    body = [
        f"{r.ticker:<8}{r.performance_5d_pct:>9.2f}%{r.base_close_5d:>16.2f}{r.latest_close:>12.2f}"
        for r in rows
    ]
    return "\n".join([header, sep, *body])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Track S&P sector ETFs and report Google-Finance-like 5D performance %"
    )
    parser.add_argument(
        "--tickers",
        nargs="+",
        default=DEFAULT_TICKERS,
        help="Space-separated ETF tickers (default: common S&P sector SPDR ETFs)",
    )
    parser.add_argument(
        "--sort",
        choices=["ticker", "performance"],
        default="performance",
        help="Sort output by ticker or by 5D performance",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    results: list[SectorPerformance] = []
    failures: list[str] = []

    for ticker in args.tickers:
        try:
            results.append(compute_5d_performance(ticker.upper()))
        except Exception as exc:  # keep going per-ticker
            failures.append(f"{ticker}: {exc}")

    if args.sort == "ticker":
        results.sort(key=lambda r: r.ticker)
    else:
        results.sort(key=lambda r: r.performance_5d_pct, reverse=True)

    if results:
        print(format_table(results))

    if failures:
        print("\nWarnings:", file=sys.stderr)
        for msg in failures:
            print(f"- {msg}", file=sys.stderr)

    return 0 if results else 1


if __name__ == "__main__":
    raise SystemExit(main())
