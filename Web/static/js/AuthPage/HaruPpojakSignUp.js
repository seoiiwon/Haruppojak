document.addEventListener('DOMContentLoaded', function() {
    const firstForm = document.querySelector('.FirstForm');
    const secondForm = document.querySelector('.SecondForm');
    const nextButton = document.querySelector('.NextBtn');
    const submitButton = document.querySelector('.SignUpComplete');

    nextButton.addEventListener('click', function() {
        if (isFirstFormValid()) {
            firstForm.style.opacity = '0';
            setTimeout(() => {
                firstForm.classList.add('hidden');
                secondForm.style.left = '50%';
                setTimeout(() => {
                    secondForm.style.opacity = '1';
                }, 1000); 
            }, 1000);
        }
    });

    submitButton.addEventListener('click', function(event) {
        if (!isSecondFormValid()) {
            event.preventDefault();
            alert('모든 필드를 입력해주세요.');
        }
    });

    function isFirstFormValid() {
        const id = document.getElementById('ID').value.trim();
        const pw = document.getElementById('PW').value.trim();
        const pwCheck = document.getElementById('PWCheck').value.trim();

        if (!id || !pw || !pwCheck) {
            alert('모든 필드를 입력해주세요.');
            return false;
        }

        if (pw !== pwCheck) {
            alert('패스워드를 다시 확인해주세요.');
            return false;
        }

        return true;
    }

    function isSecondFormValid() {
        const inputs = secondForm.querySelectorAll('input[type="text"], input[type="email"]');
        for (let input of inputs) {
            if (!input.value.trim()) {
                return false;
            }
        }
        return true;
    }
});


function goToSignInPage() {
    window.location.href = '/';
}