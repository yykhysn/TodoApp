const todoPriorityMap = {
    1: "High",
    2: "Medium High",
    3: "Medium",
    4: "Medium Low",
    5: "Low"
};



// Add Todo

const addTodoForm = document.getElementById('addTodoForm');
if (addTodoForm) {
    addTodoForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        const payload = {
            title: data.title,
            description: data.description,
            priority: Number(data.priority),
            is_completed: data.is_completed === "true",
        };

        try {
            const response = await fetch('/api/todos/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getUserAccessToken()}`
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                const response_json = await response.json();
                alert(response_json.detail);
                form.reset(); // Clear the form
            } else {
                // Handle error
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        } catch (error) {
            console.error('Add Todo Error:', error);
            alert(`An error occurred. Please try again: ${error.message}`);
        }
    });
}



// Edit Todo JS

const todoTableBody = document.getElementById('todosTableBody');
let editingRow = null;
let editingRowOriginalValue = {};

todoTableBody.addEventListener('click', function (event) {
    const todoRow = event.target.closest('tr');
    if (event.target.classList.contains('btn-edit-todo')) {
        enterTodoEdit(todoRow);
    }else if (event.target.classList.contains('btn-edit-save-todo')) {
        saveEditedTodo(todoRow)
    }else if (event.target.classList.contains('btn-edit-reset-todo')) {
        resetEditingTodo(todoRow)
    }else if (event.target.classList.contains('btn-edit-cancel-todo')){
        exitTodoEdit(todoRow, 'Cancel');
    }else if (event.target.classList.contains('btn-edit-delete-todo')){
        deleteTodo(todoRow, "Delete");
    }else if (event.target.classList.contains('btn-complete-todo')){
        setTodoCompletion(todoRow, true);
    }else if (event.target.classList.contains('btn-reopen-todo')){
        setTodoCompletion(todoRow, false);
    }
})


function enterTodoEdit(rowToEdit) {
    if (editingRow && editingRow !== rowToEdit) {
        const isDiscardEdit = window.confirm('The current row has unsaved changes. Do you want to discard it and edit a new one?')
        if (isDiscardEdit) {
            exitTodoEdit(editingRow, 'Cancel');
        }else {
            return;
        }
    }

    editingRow = rowToEdit;
    editingRow.classList.add('editing-todo-tr');
    const todoTds = Array.from(editingRow.querySelectorAll('td'));
    const isTodoCompleted = editingRow.classList.contains('alert-success');
    editingRowOriginalValue = {
        title: todoTds[1].textContent,
        description: todoTds[2].textContent,
        priority: Number(todoTds[3].dataset.todoPriority),
        is_completed: isTodoCompleted
    }

    todoTds[1].innerHTML = `<textarea class="edit-textarea" rows="2">${encodePlainHtml(editingRowOriginalValue.title)}</textarea>`;
    todoTds[2].innerHTML = `<textarea class="edit-textarea" rows="5">${encodePlainHtml(editingRowOriginalValue.description)}</textarea>`;

    let prioritySelectorOption = '';
    for (let i = 1; i <= 5; i++) {
        const isSelected = i === editingRowOriginalValue.priority? 'selected' : '';
        prioritySelectorOption += `<option value="${i}" ${isSelected}>${todoPriorityMap[i]}</option>`;
    }
    todoTds[3].innerHTML = `<select class="editing-todo-td">${prioritySelectorOption}</select>`;

    todoTds[4].innerHTML = `
        <div>
            <strong>
                <label>Is Completed:</label>
                <input type="radio" name="is_completed" value="false" ${!isTodoCompleted ? 'checked' : ''}>
                <label>No</label>
                <input type="radio" name="is_completed" value="true" ${isTodoCompleted ? 'checked' : ''}>
                <label>Yes</label>
            </strong>
        </div>
        <div>
            <button type="button" class="btn btn-warning btn-edit-reset-todo mr-1">Reset</button>
            <button type="button" class="btn btn-secondary btn-edit-cancel-todo">Cancel</button>
            <button type="button" class="btn btn-primary btn-edit-save-todo mr-1">Save</button>
            <button type="button" class="btn btn-danger btn-edit-delete-todo mr-1">Delete</button>
        </div>
        `
}


function exitTodoEdit(todoEditRow, exitMode, todoNewValue) {
    let todoValue;
    switch (exitMode) {
        case 'Save':
            todoValue = todoNewValue;
            break;
        case 'Cancel':
            todoValue = editingRowOriginalValue;
            break;
        case 'Delete':
            todoEditRow.remove();
            return;
    }

    todoEditRow.classList.remove('editing-todo-tr');
    const todoTds = Array.from(todoEditRow.querySelectorAll('td'));
    todoTds[1].textContent = todoValue.title;
    todoTds[2].textContent = todoValue.description;
    todoTds[3].dataset.todoPriority = todoValue.priority;
    todoTds[3].textContent = todoPriorityMap[todoValue.priority];

    if (todoValue.is_completed) {
        todoEditRow.classList.add('alert', 'alert-success');
        todoTds.forEach((todoTd, index) => {
            if (index !== todoTds.length -1) {
                todoTd.classList.add('strike-through-td')
            }
        });
    }else {
        todoEditRow.classList.remove('alert', 'alert-success');
        todoTds.forEach((todoTd) => todoTd.classList.remove('strike-through-td'));
    }

    if (todoValue.is_completed) {
        todoTds[4].innerHTML = `
        <button type="button" class="btn btn-info btn-edit-todo">Edit</button>
        <button type="button" class="btn btn-info btn-reopen-todo">Reopen</button>
    `;
    }else {
        todoTds[4].innerHTML = `
        <button type="button" class="btn btn-info btn-edit-todo">Edit</button>
        <button type="button" class="btn btn-info btn-complete-todo">Complete</button>
    `;
    }

    editingRow = null;
    editingRowOriginalValue = {};
}


function resetEditingTodo(editingTodoRow) {
    const todoTds = Array.from(editingTodoRow.querySelectorAll('td'));
    todoTds[1].querySelector('textarea').value = editingRowOriginalValue.title;
    todoTds[2].querySelector('textarea').value = editingRowOriginalValue.description;
    todoTds[3].querySelector('select').value = editingRowOriginalValue.priority;

    const isCompletedSelector = todoTds[4].querySelectorAll('input');
    isCompletedSelector.forEach(item => {
        item.checked = item.value === String(editingRowOriginalValue.is_completed);
    } );
}


async function saveEditedTodo(editedRow){
    const todoTds = Array.from(editedRow.querySelectorAll('td'));
    const payload = {
            title: todoTds[1].querySelector('textarea').value,
            description: todoTds[2].querySelector('textarea').value,
            priority: Number(todoTds[3].querySelector('select').value),
            is_completed: todoTds[4].querySelector('input[name="is_completed"]:checked').value === 'true',
    };

    const todoUpdateParams = new URLSearchParams();
    todoUpdateParams.set('todo_public_uuid', editedRow.dataset.todoPublicUuid);
    try {
            const response = await fetch(`/api/todos/update?${todoUpdateParams}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getUserAccessToken()}`
                },
                body: JSON.stringify(payload)
            });
            const responseJson = await response.json();

            if (response.ok) {
                alert(responseJson.message);
                exitTodoEdit(editedRow, "Save",  responseJson.data.after);
            } else {
                // Handle error
                alert(`Error: ${responseJson.detail}`)
            }
    } catch (error) {
            console.error('Add Todo Error:', error);
            alert(`An error occurred. Please try again: ${error.message}`);
    }
}


async function deleteTodo(editedRow) {
    const confirmDeleteTodo = window.confirm('Are you sure that you want to delete this todo item? Once deleted, it can not be recovered');
    if (!confirmDeleteTodo) {
        return;
    }

    const todoUpdateParams = new URLSearchParams();
    todoUpdateParams.set('todo_public_uuid', editedRow.dataset.todoPublicUuid);

    try {
            const response = await fetch(`/api/todos/deleteTodo?${todoUpdateParams}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getUserAccessToken()}`
                },
            });
            const responseJson = await response.json();

            if (response.ok) {
                alert(responseJson.message);
                exitTodoEdit(editedRow, "Delete");
                renderTodosTableRowNumber()
            } else {
                // Handle error
                alert(`Error: ${responseJson.detail}`)
            }
    } catch (error) {
            console.error('Add Todo Error:', error);
            alert(`An error occurred. Please try again: ${error.message}`);
    }
}


async function setTodoCompletion(rowToSetCompletion, completionToSet) {
    const todoUpdateParams = new URLSearchParams();
    todoUpdateParams.set('todo_public_uuid', rowToSetCompletion.dataset.todoPublicUuid);

    try {
        const response = await fetch(`/api/todos/update?${todoUpdateParams}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getUserAccessToken()}`
            },
            body: JSON.stringify({is_completed: completionToSet})
        });
        const responseJson = await response.json();

        if (response.ok) {
            alert(responseJson.message);
            exitTodoEdit(rowToSetCompletion, "Save",  responseJson.data.after);
        } else {
            // Handle error
            alert(`Error: ${responseJson.detail}`)
        }
    } catch (error) {
        console.error('Add Todo Error:', error);
        alert(`An error occurred. Please try again: ${error.message}`);
    }
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
            valA = todoTrA.querySelectorAll("td")[keyIndex].dataset.todoPriority;
            valB = todoTrB.querySelectorAll("td")[keyIndex].dataset.todoPriority;
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