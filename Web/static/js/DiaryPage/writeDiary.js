let selectedTodos = [];

// 현재 날짜를 가져와서 표시
window.onload = function () {
  var today = new Date();
  var date =
    today.getFullYear() +
    "년 " +
    (today.getMonth() + 1) +
    "월 " +
    today.getDate() +
    "일";
  document.getElementById("current-date").innerText = date;
};

// 모달을 여는 함수
function openModal() {
  document.getElementById("modal").style.display = "block";
}

// 모달을 닫는 함수
function closeModal() {
  document.getElementById("modal").style.display = "none";
}

// '뽀짝이가 답장을 써줄 거예요!' 클릭 시 '/diary/reply'로 이동
function goToReply() {
  window.location.href = "/diary/reply";
}

// '오늘의 To Do 불러오기' 클릭 시 모달을 열기
function showTodoModal() {
  openModal();
}

async function submitDiary() {
  let content = document.getElementById("diary-content").value;
  // let todo = document.getElementById("todo-list").value;

  let diaryData = {
    content: content,
    todo: "",
    response: "",
    id: 0, // 서버에서 사용자 ID를 설정합니다.
  };

  console.log("Sending diary data:", diaryData); // 요청 전 데이터를 로그로 확인

  try {
    const response = await fetch("/diary/write", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${getAuthToken()}`,
      },
      body: JSON.stringify(diaryData),
    });

    console.log("Server response status:", response.status); // 상태 코드 로그 확인

    if (response.ok) {
      const result = await response.json();
      alert("뽀짝일기 쓰기 성공!");
      goToReply(); // 저장이 완료되면 답장 페이지로 이동
    } else {
      const error = await response.json();
      console.error("Error response:", error); // 오류 로그 확인
      alert(`${error.detail}`);
    }
  } catch (error) {
    console.error("Fetch error:", error); // 예외 로그 확인
    alert(`Fetch Error: ${error.message}`);
  }
}

function getAuthToken() {
  // 브라우저의 로컬 스토리지 또는 쿠키에서 토큰을 가져오는 함수
  return localStorage.getItem("access_token");
}
