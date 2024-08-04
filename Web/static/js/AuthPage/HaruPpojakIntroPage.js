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
                    tododate: new Date().toISOString(),  // 현재 시간을 기본값으로 설정
                    todocheck: false  // 기본값 false
                });
            }
        });

        let payload = {
            todos: todoList
        };

        let url = '/haru/intro';

        console.log(payload);

        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        })
        .then(response => {
            if (response.ok) {
                console.log("Data sent successfully!");
            } else {
                return response.json().then(errorData => {
                    throw new Error(errorData.detail || 'Error occurred while sending data');
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
