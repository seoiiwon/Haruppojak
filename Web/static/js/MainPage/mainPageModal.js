// static/js/MainPage/mainPage.js
function showChallengeModal(challId) {
  fetchChallenge(challId);
  openModal();
}

function fetchChallenge(challId) {
  // 예시 데이터입니당.. 나중에 실제 API 호출하면 될 것 같아요
  var challengeData = {
    chall1: {
      title: '밀리의 서재 #독서',
      participants: '100명 참여중',
      description: '밀리의 서재 챌린지 설명',
      images: [
        'https://via.placeholder.com/300x150',
        'https://via.placeholder.com/300x150',
      ],
    },
    chall2: {
      title: '1일 1커밋 #코딩',
      participants: '200명 참여중',
      description: '1일 1커밋 챌린지 설명',
      images: [
        'https://via.placeholder.com/300x150',
        'https://via.placeholder.com/300x150',
      ],
    },
    chall3: {
      title: '냠냠 #요리',
      participants: '150명 참여중',
      description: '냠냠 챌린지 설명',
      images: [
        'https://via.placeholder.com/300x150',
        'https://via.placeholder.com/300x150',
      ],
    },
    chall4: {
      title: '다른 챌린지 #기타',
      participants: '50명 참여중',
      description: '다른 챌린지 설명',
      images: [
        'https://via.placeholder.com/300x150',
        'https://via.placeholder.com/300x150',
      ],
    },
  };

  var modalText = document.getElementById('modalText');
  var data = challengeData[challId];

  modalText.innerHTML = `
    <div class="carousel">
      ${data.images
        .map((src) => `<img src="${src}" alt="Challenge Image">`)
        .join('')}
    </div>
    <h2 class="challenge-title">${data.title}</h2>
    <p class="participants-count">${data.participants}</p>
    <p class="challenge-description">${data.description}</p>
  `;

  // 자동 슬라이드 설정
  const carouselInner = document.querySelector('.carousel-inner');
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
  var modal = document.getElementById('modal');
  modal.style.display = 'block';
}

function closeModal() {
  var modal = document.getElementById('modal');
  modal.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function () {
  // 각 challengeBox 클릭 시 showChallengeModal 함수 호출
  document.querySelectorAll('.challengeBox').forEach(function (box) {
    box.addEventListener('click', function () {
      var challengeId = this.getAttribute('data-challenge-id');
      showChallengeModal(challengeId);
    });
  });

  // 모달 외부 클릭 시 모달 닫기
  window.addEventListener('click', function (event) {
    if (event.target.classList.contains('modal')) {
      event.target.style.display = 'none';
    }
  });
});
