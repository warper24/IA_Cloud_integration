import pytest
import os
from unittest.mock import patch
import sys
sys.path.insert(0, "C:/Users/aysim/Documents/Ynov/I.A. dans Cloud/j1/fil_rouge/IA_Cloud_integration/project_industrialisation")
from utils.audio_extractor import AudioExtractor

def test_validate_file_valid():
    """Test si la validation accepte bien les fichiers .mp4 et .wav"""
    extractor_mp4 = AudioExtractor("test.mp4")
    extractor_wav = AudioExtractor("test.wav")

    assert extractor_mp4.input_file == "test.mp4"
    assert extractor_wav.input_file == "test.wav"

def test_validate_file_invalid():
    """Test si une erreur est levée pour un format de fichier non valide"""
    with pytest.raises(ValueError, match="Format non supporté"):
        AudioExtractor("test.txt")

    with pytest.raises(ValueError, match="Format non supporté"):
        AudioExtractor("test.avi")

@patch("ffmpeg.run")  # Mock ffmpeg.run pour éviter l'exécution réelle
def test_extract_audio(mock_ffmpeg_run):
    """Test si l'extraction retourne bien le bon nom de fichier sans exécuter ffmpeg"""
    extractor = AudioExtractor("test.mp4")
    extracted_audio = extractor.extract_audio()

    assert extracted_audio == "audio-test.wav"
    mock_ffmpeg_run.assert_called_once()  # Vérifie que ffmpeg.run a bien été appelé

def test_extract_audio_failure():
    """Test si l'extraction gère bien une erreur"""
    with patch("extract_audio.ffmpeg.run", side_effect=Exception("Erreur ffmpeg")):
        extractor = AudioExtractor("test.mp4")
        result = extractor.extract_audio()

        assert result is None  # Doit retourner None en cas d'échec
        