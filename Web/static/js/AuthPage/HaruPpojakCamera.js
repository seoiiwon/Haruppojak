let stream;

async function loadAndPlay() {
  const video = document.getElementById('userCam');
  try {
    stream = await getDeviceStream({
      video: { width: { ideal: 1280 }, height: { ideal: 720 } },
      audio: false,
    });
    video.srcObject = stream;
  } catch (error) {
    console.error('Error accessing camera: ', error);
  }
}

function stop() {
  const video = document.getElementById('userCam');
  if (stream) {
    const tracks = stream.getTracks();
    tracks.forEach((track) => {
      track.stop();
    });
  }
  video.srcObject = null;
}

function getDeviceStream(option) {
  if ('mediaDevices' in navigator && 'getUserMedia' in navigator.mediaDevices) {
    return navigator.mediaDevices.getUserMedia(option);
  } else {
    return new Promise((resolve, reject) => {
      navigator.getUserMedia(option, resolve, reject);
    });
  }
}

async function capture() {
  const video = document.getElementById('userCam');
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.scale(-1, 1);
  ctx.drawImage(video, -canvas.width, 0, canvas.width, canvas.height);

  const imgData = canvas.toDataURL('image/png'); // 캡처된 이미지의 데이터 URL
  const formData = new FormData();
  formData.append('image', imgData);

  try {
    // 서버에 이미지 데이터 전송
    const response = await fetch('/upload-image', {
      // '/upload-image'는 실제 서버의 엔드포인트로 대체해야 함
      method: 'POST',
      body: formData,
    });
    if (!response.ok) {
      throw new Error('Failed to upload image');
    }

    // 서버의 응답을 처리하여 새로운 페이지로 리디렉션
    const responseData = await response.json();
    const imageUrl = responseData.imageUrl; // 서버에서 반환한 이미지 URL

    // proofImg 태그에 이미지 추가
    const proofImg = document.querySelector('.proofImg img');
    proofImg.src = imageUrl;

    // 페이지 이동
    window.location.href = '/haru/photo/detail';
  } catch (error) {
    console.error('Error capturing image:', error);
  }

  // 비디오와 canvas 정리
  const resultDiv = document.querySelector('.result');
  resultDiv.innerHTML = '';
  resultDiv.style.display = 'none';
  stop();
}
