document.addEventListener('DOMContentLoaded', function () {
  const calendarBody = document.querySelector('.calendar-body');
  const diaries = window.diaries || []; // 전역 범위로 정의된 diaries 변수 접근, 초기화
  console.log(diaries); // 데이터를 콘솔에 출력하여 확인

  function createCalendar(year, month) {
    const firstDay = new Date(year, month, 1).getDay();
    const lastDate = new Date(year, month + 1, 0).getDate();
    const prevLastDate = new Date(year, month, 0).getDate();

    let dates = [];
    // Add previous month's dates
    for (let i = firstDay; i > 0; i--) {
      dates.push(`<div class="date other-month">${prevLastDate - i + 1}</div>`);
    }
    // Add current month's dates
    for (let i = 1; i <= lastDate; i++) {
      const today = new Date();
      const isToday =
        today.getFullYear() === year &&
        today.getMonth() === month &&
        today.getDate() === i;
      const hasDiary = diaries.some(
        (diary) => new Date(diary.Date).getDate() === i
      );
      let className = 'date current-month';
      let style = '';
      let cursorStyle = '';

      if (isToday) {
        className += ' today';
        style = 'background-color: #2F4858; border-radius: 14px;';
        cursorStyle = 'cursor: pointer;';
      } else if (hasDiary) {
        className += ' diary-day';
        style = 'background-color: #95B1AE; border-radius: 14px;';
        cursorStyle = 'cursor: pointer;';
      } else if (new Date(year, month, i) > today) {
        cursorStyle = 'cursor: not-allowed;';
      }

      dates.push(
        `<div class="${className}" style="${style}${cursorStyle}" data-date="${year}-${
          month + 1
        }-${i}">${i}</div>`
      );
    }
    // Add next month's dates to fill the calendar
    const nextDays = 42 - dates.length;
    for (let i = 1; i <= nextDays; i++) {
      dates.push(`<div class="date other-month">${i}</div>`);
    }

    calendarBody.innerHTML = dates.join('');

    // 날짜 클릭 이벤트 추가
    document.querySelectorAll('.date.current-month').forEach((dateElem) => {
      dateElem.addEventListener('click', function () {
        const date = new Date(this.getAttribute('data-date'));
        const today = new Date();
        today.setHours(0, 0, 0, 0); // 시간을 0으로 설정하여 날짜만 비교

        if (date > today) {
          alert('미래 날짜는 선택할 수 없어요!');
        } else {
          window.location.href = `/diary/calendar/${this.getAttribute(
            'data-date'
          )}`;
        }
      });
    });
  }

  createCalendar(new Date().getFullYear(), new Date().getMonth());
});

// Function to navigate back to reply.html
function goBack() {
  window.history.back();
}

// Function to close the app by navigating to closeApp.html
function closeApp() {
  window.location.href = 'close';
}

function closeModal() {
  document.getElementById('diaryModal').style.display = 'none';
}

// Modal 관련 함수
function showModal(content) {
  const modal = document.getElementById('diaryModal');
  modal.querySelector('.modal-body').innerHTML = content;
  modal.style.display = 'block';
}

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
      showModal(data);
    });
}
