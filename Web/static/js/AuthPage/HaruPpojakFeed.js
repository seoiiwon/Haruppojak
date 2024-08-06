document
  .getElementById('commentForm')
  .addEventListener('submit', async function (event) {
    event.preventDefault(); // 폼 제출 기본 동작 방지

    const commentInput = document.getElementById('feedComment');
    const comment = commentInput.value;

    const proofshot = {
      photoComment: comment,
    };

    try {
      const response = await fetch('/haru/upload/comment', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(proofshot),
      });

      if (response.ok) {
        const responseData = await response.json();
        console.log('Comment uploaded successfully:', responseData);
        window.location.href = '/haru/main'; // 성공 시 이동할 페이지
      } else {
        console.error(
          'Failed to upload comment:',
          response.status,
          response.statusText
        );
      }
    } catch (error) {
      console.error('Error uploading comment:', error);
    }
  });

// 엔터키 입력 시 폼 제출
document
  .getElementById('feedComment')
  .addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
      event.preventDefault();
      document.getElementById('commentForm').submit();
    }
  });

