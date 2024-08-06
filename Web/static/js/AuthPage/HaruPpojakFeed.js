document.getElementById('commentForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const comment = document.getElementById('feedComment').value;

  // 텍스트 입력 후 Polaroid 캡처
  html2canvas(document.getElementById('polaroidWrapper')).then(canvas => {
      const imgBlob = canvas.toBlob(blob => {
          const formData = new FormData();
          formData.append('image', blob, 'polaroid_image.png');
          formData.append('comment', comment);

          fetch('/haru/saveImageWithComment', {
              method: 'POST',
              body: formData,
          })
          .then(response => response.json())
          .then(data => {
              window.location.href = data.downloadUrl;
          })
          .catch(error => console.error('Error:', error));
      }, 'image/png');
  });
});

// 엔터키 입력 시 폼 제출
document
  .getElementById('feedComment')
  .addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
      event.preventDefault();
      document.getElementById('commentForm').submit();
      window.location.href = "/haru/main";
    }
  });

