document.addEventListener("DOMContentLoaded", function () {
  var modal = document.getElementById("myModal");
  var modalText = document.getElementById("modalText");
  var span = document.getElementsByClassName("close")[0];

  document.querySelectorAll(".challengeBox").forEach(function (box) {
    box.addEventListener("click", function () {
      modalText.innerHTML = this.innerHTML;
      modal.style.display = "block";
    });
  });

  span.onclick = function () {
    modal.style.display = "none";
  };

  window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  };

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" || event.key === "Esc" || event.keyCode === 27) {
      modal.style.display = "none";
    }
  });
});
