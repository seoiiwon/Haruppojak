let dates = [];
let dateElements = {};

// 헤더 상단 날짜 표시
window.onload = function () {
  const today = new Date();
  dateElements = {
    past2: document.getElementById("past2"),
    past1: document.getElementById("past1"),
    today: document.getElementById("today"),
    future1: document.getElementById("future1"),
    future2: document.getElementById("future2"),
  };

  dates = [
    new Date(today.getFullYear(), today.getMonth(), today.getDate() - 2),
    new Date(today.getFullYear(), today.getMonth(), today.getDate() - 1),
    new Date(today.getFullYear(), today.getMonth(), today.getDate()),
    new Date(today.getFullYear(), today.getMonth(), today.getDate() + 1),
    new Date(today.getFullYear(), today.getMonth(), today.getDate() + 2),
  ];

  updateDateElements();

  for (const [key, element] of Object.entries(dateElements)) {
    element.addEventListener("click", function () {
      handleDateClick(key);
    });
  }
};

// dateElements 값 반영
function updateDateElements() {
  dateElements.past2.textContent = dates[0].getDate();
  dateElements.past1.textContent = dates[1].getDate();
  dateElements.today.textContent = dates[2].getDate();
  dateElements.future1.textContent = dates[3].getDate();
  dateElements.future2.textContent = dates[4].getDate();
}

// Todo 항목 불러오기
function handleDateClick(clickedDate) {
  const dateOrder = ["past2", "past1", "today", "future1", "future2"];
  const clickedIndex = dateOrder.indexOf(clickedDate);

  if (clickedIndex !== -1) {
    dates = dateOrder.map((_, index) => {
      return new Date(
        dates[clickedIndex].getFullYear(),
        dates[clickedIndex].getMonth(),
        dates[clickedIndex].getDate() + index - 2
      );
    });

    updateDateElements();
    fetchTodosForDate(dates[2]);
  }
}

// Todo 화면에 표시하기
function fetchTodosForDate(date) {
  const formattedDate = `${date.getFullYear()}-${String(
    date.getMonth() + 1
  ).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;

  fetch(`/todo/date/${formattedDate}`, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => {
      const todoListContainer = document.getElementById("todoListContainer");
      todoListContainer.innerHTML = ""; // 기존 항목 제거
      data.todos.forEach((todo) => {
        const todoItem = createTodoElement(todo);
        todoListContainer.appendChild(todoItem);
      });
    })
    .catch((error) => console.error("Error fetching todos:", error));
}

// 뽀짝챌 자동으로 넘어가기
document.addEventListener("DOMContentLoaded", function () {
  const boxContainer = document.querySelector(".challenges .challengeList");
  let scrollAmount = 0;

  const box = boxContainer.querySelector(".challengeBox");
  const boxStyle = getComputedStyle(box);
  const boxWidth =
    box.offsetWidth +
    parseFloat(boxStyle.marginLeft) +
    parseFloat(boxStyle.marginRight);
  const scrollStep = boxWidth * 2;

  function scrollBoxes() {
    if (scrollAmount >= boxContainer.scrollWidth - boxContainer.offsetWidth) {
      scrollAmount = 0;
    } else {
      scrollAmount += scrollStep;
    }
    boxContainer.scrollTo({
      left: scrollAmount,
      behavior: "smooth",
    });
  }

  setInterval(scrollBoxes, 5000);
});

// 뽀짝챌 스크롤 도트
document.addEventListener("DOMContentLoaded", function () {
  const boxContainer = document.querySelector(".challenges .challengeList");
  const dotsContainer = document.querySelector(".dots");
  const boxes = boxContainer.querySelectorAll(".challengeBox");
  let scrollAmount = 0;
  const boxStyle = getComputedStyle(boxes[0]);
  const boxWidth =
    boxes[0].offsetWidth +
    parseFloat(boxStyle.marginLeft) +
    parseFloat(boxStyle.marginRight);
  const scrollStep = boxWidth * 2;

  boxes.forEach((_, index) => {
    const dot = document.createElement("div");
    dot.classList.add("dot");
    if (index === 0) {
      dot.classList.add("active");
    }
    dotsContainer.appendChild(dot);
  });

  const dots = dotsContainer.querySelectorAll(".dot");

  function scrollBoxes() {
    if (scrollAmount >= boxContainer.scrollWidth - boxContainer.offsetWidth) {
      scrollAmount = 0;
    } else {
      scrollAmount += scrollStep;
    }
    boxContainer.scrollTo({
      left: scrollAmount,
      behavior: "smooth",
    });

    const activeIndex = Math.floor(scrollAmount / boxWidth) % boxes.length;
    dots.forEach((dot, index) => {
      dot.classList.toggle("active", index === activeIndex);
    });
  }

  setInterval(scrollBoxes, 5000);
});

// Todo
document.addEventListener("DOMContentLoaded", function () {
  fetchTodos();

  document
    .getElementById("addTodoButton")
    .addEventListener("click", function () {
      addTodoItem();
    });
});

// Todo 표시
function fetchTodos() {
  fetch("/todo/all", {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => {
      const todoListContainer = document.getElementById("todoListContainer");
      data.todos.forEach((todo) => {
        const todoItem = createTodoElement(todo);
        todoListContainer.appendChild(todoItem);
      });
    })
    .catch((error) => console.error("Error fetching todos:", error));
}

//
function createTodoElement(todo) {
  const li = document.createElement("li");
  const button = document.createElement("input");
  button.type = "button";
  button.checked = todo.completed;
  const input = document.createElement("input");
  input.type = "text";
  input.value = todo.content;
  input.className = "todoContent";
  li.appendChild(button);
  li.appendChild(input);
  return li;
}

//
function addTodoItem() {
  const todoListContainer = document.getElementById("todoListContainer");
  const li = document.createElement("li");
  const button = document.createElement("input");
  button.type = "button";
  const hr = document.createElement("hr");
  const input = document.createElement("input");
  input.type = "text";
  input.placeholder = "오늘의 투두를 입력해주세요.";
  input.className = "todoContent";
  li.appendChild(button);
  li.appendChild(input);
  li.appendChild(hr);
  todoListContainer.appendChild(li);
  input.focus();
}

// 챌린지 페이지 넘어가기
document.addEventListener("DOMContentLoaded", function () {
  var challengeBoxMore = document.querySelector(".challengeBoxMore");

  if (challengeBoxMore) {
    challengeBoxMore.addEventListener("click", function () {
      window.location.href = "/templates/ChallengePage/challengePage.html";
    });
  } else {
    console.error("challengeBoxMore 요소를 찾을 수 없습니다.");
  }
});
