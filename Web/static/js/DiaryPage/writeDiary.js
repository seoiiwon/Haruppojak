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

// '오늘의 To Do 불러오기' 클릭 시 모달을 열기
function showTodoModal() {
  openModal();
  fetchTodos(); // 투두리스트 데이터를 데이터베이스에서 로드
}

// '뽀짝이가 답장을 써줄 거예요!' 클릭 시 '/diary/reply'로 이동
function goToReply() {
  window.location.href = "/diary/reply";
}

// 투두리스트 데이터를 로드하고 모달에 표시하는 함수
function displayTodos() {
  const todos = [
    { text: "투두리스트 항목 1", completed: false },
    { text: "투두리스트 항목 2", completed: true },
    { text: "투두리스트 항목 3", completed: false },
  ];

  const todoList = document.getElementById("todo-list");
  todoList.innerHTML = "";

  todos.forEach((todo, index) => {
    const todoItem = document.createElement("li");
    todoItem.classList.add("todo-item");

    const checkImg = document.createElement("img");
    checkImg.src = todo.completed
      ? "../../static/img/DiaryPage/checked-fill.svg"
      : "../../static/img/DiaryPage/checked.svg";
    checkImg.classList.add("check-img");

    const pawprintImg = document.createElement("img");
    pawprintImg.src = selectedTodos.includes(todo.text)
      ? "../../static/img/DiaryPage/pawprint-fill.svg"
      : "../../static/img/DiaryPage/pawprint.svg";
    pawprintImg.classList.add("pawprint-img");
    pawprintImg.onclick = () => toggleTodoInDiary(index, todo.text);

    const todoText = document.createElement("span");
    todoText.textContent = todo.text;
    todoText.onclick = () => toggleTodoInDiary(index, todo.text);

    todoItem.appendChild(checkImg);
    todoItem.appendChild(todoText);
    todoItem.appendChild(pawprintImg);

    todoList.appendChild(todoItem);
  });
}

// 투두리스트 항목을 일기에 추가하거나 제거하는 함수
function toggleTodoInDiary(index, todoText) {
  const diary = document.querySelector(".diary-textfield");
  const todoItems = document.querySelectorAll(".todo-item");
  const pawprintImg = todoItems[index].querySelector(".pawprint-img");

  if (!selectedTodos.includes(todoText)) {
    selectedTodos.push(todoText);
    pawprintImg.src = "../../static/img/DiaryPage/pawprint-fill.svg";
  } else {
    selectedTodos = selectedTodos.filter((todo) => todo !== todoText);
    pawprintImg.src = "../../static/img/DiaryPage/pawprint.svg";
  }

  updateDiaryText(diary);
}

// 일기 텍스트 업데이트 함수
function updateDiaryText(diary) {
  const todoText = selectedTodos.join("\n");
  const diaryContent = diary.value.split("\n\n");
  diary.value = `${todoText}\n\n${diaryContent.slice(1).join("\n\n")}`;
}

// 일기 텍스트 필드에서 투두리스트가 수정되지 않도록 설정
document.addEventListener("DOMContentLoaded", (event) => {
  const diaryTextField = document.querySelector(".diary-textfield");
  diaryTextField.addEventListener("input", (e) => {
    const todoText = selectedTodos.join("\n");
    if (!diaryTextField.value.startsWith(todoText)) {
      updateDiaryText(diaryTextField);
    }
  });
});

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
      alert(`Error: ${error.detail || response.statusText}`);
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
