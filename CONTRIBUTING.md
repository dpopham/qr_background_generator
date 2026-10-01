# Contributing

Thanks for helping improve QR Background Generator.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

## Before opening a pull request

Run:

```bash
ruff check .
pytest -q
```

Please keep changes focused, add or update tests for behavior changes, and update the README when configuration or deployment behavior changes.

## Pull requests

Describe:

- what changed;
- why it changed;
- how it was tested; and
- any deployment or configuration changes required.
