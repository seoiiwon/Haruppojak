async function joinChallenge(challengeId) {
  try {
    const response = await fetch('/challenge/join', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + getCookie('access_token'),
      },
      body: JSON.stringify({ challenge_id: challengeId }),
    });

    if (!response.ok) {
      const error = await response.json();
      alert(`Error: ${error.detail}`);
    } else {
      alert('참여 신청이 완료');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('챌린지 참여 중 오류가 발생했습니다.');
  }
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.joinChallengeBtn').forEach((button) => {
    button.addEventListener('click', () => {
      const challengeId = button.getAttribute('challengeID');
      console.log(challengeId);
      joinChallenge(challengeId);
    });
  });
});
