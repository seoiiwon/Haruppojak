// 현재 날짜를 가져와서 표시
window.onload = function () {
  var today = new Date();
  var dayNames = [
    '일요일',
    '월요일',
    '화요일',
    '수요일',
    '목요일',
    '금요일',
    '토요일',
  ];
  var date =
    today.getFullYear() +
    '년 ' +
    (today.getMonth() + 1) +
    '월 ' +
    today.getDate() +
    '일 ' +
    dayNames[today.getDay()];
  document.getElementById('current-date').innerText = date;
};

// '돌아가기' 클릭 시 이전 페이지로 이동
function goBack() {
  window.history.back();
}

// '뽀짝일기 달력' 클릭 시 diaryCalendar.html 페이지로 이동
function goToCalendar() {
  window.location.href = 'calendar';
}

// '뽀짝 종료' 클릭 시 closeApp.html 페이지로 이동
function closeApp() {
  window.location.href = 'close';
}
