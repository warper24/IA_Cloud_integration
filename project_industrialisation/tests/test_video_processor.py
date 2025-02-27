import pytest
import sys
from unittest.mock import patch, MagicMock
sys.path.insert(0, "C:/Users/aysim/Documents/Ynov/I.A. dans Cloud/j1/fil_rouge/IA_Cloud_integration/project_industrialisation")
from utils.video_processor import VideoProcessor



@pytest.fixture
def video_processor():
    return VideoProcessor("test.mp4", "test.srt", "output.mp4")

# Test 1 : Vérifier la validation des fichiers
@pytest.mark.parametrize("missing_file", ["video", "subtitles"])
def test_validate_files_missing(missing_file, video_processor):
    with patch("os.path.exists", side_effect=lambda path: path != ("test.mp4" if missing_file == "video" else "test.srt")):
        with pytest.raises(FileNotFoundError, match="introuvable"):
            video_processor.validate_files()

# Test 2 : Vérifier la conversion d'un fichier SRT en ASS
def test_convert_srt_to_ass(video_processor):
    with patch("ffmpeg.input") as mock_ffmpeg:
        mock_output = MagicMock()
        mock_ffmpeg.return_value.output.return_value = mock_output
        mock_output.run.return_value = None
        
        result = video_processor.convert_srt_to_ass()
        assert result == "test.ass"
        mock_ffmpeg.assert_called_once_with("test.srt", format="srt")
        mock_output.run.assert_called_once_with(overwrite_output=True)

# Test 3 : Vérifier l'ajout de sous-titres à une vidéo
def test_add_subtitles(video_processor, mocker):
    # Mock des méthodes utilisées dans add_subtitles()
    mocker.patch.object(video_processor, "validate_files")
    mocker.patch.object(video_processor, "convert_srt_to_ass", return_value="test.ass")

    # Simuler l'existence du fichier .ass après conversion
    mocker.patch("os.path.exists", return_value=True)

    # Mock ffmpeg
    mock_ffmpeg = mocker.patch("ffmpeg.input")
    mock_output = mocker.MagicMock()
    mock_ffmpeg.return_value.output.return_value = mock_output
    mock_output.run.return_value = None

    # Exécution de la méthode
    video_processor.add_subtitles()

    # Vérifier que toutes les méthodes ont bien été appelées
    video_processor.validate_files.assert_called_once()
    video_processor.convert_srt_to_ass.assert_called_once()
    mock_ffmpeg.assert_called_once_with(video_processor.video_path)