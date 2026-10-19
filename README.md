# PulseCheck

An asynchronous website health monitor built with Python and HTTPX.

## Features

- Checks multiple websites concurrently using asyncio.
- Limits concurrent requests with asyncio.Semaphore.
- Measures HTTP response times.
- Follows HTTP redirects.
- Handles connection errors and timeouts.
- Displays website status and a summary.

## Tech Stack

- Python
- asyncio
- HTTPX

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd pulsecheck
```

## Create and activate a virtual environment:
```
python3 -m venv .venv
source .venv/bin/activate
```

## Install dependencies
```
pip install -r requirements.txt
```

## run the monitor
```
python3 main.py
```