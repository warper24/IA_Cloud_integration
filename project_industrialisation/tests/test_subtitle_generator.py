import pytest
import os
import sys
sys.path.insert(0, "C:/Users/aysim/Documents/Ynov/I.A. dans Cloud/j1/fil_rouge/IA_Cloud_integration/project_industrialisation")
from utils.subtitle_generator import SubtitleGenerator


@pytest.fixture
def sample_transcription():
    return {
        "chunks": [
            {"timestamp": (0.5, 3.0), "text": "Bonjour tout le monde."},
            {"timestamp": (4.0, 7.0), "text": "Ceci est un test."}
        ]
    }

@pytest.fixture
def subtitle_generator(sample_transcription):
    return SubtitleGenerator("test.mp4", sample_transcription)

# Test 1 : Vérifier le format de temps
@pytest.mark.parametrize("seconds, expected", [
    (0.5, "00:00:00,500"),
    (61.2, "00:01:01,200"),
    (3600.99, "01:00:00,990"),
    (3661.7, "01:01:01,700")
])
def test_format_time(subtitle_generator, seconds, expected):
    assert subtitle_generator.format_time(seconds) == expected

# Test 2 : Vérifier la génération de sous-titres
def test_generate_subtitles(subtitle_generator):
    subtitle_file, transcript_file = subtitle_generator.generate_subtitles()
    
    assert os.path.exists(subtitle_file)
    assert os.path.exists(transcript_file)
    
    with open(subtitle_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "1\n00:00:00,500 --> 00:00:03,000\nBonjour tout le monde." in content
        assert "2\n00:00:04,000 --> 00:00:07,000\nCeci est un test." in content
    
    with open(transcript_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Bonjour tout le monde." in content
        assert "Ceci est un test." in content

# Test 3 : Vérifier le comportement avec une transcription vide
def test_generate_subtitles_empty():
    generator = SubtitleGenerator("test.mp4", {"chunks": []})
    subtitle_file, transcript_file = generator.generate_subtitles()
    
    assert os.path.exists(subtitle_file)
    assert os.path.exists(transcript_file)
    
    with open(subtitle_file, "r", encoding="utf-8") as f:
        assert f.read().strip() == ""
    
    with open(transcript_file, "r", encoding="utf-8") as f:
        assert f.read().strip() == ""
