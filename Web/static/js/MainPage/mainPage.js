// 페이지 연결
// function fetchTodos() {
//   fetch("/haru/main", {
//     method: "GET",
//   })
//     .then((response) => response.json())
//     .then((data) => {
//       const todoListContainer = document.getElementById("todoListContainer");
//       data.todos.forEach((todo) => {
//         const todoItem = createTodoElement(todo);
//         todoListContainer.appendChild(todoItem);
//       });
//     })
//     .catch((error) => console.error("Error fetching todos:", error));
// }

// todo 수정 및 삭제
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".optionBtn").forEach((button) => {
    button.addEventListener("click", function () {
      const options = button.nextElementSibling;
      options.style.display =
        options.style.display === "none" ? "block" : "none";
    });
  });

  document.querySelectorAll(".editTodo").forEach((button) => {
    button.addEventListener("click", function () {
      const todoId = button.getAttribute("data-id");
      const todoListContainer = button.closest(".todoListContainer");
      if (!todoListContainer) {
        console.error("Cannot find .todoListContainer");
        return;
      }
      const todoTextElement = todoListContainer.querySelector(".todoText");
      if (!todoTextElement) {
        console.error("Cannot find .todoText");
        return;
      }
      const currentTodoText = todoTextElement.innerText;
      const newTodo = prompt("새로운 할 일을 입력하세요:", currentTodoText);

      if (newTodo) {
        fetch(`/todo/update/${todoId}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            id: parseInt(todoId),
            todowrite: newTodo,
          }),
        })
          .then((response) => {
            console.log("Response status:", response.status);
            if (!response.ok) {
              throw new Error("Network response was not ok");
            }
            return response.json();
          })
          .then((data) => {
            console.log("Response data:", data);
            if (data.success) {
              todoTextElement.innerText = newTodo;
              alert("수정됨");
            } else {
              alert("수정안되.");
            }
          })
          .catch((error) => {
            console.error("Error:", error);
            alert("수정오류 ㅅㄱ");
          });
      }
    });
  });

  // 삭제 버튼 클릭 시
  document.querySelectorAll(".deleteTodo").forEach((button) => {
    button.addEventListener("click", function () {
      const todoId = button.getAttribute("data-id");
      if (confirm("정말 삭제하시겠습니까?")) {
        fetch(`/todo/delete/${todoId}`, {
          method: "DELETE",
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              const todoItem = button.closest(".todoListContainer");
              todoItem.remove();
              alert("삭제되었습니다.");
            } else {
              alert("삭제에 실패했습니다.");
            }
          })
          .catch((error) => {
            console.error("Error:", error);
            alert("삭제오류 ㅅㄱ");
          });
      }
    });
  });
});

// 날짜 및 날짜 요소 배열 생성
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

// 날짜 클릭 시 해당 날짜로 이동
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

// 날짜 투두 불러오기
function fetchTodosForDate(date) {
  const formattedDate = `${date.getFullYear()}-${String(
    date.getMonth() + 1
  ).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;

  fetch(`/haru/main?date=${formattedDate}`, {
    method: "GET",
  })
    .then((response) => response.text())
    .then((html) => {
      const todoListContainer = document.getElementById("todoListContainer");
      const tempElement = document.createElement("div");
      tempElement.innerHTML = html;

      const newTodoList = tempElement.querySelector("#todoListContainer");
      if (newTodoList) {
        todoListContainer.innerHTML = newTodoList.innerHTML;
      }
    })
    .catch((error) => console.error("Error fetching todos:", error));
}

// 투두 추가
function addEnterKeyListener(inputText) {
  inputText.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      event.stopPropagation();

      inputText.disabled = true;

      const plusImage = inputText.previousSibling;
      plusImage.src = "../../static/img/MainPage/checkboxWhite.svg";
      const todoText = inputText.value;

      let url = "/todo/create";
      let payload = JSON.stringify({ todowrite: todoText });

      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: payload,
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then(() => {
          location.reload();
        })
        .catch((error) => console.error("Error:", error));
    }
  });
}

// html에 투두 추가하기
function addTodoItem() {
  const todoListContainer = document.getElementById("addTodoList");
  const li = document.createElement("li");
  const div = document.createElement("div");
  const plus = document.createElement("img");
  const inputText = document.createElement("input");
  const hr = document.createElement("hr");

  li.className = "todoListContainer";
  plus.src = "../../static/img/MainPage/addTodoButton.svg";
  inputText.type = "text";
  inputText.placeholder = "투두 추가하기";
  inputText.className = "todoContent";

  div.appendChild(plus);
  div.appendChild(inputText);
  div.appendChild(hr);
  li.appendChild(div);
  todoListContainer.appendChild(li);

  addEnterKeyListener(inputText);
}

document.addEventListener("DOMContentLoaded", function () {
  const initialInput = document.querySelector("#addTodoList .todoContent");
  if (initialInput) {
    addEnterKeyListener(initialInput);
  }
});

// 추가 이미지에서 체크박스 이미지로 변경
document.addEventListener("DOMContentLoaded", (event) => {
  const inputField = document.getElementById("firstWrite");
  const changeCheckbox = document.getElementById("firstAdd");

  inputField.addEventListener("keypress", (event) => {
    changeImage();
  });

  function changeImage() {
    changeCheckbox.src = "../../static/img/MainPage/checkboxWhite.svg";
  }
});

// 추천 뽀짝 숨기기
function hiddenRecommendTodo(element) {
  if (!element) {
    console.error("Element is undefined");
    return;
  }
  const maegae = element.parentNode;
  const ppojakRecommend = maegae.parentNode;
  const todoText = maegae.querySelector(".todoText").innerText;

  if (ppojakRecommend) {
    alert("추가되었습니다.");
    ppojakRecommend.style = "display: none;";
    let url = "/todo/create";
    let payload = JSON.stringify({ todowrite: todoText });

    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: payload,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then(() => {
        location.reload();
      })
      .catch((error) => console.error("Error:", error));
  } else {
    console.error("Parent node not found");
  }
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

// 챌린지 페이지 넘어가기
document.addEventListener("DOMContentLoaded", function () {
  var challengeBoxMore = document.getElementById("challengeBoxMore");
  challengeBoxMore.addEventListener("click", function () {
    window.location.href = "/challenge/all";
  });
});

function openModal(modalId) {
  document.getElementById(modalId).style.display = "block";
}

function closeModal(modalId) {
  document.getElementById(modalId).style.display = "none";
}

window.onclick = function (event) {
  const modals = document.getElementsByClassName("modal");
  for (let i = 0; i < modals.length; i++) {
    if (event.target == modals[i]) {
      modals[i].style.display = "none";
    }
  }
};

function openModal(modalId) {
  document.getElementById(modalId).style.display = "block";
}

function closeModal(modalId) {
  document.getElementById(modalId).style.display = "none";
}

window.onclick = function (event) {
  const modals = document.getElementsByClassName("modal");
  for (let i = 0; i < modals.length; i++) {
    if (event.target == modals[i]) {
      modals[i].style.display = "none";
    }
  }
};
