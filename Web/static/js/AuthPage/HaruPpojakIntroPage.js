document.addEventListener("DOMContentLoaded", function () {
    const addCompleteButton = document.querySelector(".AddComplete");

    addCompleteButton.addEventListener("click", function (event) {
        event.preventDefault();

        const todoInputs = document.querySelectorAll(".TodoBox input[type='text']");
        const todoList = [];

        todoInputs.forEach(input => {
            if (input.value.trim() !== "") {
                todoList.push({
                    todowrite: input.value.trim(),
                });
            }
        });

        let url = '/haru/intro';  // 엔드포인트 확인

        fetch(url, {
            method: "POST",  // HTTP 메소드 확인
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ todos: todoList })
        })
        .then(response => {
            if (response.ok) {
                console.log("Data sent successfully!");
            } else {
                return response.json().then(errorData => {
                    throw new Error(JSON.stringify(errorData));
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });

    });
    addCompleteButton.addEventListener("click", function (event) {
        event.preventDefault();
        window.location.href = '/haru/main';
    });
});
