// --- AUTH FUNCTIONS (index.html) ---

async function register() {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const role = document.getElementById('role').value;

    if(!username || !email || !password) {
        alert("Saari details bharo bhai!");
        return;
    }

    const res = await fetch('/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password, role })
    });

    const result = await res.json();
    alert(result.msg);
}

async function login() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const res = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });

    if (res.status === 200) {
        const result = await res.json();
        localStorage.setItem('token', result.access_token);
        localStorage.setItem('role', result.role);
        window.location.href = '/templates/dashboard.html';
    } else {
        const result = await res.json();
        alert(result.msg || "Login failed!");
    }
}

function logout() {
    localStorage.clear();
    window.location.href = '/';
}

// --- TASK CRUD FUNCTIONS (dashboard.html) ---

async function addTask() {
    const token = localStorage.getItem('token');
    const title = document.getElementById('taskTitle').value;
    const description = document.getElementById('taskDesc').value;

    if(!title) {
        alert("Task ka title toh dalo!");
        return;
    }

    const res = await fetch('/api/tasks', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` 
        },
        body: JSON.stringify({ title, description })
    });

    if (res.status === 201) {
        document.getElementById('taskTitle').value = '';
        document.getElementById('taskDesc').value = '';
        loadTasks();
    }
}

async function loadTasks() {
    const token = localStorage.getItem('token');
    if (!token) return;

    const res = await fetch('/api/tasks', {
        headers: { 'Authorization': `Bearer ${token}` }
    });

    const tasks = await res.json();
    const taskList = document.getElementById('taskList');
    taskList.innerHTML = '';

    tasks.forEach(t => {
        const isCompleted = t.status === 'completed';
        const textStyle = isCompleted ? 'text-decoration: line-through; color: #888;' : '';
        
        taskList.innerHTML += `
            <div class="task-item" style="border-bottom: 1px solid #eee; padding: 15px; display: flex; justify-content: space-between; align-items: center; background: white; margin-bottom: 10px; border-radius: 8px;">
                <div style="${textStyle}">
                    <strong style="font-size: 1.1rem;">${t.title}</strong><br>
                    <small>${t.description || 'No description'}</small>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button onclick="toggleStatus(${t.id}, '${t.status}')" style="background: ${isCompleted ? '#6c757d' : '#28a745'}; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">
                        ${isCompleted ? 'Undo' : 'Done'}
                    </button>
                    <button onclick="editTask(${t.id}, '${t.title}', '${t.description}')" style="background: #ffc107; color: black; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">Edit</button>
                    <button onclick="deleteTask(${t.id})" style="background: #dc3545; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">Del</button>
                </div>
            </div>
        `;
    });
}

async function toggleStatus(id, currentStatus) {
    const token = localStorage.getItem('token');
    const newStatus = currentStatus === 'pending' ? 'completed' : 'pending';
    
    await fetch(`/api/tasks/${id}`, {
        method: 'PUT',
        headers: { 
            'Content-Type': 'application/json', 
            'Authorization': `Bearer ${token}` 
        },
        body: JSON.stringify({ status: newStatus })
    });
    loadTasks();
}

async function editTask(id, oldTitle, oldDesc) {
    const newTitle = prompt("Edit Task Title:", oldTitle);
    if (newTitle === null) return; // Cancel handle karega

    const token = localStorage.getItem('token');
    await fetch(`/api/tasks/${id}`, {
        method: 'PUT',
        headers: { 
            'Content-Type': 'application/json', 
            'Authorization': `Bearer ${token}` 
        },
        body: JSON.stringify({ title: newTitle })
    });
    loadTasks();
}

async function deleteTask(taskId) {
    if (!confirm("Pakka delete karna hai?")) return;

    const token = localStorage.getItem('token');
    const res = await fetch(`/api/tasks/${taskId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
    });

    if (res.status === 200) {
        loadTasks();
    }
}