// 각 challengeBox 클릭 시 모달 열기
document.querySelectorAll(".challengeBox").forEach(function (box) {
  box.addEventListener("click", function () {
    var challengeId = this.getAttribute("data-challenge-id");
    var modal = document.getElementById("myModal-" + challengeId);
    var modalText = document.getElementById("modalText-" + challengeId);

    // modalText 요소가 존재하는지 확인
    if (modalText) {
      // 챌린지 정보 가져오기
      var challengeTitle = document.querySelector(
        `[data-challenge-id="${challengeId}"] ~ .challengeTitle`
      ).innerText;
      var challengeChallenger = this.getAttribute("data-challenge-challenger");
      var challengeOwner = this.getAttribute("data-challenge-owner");
      var challengeReward = this.getAttribute("data-challenge-reward");
      var challengeComment = this.getAttribute("data-challenge-comment");

      // 모달 내용 채우기
      modalText.innerHTML = `
        <h2>${challengeTitle}</h2>
        <p>${challengeChallenger}명 참여 중</p>
        <p>${challengeOwner}</p>
        <p>리워드: ${challengeReward}</p>
        <p>${challengeComment}</p>
      `;
      modal.style.display = "block";
    } else {
      console.error(
        "Modal text element not found for challenge ID: " + challengeId
      );
    }
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
