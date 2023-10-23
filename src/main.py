import pathlib
import io
import uuid

from fastapi import FastAPI, Request, UploadFile, HTTPException, status
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from PIL import Image

from src.settings import settings

BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
VALID_MEDIA_EXTENSIONS = ["jpg", "jpeg", "png"]

app = FastAPI(debug=settings.debug)
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/")
def index():
    return {"messages": "Done"}


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
