"""Backward-compatible WSGI entry point.

Run with ``python qr.py`` or point Gunicorn at ``qr:app``.
"""

from qr_background_generator.app import app, convert_file, create_app, make_qr

__all__ = ["app", "convert_file", "create_app", "make_qr"]


if __name__ == "__main__":
    from qr_background_generator.app import settings

    app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)
