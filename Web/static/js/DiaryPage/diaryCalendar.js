document.addEventListener("DOMContentLoaded", function () {
  const calendarBody = document.querySelector(".calendar-body");

  function createCalendar(year, month) {
    const firstDay = new Date(year, month, 1).getDay();
    const lastDate = new Date(year, month + 1, 0).getDate();
    const prevLastDate = new Date(year, month, 0).getDate();

    let dates = [];
    // Add previous month's dates
    for (let i = firstDay; i > 0; i--) {
      dates.push(`<div class="date other-month">${prevLastDate - i + 1}</div>`);
    }
    // Add current month's dates
    for (let i = 1; i <= lastDate; i++) {
      const today = new Date();
      const isToday =
        today.getFullYear() === year &&
        today.getMonth() === month &&
        today.getDate() === i;
      const className = isToday
        ? "date current-month today"
        : "date current-month";
      dates.push(`<div class="${className}">${i}</div>`);
    }
    // Add next month's dates to fill the calendar
    const nextDays = 42 - dates.length;
    for (let i = 1; i <= nextDays; i++) {
      dates.push(`<div class="date other-month">${i}</div>`);
    }

    calendarBody.innerHTML = dates.join("");
  }

  createCalendar(new Date().getFullYear(), new Date().getMonth());
});
