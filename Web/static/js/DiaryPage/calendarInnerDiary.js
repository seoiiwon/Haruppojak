document.addEventListener('DOMContentLoaded', function () {
  const diaryContainer = document.querySelector('.innerDiary-container');
  const diary = JSON.parse('{{ diary | tojson | safe }}'); // 서버에서 전달된 일기 데이터

  diaryContainer.innerHTML = diary.Diarycontent;
  diaryContainer.setAttribute('data-date', diary.Date);

  document.getElementById('show-reply').addEventListener('click', function () {
    showReply();
  });
});

// 모달 관련 함수
function closeReplyModal() {
  document.getElementById('replyModal').style.display = 'none';
}

function showReply() {
  const date = document
    .querySelector('.innerDiary-container')
    .getAttribute('data-date');
  fetch(`/diary/reply/${date}`)
    .then((response) => response.text())
    .then((data) => {
      const modal = document.getElementById('replyModal');
      modal.querySelector('.modal-body').innerHTML = data;
      modal.style.display = 'block';
    });
}
