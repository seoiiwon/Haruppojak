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

// 뽀짝챌 스크롤 도트
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
