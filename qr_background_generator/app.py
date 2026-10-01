"""Flask application for generating video-conference backgrounds containing a QR code."""

from __future__ import annotations

import io
import logging
from pathlib import Path

import qrcode
from flask import Flask, render_template, request, send_file
from PIL import Image

from . import settings

LOGGER = logging.getLogger(__name__)
TEMPLATE_DIR = Path(__file__).with_name("templates")


def make_qr(message: str) -> bytes:
    """Return a PNG QR code for *message*."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=settings.QR_BOX_SIZE,
        border=settings.QR_BORDER,
    )
    qr.add_data(message)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    output = io.BytesIO()
    image.save(output, format="PNG", optimize=True)
    return output.getvalue()


def convert_file(image_binary: bytes) -> bytes:
    """Place a QR image onto the configured video-conference background."""
    with Image.open(io.BytesIO(image_binary)) as foreground:
        foreground = foreground.convert("RGB")
        foreground.thumbnail(
            (settings.QR_SIZE, settings.QR_SIZE),
            Image.Resampling.LANCZOS,
        )

        background = Image.new(
            "RGB",
            (settings.BACKGROUND_WIDTH, settings.BACKGROUND_HEIGHT),
            settings.BACKGROUND_COLOR,
        )
        background.paste(foreground, (settings.QR_LEFT, settings.QR_TOP))

        output = io.BytesIO()
        background.save(output, format="PNG", optimize=True)
        return output.getvalue()


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__, template_folder=str(TEMPLATE_DIR))
    app.config["MAX_CONTENT_LENGTH"] = settings.MAX_REQUEST_BYTES

    @app.after_request
    def add_security_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        return response

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.post("/generate_background")
    def background():
        message = request.form.get("Message", "").strip()
        if not message:
            return render_template("error.html", message="Please enter text or a URL."), 400

        if len(message) > settings.MAX_MESSAGE_LENGTH:
            return (
                render_template(
                    "error.html",
                    message=(
                        f"The message is too long. Please limit it to "
                        f"{settings.MAX_MESSAGE_LENGTH:,} characters."
                    ),
                ),
                400,
            )

        try:
            background_png = convert_file(make_qr(message))
        except Exception:
            LOGGER.exception("Failed to generate QR background")
            return (
                render_template(
                    "error.html",
                    message="The background could not be generated. Please try again.",
                ),
                500,
            )

        return send_file(
            io.BytesIO(background_png),
            mimetype="image/png",
            as_attachment=True,
            download_name="background.png",
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)
