//페이지 연결
function fetchTodos() {
  fetch("/haru/main", {
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

document.addEventListener("DOMContentLoaded", function () {
  // 옵션 버튼 클릭 시 수정, 삭제 버튼 표시
  document.querySelectorAll(".options-btn").forEach((button) => {
    button.addEventListener("click", function () {
      const options = button.nextElementSibling;
      options.style.display =
        options.style.display === "none" ? "block" : "none";
    });
  });

  document.querySelectorAll(".edit-todo").forEach((button) => {
    button.addEventListener("click", function () {
      const todoId = button.getAttribute("data-id");

      // 현재 ToDo 텍스트를 가져옴
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
        // const checkBox = todoListContainer.querySelector(".todoCheck");
        // if (!checkBox) {
        //   console.error("Cannot find .todoCheck");
        //   return;
        // }

        // console.log(checkBox.dataset.checked);
        // const isChecked = function () {
        //   if (checkBox.dataset.checked) {
        //     return true;
        //   } else {
        //     return false;
        //   }
        // };
        // const userId = todoListContainer.getAttribute("data-user-id");

        // console.log("Sending update request for todoId:", todoId);
        // console.log("New todo text:", newTodo);
        // console.log("Checkbox status:", isChecked());

        let url = `/todo/update/${todoId}`;
        let asdf = {
          id: parseInt(todoId),
          todowrite: newTodo,
          // todocheck: isChecked(),
        };

        fetch(`/todo/update/${todoId}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            id: parseInt(todoId),
            todowrite: newTodo,
            // todocheck: isChecked(),
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
            alert("오류 ㅅㄱ.");
          });
      }
    });
  });

  // 삭제 버튼 클릭 시
  document.querySelectorAll(".delete-todo").forEach((button) => {
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
            alert("삭제 중 오류가 발생했습니다.");
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
        todoListContainer.innerHTML = newTodoList.innerHTML; // 기존 항목 제거 후 새 항목 추가
      }
    })
    .catch((error) => console.error("Error fetching todos:", error));
}

// 투두 추가 - 더 수정하기
// 이벤트 리스너를 등록하는 함수
function addEnterKeyListener(inputText) {
  inputText.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      event.stopPropagation();
      console.log(`뿡`);
      addTodoItem();
      const todoContentInputs = document.getElementsByClassName("todoContent");
      const nextInputIndex =
        Array.from(todoContentInputs).indexOf(inputText) + 1;
      console.log(`${todoContentInputs}`);
      console.log(`${nextInputIndex}`);
      if (todoContentInputs[nextInputIndex]) {
        todoContentInputs[nextInputIndex].focus();
      }
    }
  });
}

// addTodoItem 함수
function addTodoItem() {
  const todoListContainer = document.getElementById("addTodoList");
  const li = document.createElement("li");
  const div = document.createElement("div");
  const plus = document.createElement("img");
  const inputText = document.createElement("input");
  const hr = document.createElement("hr");

  plus.src = "../../static/img/MainPage/addTodoButton.svg";
  // plus.src = "{{ url_for('static', path='img/MainPage/addTodoButton.svg')}}";
  inputText.type = "text";
  inputText.placeholder = "투두 추가하기";
  inputText.className = "todoContent";

  div.appendChild(plus);
  div.appendChild(inputText);
  div.appendChild(hr);
  li.appendChild(div);
  todoListContainer.appendChild(li);

  addEnterKeyListener(inputText);

  inputText.focus();
}

document.addEventListener("DOMContentLoaded", function () {
  const initialInput = document.querySelector("#addTodoList .todoContent");
  if (initialInput) {
    addEnterKeyListener(initialInput);
    initialInput.focus();
  }
});

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

// static/js/MainPage/mainPage.js
function showChallengeModal(challId) {
  fetchChallenge(challId);
  openModal();
}

function fetchChallenge(challId) {
  // 예시 데이터입니당.. 나중에 실제 API 호출하면 될 것 같아요
  var challengeData = {
    chall1: {
      title: "밀리의 서재 #독서",
      participants: "100명 참여중",
      description: "밀리의 서재 챌린지 설명",
      images: [
        "https://via.placeholder.com/300x150",
        "https://via.placeholder.com/300x150",
      ],
    },
    chall2: {
      title: "1일 1커밋 #코딩",
      participants: "200명 참여중",
      description: "1일 1커밋 챌린지 설명",
      images: [
        "https://via.placeholder.com/300x150",
        "https://via.placeholder.com/300x150",
      ],
    },
    chall3: {
      title: "냠냠 #요리",
      participants: "150명 참여중",
      description: "냠냠 챌린지 설명",
      images: [
        "https://via.placeholder.com/300x150",
        "https://via.placeholder.com/300x150",
      ],
    },
    chall4: {
      title: "다른 챌린지 #기타",
      participants: "50명 참여중",
      description: "다른 챌린지 설명",
      images: [
        "https://via.placeholder.com/300x150",
        "https://via.placeholder.com/300x150",
      ],
    },
  };

  var modalText = document.getElementById("modalText");
  var data = challengeData[challId];

  modalText.innerHTML = `
    <div class="carousel">
      ${data.images
        .map((src) => `<img src="${src}" alt="Challenge Image">`)
        .join("")}
    </div>
    <h2 class="challenge-title">${data.title}</h2>
    <p class="participants-count">${data.participants}</p>
    <p class="challenge-description">${data.description}</p>
  `;

  // 자동 슬라이드 설정
  const carouselInner = document.querySelector(".carousel-inner");
  let index = 0;

  function slideImages() {
    index++;
    if (index >= data.images.length) {
      index = 0;
    }
    carouselInner.style.transform = `translateX(-${index * 100}%)`;
  }

  setInterval(slideImages, 5000);
}

function openModal() {
  var modal = document.getElementById("modal");
  modal.style.display = "block";
}

function closeModal() {
  var modal = document.getElementById("modal");
  modal.style.display = "none";
}

document.addEventListener("DOMContentLoaded", function () {
  // 각 challengeBox 클릭 시 showChallengeModal 함수 호출
  document.querySelectorAll(".challengeBox").forEach(function (box) {
    box.addEventListener("click", function () {
      var challengeId = this.getAttribute("data-challenge-id");
      showChallengeModal(challengeId);
    });
  });

  // 모달 외부 클릭 시 모달 닫기
  window.addEventListener("click", function (event) {
    if (event.target.classList.contains("modal")) {
      event.target.style.display = "none";
    }
  });
});
