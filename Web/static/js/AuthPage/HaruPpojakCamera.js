let stream;

async function loadAndPlay() {
  const video = document.getElementById('userCam');
  try {
    stream = await getDeviceStream({
      video: { width: 400, height: 600 },
      audio: false
    });
    video.srcObject = stream;
    video.play(); // video.play() 호출로 비디오 재생 시작
  } catch (error) {
    console.error('Error accessing camera: ', error);
  }
}

function stop() {
  const video = document.getElementById('userCam');
  if (stream) {
    const tracks = stream.getTracks();
    tracks.forEach(track => {
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
  canvas.width = 400;
  canvas.height = 600;
  const ctx = canvas.getContext('2d');
  ctx.scale(-1, 1);
  ctx.drawImage(video, -canvas.width, 0, canvas.width, canvas.height);
  
  const imgBlob = await new Promise((resolve) => canvas.toBlob(resolve, 'image/png')); // 캡처된 이미지 Blob

  const formData = new FormData();
  formData.append('image', imgBlob, 'user_image.png'); // 파일 이름은 예시

  try {
    const response = await fetch('/haru/upload/imgFile', { // 서버의 엔드포인트
      method: 'POST',
      body: formData
    });
    if (!response.ok) {
      throw new Error('Failed to upload image');
    }

    const responseData = await response.json();
    const imageUrl = responseData.imageUrl; // 서버에서 반환한 이미지 URL

    // 페이지 이동
    window.location.href = '/haru/upload/imgFile';
  } catch (error) {
    console.error('Error capturing image:', error);
  }

  stop();
}

window.onload = loadAndPlay;
