document.addEventListener("DOMContentLoaded", function () {
  var modal = document.getElementById("myModal");
  var modalText = document.getElementById("modalText");
  var span = document.getElementsByClassName("close")[0];
  var container = document.getElementsByClassName("container");

  // 각 challengeBox 클릭 시 모달 열기
  document.querySelectorAll(".challengeBox").forEach(function (box) {
    box.addEventListener("click", function () {
      modalText.innerHTML = this.innerHTML;
      modal.style.display = "block";
      container.style
    });
  });

  // 모달 닫기 버튼 클릭 시
  span.onclick = function () {
    modal.style.display = "none";
  };

  // 모달 외부 클릭 시
  window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  };

  // Escape 키 눌렀을 때
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" || event.key === "Esc" || event.keyCode === 27) {
      modal.style.display = "none";
    }
  });

  // 각 joinChallengeBtn 클릭 시 챌린지 참여 요청
  document.querySelectorAll(".joinChallengeBtn").forEach(function (button) {
    button.addEventListener("click", function () {
      var challengeId = this.getAttribute("data-challenge-id");
      console.log("Clicked challengeId:", challengeId); // 클릭된 챌린지 ID 콘솔에 출력

      var url = "/challenge/join";
      var payload = {
        challenge_id: parseInt(challengeId, 10)
      };

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
