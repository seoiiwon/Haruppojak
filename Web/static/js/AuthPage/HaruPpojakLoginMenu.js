function goToSignInPage() {
    window.location.href = 'HaruPpojakSignIn.html';
}

window.onload = function() {
    setTimeout(() => {
        document.querySelector('.HPIntroBox').classList.add('move-up');
        setTimeout(() => {
            document.querySelector('.LoginBars').classList.add('show-login-bars');
        }, 1000);
    }, 3000);
};