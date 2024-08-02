document.addEventListener('DOMContentLoaded', function() {
    const firstForm = document.querySelector('.FirstForm');
    const secondForm = document.querySelector('.SecondForm');
    const nextButton = document.querySelector('.NextBtn');
    const signUpForm = document.getElementById('SignUpForm');

    nextButton.addEventListener('click', function() {
        if (isFirstFormValid()) {
            // 첫 번째 폼의 opacity를 0으로 설정하여 서서히 사라지도록 합니다.
            firstForm.style.opacity = '0';
            // 1초 후 첫 번째 폼을 display: none으로 변경하여 공간을 차지하지 않도록 합니다.
            setTimeout(() => {
                firstForm.style.display = 'none';
                // 두 번째 폼을 display: flex로 설정하여 보이도록 합니다.
                secondForm.style.display = 'flex';
                secondForm.style.opacity = '0';
                // 초기 opacity를 0으로 설정한 후 0.1초 후에 서서히 나타나도록 설정합니다.
                setTimeout(() => {
                    secondForm.style.opacity = '1';
                }, 100);
            }, 1000);
        }
    });

    signUpForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        if (!isSecondFormValid()) {
            alert('모든 필드를 입력해주세요.');
            return;
        }
    
        let userData = {
            userID: document.getElementById('ID').value.trim(),
            userPassword: document.getElementById('PW').value.trim(),
            userName: document.getElementById('Name').value.trim(),
            userEmail: document.getElementById('Email').value.trim(),
            userBirth: parseInt(document.getElementById('Birth').value.trim(), 10),
            userGender: parseInt(document.querySelector('input[name="Gender"]:checked').value, 10),
            userProfileName: document.getElementById('Name').value.trim(),
        };
    
        let url = '/auth/signup';
    
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(userData)
            });
    
            if (response.status === 204) {
                alert('회원가입이 완료되었습니다.');
                goToSignInPage();
            } else {
                const result = await response.json();
                alert(result.detail || '회원가입에 실패했습니다.');
            }
        } 
        catch (error) {
            console.error('Error:', error);
            alert('회원가입 중 오류가 발생했습니다.');
        }
    });
    

    function isFirstFormValid() {
        const id = document.getElementById('ID').value.trim();
        const pw = document.getElementById('PW').value.trim();
        const pwCheck = document.getElementById('PWCheck').value.trim();

        if (!id || !pw || !pwCheck) {
            alert('모든 정보를 입력해주세요.');
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
