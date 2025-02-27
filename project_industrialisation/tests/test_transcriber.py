import pytest
import sys
from unittest.mock import patch
sys.path.insert(0, "C:/Users/aysim/Documents/Ynov/I.A. dans Cloud/j1/fil_rouge/IA_Cloud_integration/project_industrialisation")
from utils.transcriber import Transcriber


@pytest.fixture
def transcriber():
    return Transcriber()


# Test 1 : Vérifier que seuls les fichiers .wav sont acceptés
@pytest.mark.parametrize(
    "invalid_file", ["audio.mp3", "audio.flac", "audio.ogg", "audio.txt"]
)
def test_validate_audio_file_invalid(transcriber, invalid_file):
    with pytest.raises(ValueError, match="Format non supporté"):
        transcriber.validate_audio_file(invalid_file)


# Test 2 : Vérifier qu'un fichier .wav est bien accepté
def test_validate_audio_file_valid(transcriber):
    try:
        transcriber.validate_audio_file("test.wav")
    except ValueError:
        pytest.fail("""validate_audio_file a levé
                    une ValueError pour un .wav valide""")


# Test 3 : Simuler une transcription réussie
def test_transcribe_success(transcriber):
    fake_result = {"text": "Ceci est un test de transcription."}
    with patch.object(transcriber, "model", return_value=fake_result):
        result = transcriber.transcribe("test.wav")
        assert result == fake_result


# Test 4 : Simuler une erreur lors de la transcription
def test_transcribe_failure(transcriber):
    with patch.object(
        transcriber, "model", side_effect=Exception("Erreur de transcription")
    ):
        result = transcriber.transcribe("test.wav")
        assert result is None
