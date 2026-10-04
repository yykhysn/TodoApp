function getUserAccessToken() {
    const cookies = "; " + document.cookie;
    const cookies_part = cookies.split('; user_access_token=');
    if (cookies_part.length === 2){
        return cookies_part.pop().split(';').shift();
    }
    window.location.href = '/user/redirectToLogin.html'
}



function encodePlainHtml(str){
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}




    // const editTodoForm = document.getElementById('editTodoForm');
    // if (editTodoForm) {
    //     editTodoForm.addEventListener('submit', async function (event) {
    //     event.preventDefault();
    //     const form = event.target;
    //     const formData = new FormData(form);
    //     const data = Object.fromEntries(formData.entries());
    //     var url = window.location.pathname;
    //     const todoId = url.substring(url.lastIndexOf('/') + 1);
    //
    //     const payload = {
    //         title: data.title,
    //         description: data.description,
    //         priority: parseInt(data.priority),
    //         complete: data.complete === "on"
    //     };
    //
    //     try {
    //         const token = getCookie('access_token');
    //         console.log(token)
    //         if (!token) {
    //             throw new Error('Authentication token not found');
    //         }
    //
    //         console.log(`${todoId}`)
    //
    //         const response = await fetch(`/todos/todo/${todoId}`, {
    //             method: 'PUT',
    //             headers: {
    //                 'Content-Type': 'application/json',
    //                 'Authorization': `Bearer ${token}`
    //             },
    //             body: JSON.stringify(payload)
    //         });
    //
    //         if (response.ok) {
    //             window.location.href = '/todos/todo-page'; // Redirect to the todo page
    //         } else {
    //             // Handle error
    //             const errorData = await response.json();
    //             alert(`Error: ${errorData.detail}`);
    //         }
    //     } catch (error) {
    //         console.error('Error:', error);
    //         alert('An error occurred. Please try again.');
    //     }
    // });
    //
    //     document.getElementById('deleteButton').addEventListener('click', async function () {
    //         var url = window.location.pathname;
    //         const todoId = url.substring(url.lastIndexOf('/') + 1);
    //
    //         try {
    //             const token = getCookie('access_token');
    //             if (!token) {
    //                 throw new Error('Authentication token not found');
    //             }
    //
    //             const response = await fetch(`/todos/todo/${todoId}`, {
    //                 method: 'DELETE',
    //                 headers: {
    //                     'Authorization': `Bearer ${token}`
    //                 }
    //             });
    //
    //             if (response.ok) {
    //                 // Handle success
    //                 window.location.href = '/todos/todo-page'; // Redirect to the todo page
    //             } else {
    //                 // Handle error
    //                 const errorData = await response.json();
    //                 alert(`Error: ${errorData.detail}`);
    //             }
    //         } catch (error) {
    //             console.error('Error:', error);
    //             alert('An error occurred. Please try again.');
    //         }
    //     });
    //
    //
    // }
    //




