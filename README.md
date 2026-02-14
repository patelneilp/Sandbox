## S&P Sector 5D Tracker

`sector_tracker.py` fetches daily data for sector ETFs (XLV, XLK, XLF, XLI, XLRE, XLE, etc.) and computes a 5-day trading performance percentage.

### Why this matches Google Finance 5D
Google Finance's **5D** view is based on recent trading sessions rather than calendar days. This tool uses:

- latest adjusted close
- adjusted close from **5 trading days earlier**

Formula:

```text
5D % = (latest_close / close_5_trading_days_ago - 1) * 100
```

### Run

```bash
python3 sector_tracker.py
```

Custom tickers:

```bash
python3 sector_tracker.py --tickers XLV XLK XLF XLI XLRE XLE
```

Sort alphabetically:

```bash
python3 sector_tracker.py --sort ticker
```
