// User Login

const userLoginForm = document.getElementById('loginUserForm');
if (userLoginForm) {
    userLoginForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const userLoginData = new FormData(event.target)
        const payload = new URLSearchParams(userLoginData);

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
                document.cookie = `user_access_token=${response_json.access_token}; path=/`;
                window.location.href = '/todos/todo.html';
            } else {
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




// User Logout

function logoutUser() {
    window.location.href = '/user/redirectToLogin.html';
}