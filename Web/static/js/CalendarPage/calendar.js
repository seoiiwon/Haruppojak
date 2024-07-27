// 연도 및 월 표시
document.addEventListener("DOMContentLoaded", function () {
  const daysContainer = document.querySelector(".calendarDays");
  const yearElement = document.querySelector(".year");
  const monthElement = document.querySelector(".month");
  const prevMonthButton = document.querySelector(".prevMonth");
  const nextMonthButton = document.querySelector(".nextMonth");

  let currentMonth = new Date().getMonth();
  let currentYear = new Date().getFullYear();

  const monthNames = [
    "1월",
    "2월",
    "3월",
    "4월",
    "5월",
    "6월",
    "7월",
    "8월",
    "9월",
    "10월",
    "11월",
    "12월",
  ];

  function generateCalendar(year, month) {
    daysContainer.innerHTML = "";
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    yearElement.textContent = `${year}년`;
    monthElement.textContent = monthNames[month];

    for (let i = 0; i < firstDay; i++) {
      const emptySpot = document.createElement("div");
      emptySpot.classList.add("day");
      daysContainer.appendChild(emptySpot);
    }

    for (let i = 1; i <= daysInMonth; i++) {
      const day = document.createElement("div");
      day.classList.add("day");
      day.textContent = i;

      if (
        i === new Date().getDate() &&
        month === new Date().getMonth() &&
        year === new Date().getFullYear()
      ) {
        day.classList.add("today");
      }
      daysContainer.appendChild(day);
    }
  }

  function prevMonth() {
    if (currentMonth === 0) {
      currentMonth = 11;
      currentYear--;
    } else {
      currentMonth--;
    }
    generateCalendar(currentYear, currentMonth);
  }

  function nextMonth() {
    if (currentMonth === 11) {
      currentMonth = 0;
      currentYear++;
    } else {
      currentMonth++;
    }
    generateCalendar(currentYear, currentMonth);
  }

  prevMonthButton.addEventListener("click", prevMonth);
  nextMonthButton.addEventListener("click", nextMonth);

  generateCalendar(currentYear, currentMonth);
});

// 날짜 표시
document.addEventListener("DOMContentLoaded", function () {
  const daysContainer = document.querySelector(".calendarDays");
  const currentMonth = new Date().getMonth();
  const currentYear = new Date().getFullYear();

  function generateCalendar(month, year) {
    daysContainer.innerHTML = "";
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    for (let i = 0; i < firstDay; i++) {
      const emptySpot = document.createElement("div");
      emptySpot.classList.add("day");
      daysContainer.appendChild(emptySpot);
    }

    for (let i = 1; i <= daysInMonth; i++) {
      const day = document.createElement("div");
      day.classList.add("day");
      day.textContent = i;

      if (
        i === new Date().getDate() &&
        month === currentMonth &&
        year === currentYear
      ) {
        day.classList.add("today");
      }
      daysContainer.appendChild(day);
    }
  }

  generateCalendar(currentMonth, currentYear);
});
