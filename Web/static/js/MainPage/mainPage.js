// 헤더 상단 날짜 표시
window.onload = function () {
  const today = new Date();
  const dateElements = {
    past2: document.getElementById("past2"),
    past1: document.getElementById("past1"),
    today: document.getElementById("today"),
    future1: document.getElementById("future1"),
    future2: document.getElementById("future2"),
  };

  const dates = [
    new Date(today.getFullYear(), today.getMonth(), today.getDate() - 2),
    new Date(today.getFullYear(), today.getMonth(), today.getDate() - 1),
    new Date(today.getFullYear(), today.getMonth(), today.getDate()),
    new Date(today.getFullYear(), today.getMonth(), today.getDate() + 1),
    new Date(today.getFullYear(), today.getMonth(), today.getDate() + 2),
  ];

  dateElements.past2.textContent = dates[0].getDate();
  dateElements.past1.textContent = dates[1].getDate();
  dateElements.today.textContent = dates[2].getDate();
  dateElements.future1.textContent = dates[3].getDate();
  dateElements.future2.textContent = dates[4].getDate();
};

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

// 뿡
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

// Todo 관련 함수
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

// Todo 추가
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
      window.location.href = "../templates/ChallengePage/challengePage.html";
    });
  } else {
    console.error("challengeBoxMore 요소를 찾을 수 없습니다.");
  }
});
