import pathlib
from PIL import Image
import pytesseract
import textwrap


BASE_DIR = pathlib.Path(__file__).parent
IMAGE_DIR = BASE_DIR / "images/ocr"
IMAGE_PATH = IMAGE_DIR / "Test_Ocr.png"


def ocr(path: pathlib.Path, lang: str = None):
    img = Image.open(path)
    preds = pytesseract.image_to_string(img, lang=lang)
    return textwrap.fill(preds)


instance = ocr(IMAGE_PATH)
print(instance)
