function goToSignInPage() {
    window.location.href = '/auth/signin';
}

window.onload = function() {
    setTimeout(() => {
        document.querySelector('.HPIntroBox').classList.add('move-up');
        setTimeout(() => {
            document.querySelector('.LoginBars').classList.add('show-login-bars');
        }, 1000);
    }, 3000);
};

const logo = document.querySelector('.ppojakLogo');
const container = document.querySelector('.container');

container.addEventListener('mousemove', (e) => {
    const { clientX: x, clientY: y } = e;
    const { innerWidth: width, innerHeight: height } = window;
    
    const moveX = (x - width / 2) / (width / 2) * 20; 
    const moveY = (y - height / 2) / (height / 2) * 20; 

    logo.style.transform = `rotateX(${moveY}deg) rotateY(${moveX}deg)`;
});

container.addEventListener('mouseleave', () => {
    logo.style.transform = 'rotateX(0) rotateY(0)';
});
