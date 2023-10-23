import time
import shutil

from fastapi.testclient import TestClient
from PIL import Image

from src.main import app, BASE_DIR, UPLOAD_DIR, VALID_MEDIA_EXTENSIONS


client = TestClient(app)


def test_get_index():
    response = client.get(url="/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_post_index():
    response = client.post(url="/")
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]


def test_post_img():
    test_images = BASE_DIR / "images"
    for img in test_images.glob("*"):
        response = client.post(url="/upload", files={"file": open(img, "rb")})
        try:
            image = Image.open(img)
        except:
            image = None

        if image is None:
            assert response.status_code == 400, "image cant read."
        else:
            assert (
                response.headers["content-type"].split("/")[-1]
                in VALID_MEDIA_EXTENSIONS
            ), "check valid extension"
            assert response.status_code == 201, "everything successfully"

    time.sleep(2)
    shutil.rmtree(UPLOAD_DIR)
