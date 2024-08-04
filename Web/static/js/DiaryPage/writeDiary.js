let selectedTodos = [];

// 현재 날짜를 가져와서 표시
window.onload = function () {
  var today = new Date();
  var date =
    today.getFullYear() +
    '년 ' +
    (today.getMonth() + 1) +
    '월 ' +
    today.getDate() +
    '일';
  document.getElementById('current-date').innerText = date;
};

// 모달을 여는 함수
function openModal() {
  document.getElementById('modal').style.display = 'block';
}

// 모달을 닫는 함수
function closeModal() {
  document.getElementById('modal').style.display = 'none';
}

// '오늘의 To Do 불러오기' 클릭 시 모달을 열기
function showTodoModal() {
  openModal();
  fetchTodos(); // 투두리스트 데이터를 데이터베이스에서 로드
}

// '뽀짝이가 답장을 써줄 거예요!' 클릭 시 '/diary/reply'로 이동
function goToReply() {
  window.location.href = '/diary/reply';
}

// 투두리스트 데이터를 데이터베이스에서 로드하고 모달에 표시하는 함수
function fetchTodos() {
  fetch('/todolist') // /todolist 엔드포인트 호출
    .then((response) => response.json())
    .then((data) => {
      const todos = data.filter((todo) => !todo.completed); // check가 false인 투두리스트만 필터링
      displayTodos(todos);
    })
    .catch((error) => console.error('Error fetching todos:', error));
}

// 투두리스트 데이터를 로드하고 모달에 표시하는 함수
function displayTodos(todos) {
  const todoList = document.getElementById('todo-list');
  todoList.innerHTML = '';

  todos.forEach((todo, index) => {
    const todoItem = document.createElement('li');
    todoItem.classList.add('todo-item');

    const checkImg = document.createElement('img');
    checkImg.src = todo.completed
      ? '../../static/img/DiaryPage/checked-fill.svg'
      : '../../static/img/DiaryPage/checked.svg';
    checkImg.classList.add('check-img');

    const pawprintImg = document.createElement('img');
    pawprintImg.src = selectedTodos.includes(todo.text)
      ? '../../static/img/DiaryPage/pawprint-fill.svg'
      : '../../static/img/DiaryPage/pawprint.svg';
    pawprintImg.classList.add('pawprint-img');
    pawprintImg.onclick = () => toggleTodoInDiary(index, todo.text);

    const todoText = document.createElement('span');
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
  const diary = document.querySelector('.diary-textfield');
  const todoItems = document.querySelectorAll('.todo-item');
  const pawprintImg = todoItems[index].querySelector('.pawprint-img');

  if (!selectedTodos.includes(todoText)) {
    selectedTodos.push(todoText);
    pawprintImg.src = '../../static/img/DiaryPage/pawprint-fill.svg';
  } else {
    selectedTodos = selectedTodos.filter((todo) => todo !== todoText);
    pawprintImg.src = '../../static/img/DiaryPage/pawprint.svg';
  }

  updateDiaryText(diary);
}

// 일기 텍스트 업데이트 함수
function updateDiaryText(diary) {
  const todoText = selectedTodos.join('\n');
  const diaryContent = diary.value.split('\n\n');
  diary.value = `${todoText}\n\n${diaryContent.slice(1).join('\n\n')}`;
}

// 일기 텍스트 필드에서 투두리스트가 수정되지 않도록 설정
document.addEventListener('DOMContentLoaded', (event) => {
  const diaryTextField = document.querySelector('.diary-textfield');
  diaryTextField.addEventListener('input', (e) => {
    const todoText = selectedTodos.join('\n');
    if (!diaryTextField.value.startsWith(todoText)) {
      updateDiaryText(diaryTextField);
    }
  });
});
