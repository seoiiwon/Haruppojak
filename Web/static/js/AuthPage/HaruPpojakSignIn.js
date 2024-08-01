document.addEventListener('DOMContentLoaded', function() {
    const signInForm = document.getElementById('SignInForm');
    const signUpBtn = document.getElementById('SignUpBtn');

    signInForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        let userID = document.getElementById('UserID').value.trim();
        let userPW = document.getElementById('UserPW').value.trim();

        if (!userID || !userPW) {
            alert('아이디와 비밀번호를 입력해주세요.');
            return;
        }

        const loginData = new URLSearchParams();
        loginData.append('username', userID);
        loginData.append('password', userPW);

        try {
            const response = await fetch('/auth/signin', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: loginData.toString()
            });

            if (response.ok) {
                alert('로그인 성공!');
                window.location.href = '/haru/photo';
            } else {
                const result = await response.json();
                alert(result.detail || '로그인에 실패했습니다.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('로그인 중 오류가 발생했습니다.');
        }
    });

    function goToSignUpPage() {
        window.location.href = '/auth/signup';
    }

    signUpBtn.addEventListener('click', goToSignUpPage);
});
