document.addEventListener("DOMContentLoaded", function () {
  var header = document.querySelector("header");

  // 각 challengeBox 클릭 시 모달 열기
  document.querySelectorAll(".challengeBox").forEach(function (box) {
    box.addEventListener("click", function () {
      var challengeId = this.getAttribute("data-challenge-id");
      var modal = document.getElementById("myModal-" + challengeId);
      var modalText = document.getElementById("modalText-" + challengeId);

      modalText.innerHTML = this.innerHTML;
      modal.style.display = "block";
    });
  });

  // 각 모달의 닫기 버튼 클릭 시
  document.querySelectorAll(".close").forEach(function (span) {
    span.addEventListener("click", function () {
      var modalId = this.getAttribute("data-modal-id");
      var modal = document.getElementById(modalId);
      modal.style.display = "none";
    });
  });

  // 모달 외부 클릭 시
  window.addEventListener("click", function (event) {
    if (event.target.classList.contains("modal")) {
      event.target.style.display = "none";
    }
  });

  // Escape 키 눌렀을 때 모든 모달 닫기
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" || event.key === "Esc" || event.keyCode === 27) {
      document.querySelectorAll(".modal").forEach(function (modal) {
        modal.style.display = "none";
      });
    }
  });

  // 각 joinChallengeBtn 클릭 시 챌린지 참여 요청
  document.querySelectorAll(".joinChallengeBtn").forEach(function (button) {
    button.addEventListener("click", function () {
      var challengeId = this.getAttribute("data-challenge-id");
      var url = "/challenge/join";

      var payload = {
        challenge_id: parseInt(challengeId, 10)
      };

      console.log(challengeId);

      fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(payload)
      })
      .then(response => {
        if (response.ok) {
          console.log('Challenge joined successfully!');
        } else {
          return response.json().then(errorData => {
            throw new Error(errorData.detail || '챌린지 참여 중 오류 발생');
          });
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
    });
  });
});
