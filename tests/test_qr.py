from io import BytesIO

import pytest
from PIL import Image

from qr_background_generator import app
from qr_background_generator import convert_file, make_qr, settings


def test_make_qr_returns_valid_png():
    data = make_qr("https://example.com")

    with Image.open(BytesIO(data)) as image:
        assert image.format == "PNG"
        assert image.width > 0
        assert image.height > 0


def test_convert_file_creates_configured_background():
    result = convert_file(make_qr("hello"))

    with Image.open(BytesIO(result)) as image:
        assert image.format == "PNG"
        assert image.size == (settings.BACKGROUND_WIDTH, settings.BACKGROUND_HEIGHT)


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"QR Code Video Conference Call Background" in response.data


def test_empty_message_is_rejected(client):
    response = client.post("/generate_background", data={"Message": "   "})

    assert response.status_code == 400
    assert b"Please enter text or a URL" in response.data


def test_background_download(client):
    response = client.post(
        "/generate_background",
        data={"Message": "https://example.com"},
    )

    assert response.status_code == 200
    assert response.mimetype == "image/png"
    assert response.headers["Content-Disposition"].startswith("attachment;")

    with Image.open(BytesIO(response.data)) as image:
        assert image.size == (1280, 720)


def test_oversized_message_is_rejected(client, monkeypatch):
    monkeypatch.setattr(settings, "MAX_MESSAGE_LENGTH", 5)
    response = client.post("/generate_background", data={"Message": "123456"})

    assert response.status_code == 400
    assert b"message is too long" in response.data


@pytest.fixture
def client():
    qr.app.config.update(TESTING=True)
    with qr.app.test_client() as test_client:
        yield test_client
