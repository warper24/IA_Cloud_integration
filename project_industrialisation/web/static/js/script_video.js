// script_video.js

// Prévisualisation de la vidéo uploadée
const videoFileInput = document.getElementById('videoFile');
const videoPreviewContainer = document.getElementById('videoPreviewContainer');
const videoPreview = document.getElementById('videoPreview');
const deleteVideoBtn = document.getElementById('deleteVideoBtn');

videoFileInput.addEventListener('change', function() {
  if (videoFileInput.files && videoFileInput.files[0]) {
    const file = videoFileInput.files[0];
    const videoURL = URL.createObjectURL(file);
    videoPreview.src = videoURL;
    videoPreviewContainer.style.display = 'block';
  }
});

deleteVideoBtn.addEventListener('click', function() {
  videoFileInput.value = '';
  videoPreview.src = '';
  videoPreviewContainer.style.display = 'none';
});

// Gestion du formulaire d'upload vidéo
document.getElementById('uploadForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  
  if (videoFileInput.files.length === 0) {
    alert("Veuillez sélectionner une vidéo.");
    return;
  }
  const file = videoFileInput.files[0];
  
  const selectedOptions = Array.from(document.querySelectorAll('input[name="options"]:checked')).map(el => el.value);
  if (selectedOptions.length === 0) {
    alert("Veuillez sélectionner au moins une option.");
    return;
  }
  
  const resultsContainer = document.getElementById('resultsContainer');
  resultsContainer.innerHTML = '';
  
  // Mapping des options aux endpoints FastAPI pour la vidéo
  const endpoints = {
    subtitles_txt: '/subtitles_txt',
    video_hard: '/video_hard',
    video_srt: '/video_srt',
    subtitles_srt: '/subtitles_srt'
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
        } else if (option === 'video_hard' || option === 'video_srt') {
          previewHTML = `<video class="preview" controls width="100%">
                          <source src="${url}" type="video/mp4">
                          Votre navigateur ne supporte pas la vidéo.
                         </video>`;
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
