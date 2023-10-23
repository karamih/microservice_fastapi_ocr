import pathlib
import io
import uuid

from fastapi import FastAPI, Request, UploadFile, HTTPException, status
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
import pytesseract
import textwrap

from src.settings import settings

BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
VALID_MEDIA_EXTENSIONS = ["jpg", "jpeg", "png"]

app = FastAPI(debug=settings.debug)
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def ocr(request: Request, file: UploadFile):
    file_type = pathlib.Path(file.filename).suffix.replace(".", "")
    if file_type not in VALID_MEDIA_EXTENSIONS:
        raise HTTPException(
            detail="Use jpg, jpeg or png.", status_code=status.HTTP_400_BAD_REQUEST
        )
    content_stream = io.BytesIO(await file.read())
    try:
        image = Image.open(content_stream)
        preds = pytesseract.image_to_string(image)
        text = textwrap.fill(preds)
    except:
        raise HTTPException(
            detail="Can not open Image!", status_code=status.HTTP_400_BAD_REQUEST
        )
    return templates.TemplateResponse(
        "index.html", {"request": request, "ocr_text": text}
    )


@app.post("/upload", response_class=FileResponse, status_code=status.HTTP_201_CREATED)
async def upload_img(file: UploadFile):
    file_type = pathlib.Path(file.filename).suffix.replace(".", "")
    if file_type not in VALID_MEDIA_EXTENSIONS:
        raise HTTPException(
            detail="Use jpg, jpeg or png.", status_code=status.HTTP_400_BAD_REQUEST
        )
    UPLOAD_DIR.mkdir(exist_ok=True)
    content_stream = io.BytesIO(await file.read())
    try:
        image = Image.open(content_stream)
    except:
        raise HTTPException(
            detail="Can not open Image!", status_code=status.HTTP_400_BAD_REQUEST
        )
    full_path = UPLOAD_DIR / f"{uuid.uuid4()}.{file_type}"
    image.save(full_path)
    return full_path
