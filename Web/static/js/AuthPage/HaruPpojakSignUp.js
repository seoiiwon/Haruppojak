document.addEventListener('DOMContentLoaded', function() {
    const firstForm = document.querySelector('.FirstForm');
    const secondForm = document.querySelector('.SecondForm');
    const nextButton = document.querySelector('.NextBtn');
    const submitButton = document.querySelector('.SignUpComplete');
    const signUpForm = document.getElementById('SignUpForm');

    nextButton.addEventListener('click', function() {
        if (isFirstFormValid()) {
            firstForm.style.opacity = '0';
            setTimeout(() => {
                firstForm.classList.add('hidden');
                secondForm.classList.remove('hidden');
                secondForm.style.opacity = '1';
            }, 1000);
        }
    });

    signUpForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        if (!isSecondFormValid()) {
            alert('모든 필드를 입력해주세요.');
            return;
        }

        const userData = {
            userID: document.getElementById('ID').value.trim(),
            userPassword: document.getElementById('PW').value.trim(),
            userName: document.getElementById('Name').value.trim(),
            userEmail: document.getElementById('Email').value.trim(),
            userBirth: parseInt(document.getElementById('Birth').value.trim()),
            userGender: document.querySelector('input[name="Gender"]:checked').value,
            userProfileName: document.getElementById('Name').value.trim(),
            userProfileComment: ""
        };

        try {
            const response = await fetch('/auth/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });

            if (response.status === 204) {
                alert('회원가입이 완료되었습니다.');
                goToSignInPage();
            } else {
                const result = await response.json();
                alert(result.detail || '회원가입에 실패했습니다.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('회원가입 중 오류가 발생했습니다.');
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
        const name = document.getElementById('Name').value.trim();
        const email = document.getElementById('Email').value.trim();
        const birth = document.getElementById('Birth').value.trim();
        const gender = document.querySelector('input[name="Gender"]:checked');

        if (!name || !email || !birth || !gender) {
            return false;
        }

        return true;
    }

    function goToSignInPage() {
        window.location.href = '/';
    }
});
