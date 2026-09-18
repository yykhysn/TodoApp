    // // Add Todo JS
    // const todoForm = document.getElementById('todoForm');
    // if (todoForm) {
    //     todoForm.addEventListener('submit', async function (event) {
    //         event.preventDefault();
    //
    //         const form = event.target;
    //         const formData = new FormData(form);
    //         const data = Object.fromEntries(formData.entries());
    //
    //         const payload = {
    //             title: data.title,
    //             description: data.description,
    //             priority: parseInt(data.priority),
    //             complete: false
    //         };
    //
    //         try {
    //             const response = await fetch('/todos/todo', {
    //                 method: 'POST',
    //                 headers: {
    //                     'Content-Type': 'application/json',
    //                     'Authorization': `Bearer ${getCookie('access_token')}`
    //                 },
    //                 body: JSON.stringify(payload)
    //             });
    //
    //             if (response.ok) {
    //                 form.reset(); // Clear the form
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
    // }
    //
    // // Edit Todo JS
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

    // User Login
    const userLoginForm = document.getElementById('loginUserForm');
    if (userLoginForm) {
        userLoginForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const userLoginData = new FormData(event.target)
            const payload = new URLSearchParams(userLoginData);
            // for (const [key, value] of userLoginData.entries()) {
            //     payload.append(key, value);
            // }

            try {
                const response = await fetch('/api/user/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: payload.toString()
                });
                const response_json = await response.json();

                if (response.ok) {
                    // Handle success (e.g., redirect to dashboard)
                    // Delete any cookies available
                    // logout();
                    // Save token to cookie
                    document.cookie = `user_access_token=${response_json.access_token}; path=/`;
                    window.location.href = '/todos/todo.html';
                } else {
                    // Handle error
                    alert(`Error: ${response_json.detail}`);
                }
            } catch (error) {
                console.error('User Login Error:', error);
                alert(`An error occurred. Please try again: ${error.message}`);
            }
        });
    }

    // User Registration
    const userRegisterForm = document.getElementById('registerUserForm');
    if (userRegisterForm) {
        userRegisterForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const userRegisterData = Object.fromEntries(new FormData(event.target));
            if (userRegisterData.userPassword !== userRegisterData.userConfirmPassword) {
                alert("Passwords do not match");
                return;
            }

            const payload = {
                email: userRegisterData.email,
                username: userRegisterData.username,
                first_name: userRegisterData.firstname,
                last_name: userRegisterData.lastname,
                password: userRegisterData.password
            };

            try {
                const response = await fetch('/api/user/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    alert("Register Successfully! Please login");
                    window.location.href = '/user/login.html';
                } else {
                    const error = await response.json();
                    let errMsg = "";

                    // Handle Pydantic 422 Error
                    if (response.status === 422) {
                        error.detail.forEach(item => {
                            let locField = item.loc;
                            if(locField[0] === "body"){
                                locField = locField.slice(1);
                            }
                            errMsg += `${locField.join(".")}: ${item.msg}\n`;
                        })
                    }
                    // Handle Other Error
                    else {
                        errMsg = error.detail || "Register Fail";
                    }

                    alert(`Error:${errMsg}`);
                }
            }
            catch (error) {
                console.error('User Register Error:', error);
                alert(`An error occurred. Please try again: ${error.message}`);
            }
        });
    }





    // // Helper function to get a cookie by name
    // function getCookie(name) {
    //     let cookieValue = null;
    //     if (document.cookie && document.cookie !== '') {
    //         const cookies = document.cookie.split(';');
    //         for (let i = 0; i < cookies.length; i++) {
    //             const cookie = cookies[i].trim();
    //             if (cookie.substring(0, name.length + 1) === (name + '=')) {
    //                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
    //                 break;
    //             }
    //         }
    //     }
    //     return cookieValue;
    // };

    // User Logout
    function logoutUser() {
        window.location.href = '/user/redirectToLogin.html';
    }


    // Sort Todos Table
    let sortKey = "priority";
    let sortOrder = "asc";

    function sortTodosTable(key, order) {
        const todosTbody = document.getElementById("todosTableBody");
        const todosList = Array.from(todosTbody.querySelectorAll("tr"))

        todosList.sort((todoTrA, todoTrB) => {
            sortKey = key;
            sortOrder = order;

            const keyIndexMap = {
                title: 1,
                description: 2,
                priority: 3,
            };
            const keyIndex = keyIndexMap[key];

            let valA, valB, result;
            if (key === "action") {
                valA = !! todoTrA.querySelector("td.strike-through-td")
                valB = !! todoTrB.querySelector("td.strike-through-td")
                result = valA - valB
            }else if (key === "priority") {
                valA = Number(todoTrA.querySelectorAll("td")[keyIndex].textContent);
                valB = Number(todoTrB.querySelectorAll("td")[keyIndex].textContent);
                result = valA - valB;
            }else {
                valA = todoTrA.querySelectorAll("td")[keyIndex].textContent;
                valB = todoTrB.querySelectorAll("td")[keyIndex].textContent;
                result = valA.localeCompare(valB);
            }

            if (sortOrder === "desc"){
                result = -result
            }

            return result;
        })

        todosList.forEach((todo) => {
            todosTbody.append(todo);
        });

        updateSortArrow();
        renderTodosTableRowNumber()
    }

    function updateSortArrow() {
        document.querySelectorAll(".arrow-up, .arrow-down").forEach(arrow => {
            arrow.classList.remove("active");
        });

        const activeArrow = document.querySelector('th[data-sort-key="' + sortKey +'"]');
        const arrow = sortOrder === "asc" ? activeArrow.querySelector(".arrow-up") :
            activeArrow.querySelector(".arrow-down");
        arrow.classList.add("active");
    }

    document.querySelectorAll(".arrow-up, .arrow-down").forEach(arrow => {
        arrow.addEventListener("click", () => {
            const th = arrow.closest("th");
            const key = th.getAttribute("data-sort-key")
            const order = arrow.getAttribute("data-sort-order");
            sortTodosTable(key, order);
        })
    })


    // Render Todos Table Row Number
    function renderTodosTableRowNumber(){
        const todosTbody = document.getElementById("todosTableBody");

        const todosTrs = Array.from(todosTbody.querySelectorAll("tr"));
        todosTrs.forEach((tr, index) => {
            tr.querySelector("td:nth-child(1)").textContent = String(index+1);
        })
    }

    document.addEventListener('DOMContentLoaded', () => {
        if (document.body.dataset.page === "todo"){
            renderTodosTableRowNumber()
        }
    })