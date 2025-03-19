from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException, status
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from main import process_file
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# Montage du dossier static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration des dossiers d'upload et de sortie
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
ALLOWED_EXTENSIONS = {"mp4", "wav"}

# Création des dossiers si nécessaire
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

templates = Jinja2Templates(directory="templates")

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/audio", response_class=HTMLResponse)
async def audio(request: Request):
    return templates.TemplateResponse("audio.html", {"request": request})

@app.get("/video", response_class=HTMLResponse)
async def video(request: Request):
    return templates.TemplateResponse("video.html", {"request": request})

@app.post("/process")
async def process(request: Request, file: UploadFile = File(...), output_type: str = Form(...)):
    filename = file.filename
    if not allowed_file(filename):
        raise HTTPException(status_code=400, detail="Format de fichier non supporté.")
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
        print("DEBUG: file_path =", file_path)
        print("DEBUG: Fichier existe ?", os.path.exists(file_path))
    try:
        result_path = process_file(file_path, output_type, OUTPUT_FOLDER)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # Redirige l'utilisateur vers la page de téléchargement
    return RedirectResponse(url=f"/downloads/{os.path.basename(result_path)}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/downloads/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fichier non trouvé.")
    return FileResponse(file_path, filename=filename, media_type='application/octet-stream')
