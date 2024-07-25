let stream;

async function loadAndPlay() {
    const video = document.getElementById('userCam');
    try {
        stream = await getDeviceStream({
            video: { width: 400, height: 600 },
            audio: false
        });
        video.srcObject = stream;
    } catch (err) {
        console.error('Error accessing media devices.', err);
    }
}

function stop() {
    const video = document.getElementById('userCam');
    if (stream) {
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
        video.srcObject = null;
        stream = null; 
    }
}

function getDeviceStream(option) {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        return navigator.mediaDevices.getUserMedia(option);
    } else {
        return new Promise(function(resolve, reject) {
            navigator.getUserMedia(option, resolve, reject);
        });
    }
}