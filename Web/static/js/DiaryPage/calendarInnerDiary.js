document.addEventListener("DOMContentLoaded", function () {
  const diaryContainer = document.querySelector(".innerDiary-container");
  const diary = JSON.parse("{{ diary | tojson | safe }}"); // 서버에서 전달된 일기 데이터

  diaryContainer.innerHTML = diary.Diarycontent;
  diaryContainer.setAttribute("data-date", diary.Date);
});

document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("myModal");
  const openModalButton = document.getElementById("show-reply");
  const closeModalButton = document.querySelector("#myModal .close");

  // 모달 열기
  openModalButton.onclick = function () {
    modal.style.display = "block";
  };

  // 모달 닫기
  closeModalButton.onclick = function () {
    modal.style.display = "none";
  };

  // 모달 외부 클릭 시 닫기
  window.onclick = function (event) {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  };
});

// Function to navigate back to reply.html
function goBack() {
  window.history.back();
}

// Function to close the app by navigating to closeApp.html
function closeApp() {
  window.location.href = "/diary/close";
}
