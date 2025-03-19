document.addEventListener("DOMContentLoaded", () => {
  const audioFileInput = document.getElementById("file");
  const audioPreviewContainer = document.getElementById("audioPreviewContainer");
  const audioPreview = document.getElementById("audioPreview");
  const deleteAudioBtn = document.getElementById("deleteAudioBtn");

  if (audioFileInput && audioPreviewContainer && audioPreview && deleteAudioBtn) {
      audioFileInput.addEventListener("change", () => {
          const file = audioFileInput.files[0];
          if (file) {
              const url = URL.createObjectURL(file);
              audioPreview.src = url;
              audioPreviewContainer.style.display = "block";
          }
      });

      deleteAudioBtn.addEventListener("click", () => {
          audioFileInput.value = "";
          audioPreview.src = "";
          audioPreviewContainer.style.display = "none";
      });
  }
});
