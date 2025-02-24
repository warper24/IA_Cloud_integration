// script_audio.js

// Prévisualisation de l'audio uploadé
const audioFileInput = document.getElementById('audioFile');
const audioPreviewContainer = document.getElementById('audioPreviewContainer');
const audioPreview = document.getElementById('audioPreview');
const deleteAudioBtn = document.getElementById('deleteAudioBtn');

audioFileInput.addEventListener('change', function() {
  if (audioFileInput.files && audioFileInput.files[0]) {
    const file = audioFileInput.files[0];
    const audioURL = URL.createObjectURL(file);
    audioPreview.src = audioURL;
    audioPreviewContainer.style.display = 'block';
  }
});

deleteAudioBtn.addEventListener('click', function() {
  audioFileInput.value = '';
  audioPreview.src = '';
  audioPreviewContainer.style.display = 'none';
});

// Gestion du formulaire d'upload audio
document.getElementById('uploadForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  
  if (audioFileInput.files.length === 0) {
    alert("Veuillez sélectionner un fichier audio.");
    return;
  }
  const file = audioFileInput.files[0];
  
  const selectedOptions = Array.from(document.querySelectorAll('input[name="options"]:checked')).map(el => el.value);
  if (selectedOptions.length === 0) {
    alert("Veuillez sélectionner au moins une option.");
    return;
  }
  
  const resultsContainer = document.getElementById('resultsContainer');
  resultsContainer.innerHTML = '';
  
  // Mapping des options aux endpoints FastAPI pour l'audio
  const endpoints = {
    subtitles_txt: '/audio_subtitles_txt',
    subtitles_srt: '/audio_subtitles_srt'
  };
  
  for (const option of selectedOptions) {
    const formData = new FormData();
    formData.append('file', file);
    
    const resultItem = document.createElement('div');
    resultItem.className = 'result-item';
    resultItem.innerHTML = `<h3>${option.replace('_', ' ')}</h3><p>Traitement en cours...</p>`;
    resultsContainer.appendChild(resultItem);
    
    try {
      const response = await fetch(endpoints[option], { method: 'POST', body: formData });
      if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        let previewHTML = '';
        if (option === 'subtitles_txt' || option === 'subtitles_srt') {
          const text = await blob.text();
          previewHTML = `<pre class="preview">${text}</pre>`;
        }
        resultItem.innerHTML = `<h3>${option.replace('_', ' ')}</h3>
                                ${previewHTML}
                                <a class="download-btn" href="${url}" download="result_${option}">Télécharger</a>`;
      } else {
        resultItem.innerHTML = `<h3>${option.replace('_', ' ')}</h3><p>Erreur lors du traitement.</p>`;
      }
    } catch (error) {
      console.error(`Erreur pour l'option ${option}:`, error);
      resultItem.innerHTML = `<h3>${option.replace('_', ' ')}</h3><p>Erreur de communication avec le serveur.</p>`;
    }
  }
});
