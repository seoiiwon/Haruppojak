document.addEventListener("DOMContentLoaded", function () {
  const calendarBody = document.querySelector(".calendar-body");
  const diaryModal = document.querySelector("#diaryModal");
  const modalDate = document.querySelector("#modalDate");
  const modalContent = document.querySelector("#modalContent");
  const closeModalButton = document.querySelector(".close");

  // Mock diaries data
  const diaries = JSON.parse("{{ diaries|tojson|safe }}");

  // Function to create calendar
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
      dates.push(
        `<div class="${className}" data-date="${year}-${(month + 1)
          .toString()
          .padStart(2, "0")}-${i.toString().padStart(2, "0")}">${i}</div>`
      );
    }
    // Add next month's dates to fill the calendar
    const nextDays = 42 - dates.length;
    for (let i = 1; i <= nextDays; i++) {
      dates.push(`<div class="date other-month">${i}</div>`);
    }

    calendarBody.innerHTML = dates.join("");
  }

  // Open modal with diary content
  function openModal(date) {
    const diary = diaries.find((d) => d.Date === date);
    if (diary) {
      modalDate.textContent = `Date: ${diary.Date}`;
      modalContent.textContent = diary.Content;
    } else {
      modalDate.textContent = "No Diary Entry";
      modalContent.textContent = "No diary entry for this date.";
    }
    diaryModal.style.display = "flex";
  }

  // Close the modal
  function closeModal() {
    diaryModal.style.display = "none";
  }

  // Event listener for calendar date click
  calendarBody.addEventListener("click", function (e) {
    if (e.target.classList.contains("date") && e.target.dataset.date) {
      openModal(e.target.dataset.date);
    }
  });

  // Event listener for closing the modal
  closeModalButton.addEventListener("click", closeModal);

  // Initial calendar render
  createCalendar(new Date().getFullYear(), new Date().getMonth());
});

// Function to navigate back to the previous page
function goBack() {
  window.history.back();
}

// Function to close the app by navigating to closeApp.html
function closeApp() {
  window.location.href = "close";
}
