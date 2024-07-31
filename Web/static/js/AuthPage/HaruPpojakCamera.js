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
}

window.onload = loadAndPlay;
