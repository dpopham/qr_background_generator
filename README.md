# QR Background Generator

A small Flask web service that creates a **1280×720 PNG video-conference background** with a QR code in the upper-left corner. Enter plain text or a URL and download the generated `background.png`.

## Features

- Plain text or URL QR codes
- 1280×720 PNG output by default
- Configurable QR size and position
- Configurable background dimensions/color
- Input-size limits to avoid accidentally generating unmanageably large QR codes
- No database, external API, or persistent user data
- Pillow-based image composition; ImageMagick/Wand is not required
- Automated tests and GitHub Actions CI
- Gunicorn and Nginx deployment examples

## Requirements

- Python 3.10+

## Local development

```bash
git clone https://github.com/dpopham/qr_background_generator.git
cd qr_background_generator

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\\Scripts\\activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt

python qr.py
```

Open <http://127.0.0.1:5555/>.

## Production

Use Gunicorn rather than Flask's development server:

```bash
gunicorn --workers 2 --bind 127.0.0.1:5555 qr:app
```

See [`deploy/nginx.conf.example`](deploy/nginx.conf.example) and [`deploy/qr-background-generator.service.example`](deploy/qr-background-generator.service.example) for deployment examples.

## Configuration

All settings are environment variables; no secrets are stored in source code.

| Variable | Default | Purpose |
| --- | --- | --- |
| `QR_HOST` | `127.0.0.1` | Development server bind address |
| `QR_PORT` | `5555` | Development/server port |
| `QR_DEBUG` | `false` | Flask debug mode; leave off in production |
| `QR_BACKGROUND_WIDTH` | `1280` | Output width in pixels |
| `QR_BACKGROUND_HEIGHT` | `720` | Output height in pixels |
| `QR_BACKGROUND_COLOR` | `white` | Pillow background color |
| `QR_SIZE` | `300` | Maximum QR width/height in pixels |
| `QR_LEFT` | `0` | QR left offset |
| `QR_TOP` | `0` | QR top offset |
| `QR_BOX_SIZE` | `10` | QR module size before resizing |
| `QR_BORDER` | `4` | QR quiet-zone width in modules |
| `QR_MAX_MESSAGE_LENGTH` | `2048` | Maximum encoded message length |
| `QR_MAX_REQUEST_BYTES` | `16384` | Maximum HTTP request body |

## Tests and linting

```bash
python -m pytest -q
ruff check .
```

GitHub Actions runs both checks across supported Python versions.

## Project layout

```text
.
├── .github/workflows/ci.yml
├── deploy/
│   ├── nginx.conf.example
│   └── qr-background-generator.service.example
├── templates/
│   ├── error.html
│   └── index.html
├── tests/test_qr.py
├── qr.py                         # backwards-compatible WSGI entry point
├── settings.py                   # backwards-compatible import shim
├── qr_background_generator/
│   ├── __init__.py
│   ├── app.py
│   ├── settings.py
│   └── templates/
├── pyproject.toml
├── requirements.txt
└── requirements-dev.txt
```

## Security notes

The application is intended to run behind a reverse proxy such as Nginx. By default it binds to `127.0.0.1`, does not enable Flask debug mode, does not embed a secret key in source, and limits request/message sizes. If the service is exposed publicly, consider adding rate limiting at the reverse proxy or application gateway.

