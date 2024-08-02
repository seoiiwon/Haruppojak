let stream;

async function loadAndPlay() {
  const video = document.getElementById('userCam');
  try {
    stream = await getDeviceStream({
      video: { width: 400, height: 600 },
      audio: false
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
  
  const imgData = canvas.toDataURL('image/png');

  // 서버에 이미지 데이터 전송
  try {
    const response = await fetch('/upload-image', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ image: imgData })
    });

    if (!response.ok) {
      throw new Error('이미지 업로드에 실패했습니다.');
    }

    const result = await response.json();
    console.log('이미지 업로드 성공:', result);

    // 이미지 표시
    const img = document.createElement('img');
    img.src = imgData;
    const resultDiv = document.querySelector('.result');
    resultDiv.innerHTML = '';
    resultDiv.appendChild(img);
    
    // 비디오 공간 숨기기
    const videoSpace = document.querySelector('.videoSpace');
    videoSpace.style.display = 'none';
    
    // 결과 div 보이기
    resultDiv.style.display = 'block';
    
    // 카메라 종료
    stop();
  } catch (error) {
    console.error('이미지 업로드 중 오류 발생:', error);
  }
}


function capture() {
  const video = document.getElementById('userCam');
  const canvas = document.createElement('canvas');
  canvas.width = 400;
  canvas.height = 600;
  const ctx = canvas.getContext('2d');
  ctx.scale(-1, 1);
  ctx.drawImage(video, -canvas.width, 0, canvas.width, canvas.height);
  
  const img = document.createElement('img');
  img.src = canvas.toDataURL('image/png');
  const resultDiv = document.querySelector('.result');
  resultDiv.innerHTML = '';
  resultDiv.appendChild(img);
  
  // videoSpace 숨기기
  const videoSpace = document.querySelector('.videoSpace');
  videoSpace.style.display = 'none';
  
  // resultDiv 보이기
  resultDiv.style.display = 'block';

  // 캠 종료
  stop();
}

window.onload = loadAndPlay;
