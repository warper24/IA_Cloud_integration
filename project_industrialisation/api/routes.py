from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from services.process_media import process_media_pipeline
import os

router = APIRouter()

@router.post("/process_media/")
async def process_media(
    file: UploadFile = File(...),
    is_video: str = Form("false"),
    generate_txt: str = Form("false"),
    generate_srt: str = Form("false"),
    generate_video: str = Form("false"),
):
    """
    Route pour traiter un fichier (vidéo ou audio) avec les options utilisateur.
    - `is_video`: "true" pour une vidéo, "false" pour un fichier audio
    - `generate_txt`: "true" pour générer un fichier texte
    - `generate_srt`: "true" pour générer un fichier SRT
    - `generate_video`: "true" pour incruster les sous-titres sur la vidéo
    """

    # ✅ Vérification et conversion des booléens
    is_video = is_video.lower() == "true"
    generate_txt = generate_txt.lower() == "true"
    generate_srt = generate_srt.lower() == "true"
    generate_video = generate_video.lower() == "true"

    # ✅ Exécuter le pipeline avec les paramètres reçus
    result = await process_media_pipeline(file, is_video, generate_txt, generate_srt, generate_video)

    # ✅ Vérifier si une erreur est retournée
    if "error" in result:
        return JSONResponse(content=result, status_code=400)
    
    return JSONResponse(content=result)
