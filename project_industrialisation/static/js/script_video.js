document.addEventListener("DOMContentLoaded", () => {
  const videoFileInput = document.getElementById("file");
  const videoPreviewContainer = document.getElementById("videoPreviewContainer");
  const videoPreview = document.getElementById("videoPreview");
  const deleteVideoBtn = document.getElementById("deleteVideoBtn");

  if (videoFileInput && videoPreviewContainer && videoPreview && deleteVideoBtn) {
      videoFileInput.addEventListener("change", () => {
          const file = videoFileInput.files[0];
          if (file) {
              const url = URL.createObjectURL(file);
              videoPreview.src = url;
              videoPreviewContainer.style.display = "block";
          }
      });

      deleteVideoBtn.addEventListener("click", () => {
          videoFileInput.value = "";
          videoPreview.src = "";
          videoPreviewContainer.style.display = "none";
      });
  }
});
