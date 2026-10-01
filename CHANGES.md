# Proposed changes

## Application

- Replaced deprecated `send_file(..., attachment_filename=...)` with `download_name`.
- Removed the hard-coded Flask secret key and unrelated `OAUTHLIB_INSECURE_TRANSPORT` setting.
- Added an application factory (`create_app`) while retaining `qr:app` for Gunicorn compatibility.
- Added request/message size limits.
- Added explicit validation and 400 responses for invalid input.
- Added logged 500 handling without exposing exception details to users.
- Added basic security response headers.
- Moved runtime settings to environment variables with safe production defaults.
- Replaced Wand/ImageMagick composition with Pillow, reducing native system dependencies.
- Kept the existing 1280×720 output and upper-left QR placement as defaults.
- Changed QR error correction from L to M to give more tolerance for real-world camera/background use.

## Repository/GitHub

- Added `pyproject.toml` for modern Python project metadata and tool configuration.
- Replaced the old unpinned dependency list with bounded direct dependencies.
- Added development dependencies for pytest and Ruff.
- Added automated GitHub Actions CI for Python 3.10–3.13.
- Added `.gitignore` and `.gitattributes`.
- Added tests covering QR creation, image dimensions, validation, and downloads.
- Added deployment examples for Nginx and systemd.
- Reworked the README with setup, production, configuration, testing, and security guidance.
- Removed the old sample-image dependency from the main page so the application no longer depends on a repository asset that was only illustrative.

## Important release step

The original repository has no visible `LICENSE` file. Add a license that reflects the copyright holder's intent before treating the repository as an open-source release.
