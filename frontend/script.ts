// API configuration
const API_BASE_URL = 'http://localhost:5000';

// DOM Elements
const loginForm = document.getElementById('loginForm') as HTMLElement;
const registerForm = document.getElementById('registerForm') as HTMLElement;
const welcomeScreen = document.getElementById('welcomeScreen') as HTMLElement;
const loginFormElement = document.getElementById('loginFormElement') as HTMLFormElement;
const registerFormElement = document.getElementById('registerFormElement') as HTMLFormElement;
const loginError = document.getElementById('loginError') as HTMLElement;
const registerError = document.getElementById('registerError') as HTMLElement;
const welcomeMessage = document.getElementById('welcomeMessage') as HTMLElement;

// Toggle form visibility
function showForm(form: 'login' | 'register' | 'welcome'): void {
    loginForm.classList.add('hidden');
    registerForm.classList.add('hidden');
    welcomeScreen.classList.add('hidden');

    switch (form) {
        case 'login':
            loginForm.classList.remove('hidden');
            break;
        case 'register':
            registerForm.classList.remove('hidden');
            break;
        case 'welcome':
            welcomeScreen.classList.remove('hidden');
            break;
    }

    // Clear any error messages
    loginError.classList.remove('show');
    registerError.classList.remove('show');
}

// Display error message
function showError(errorElement: HTMLElement, message: string): void {
    errorElement.textContent = message;
    errorElement.classList.add('show');
}

// API call helper
async function apiCall(endpoint: string, data: { username: string; password: string }): Promise<Response> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
    return response;
}

// Register handler
async function handleRegister(event: Event): Promise<void> {
    event.preventDefault();

    const formData = new FormData(registerFormElement);
    const username = formData.get('username') as string;
    const password = formData.get('password') as string;

    if (!username || !password) {
        showError(registerError, 'Username and password are required');
        return;
    }

    try {
        const response = await apiCall('/register', { username, password });
        const result = await response.json();

        if (result.success) {
            // Registration successful - switch to login
            alert('Registration successful! You can now log in.');
            registerFormElement.reset();
            showForm('login');
        } else {
            showError(registerError, result.message || 'Registration failed');
        }
    } catch (error) {
        showError(registerError, 'Failed to connect to server. Make sure the backend is running.');
        console.error('Registration error:', error);
    }
}

// Login handler
async function handleLogin(event: Event): Promise<void> {
    event.preventDefault();

    const formData = new FormData(loginFormElement);
    const username = formData.get('username') as string;
    const password = formData.get('password') as string;

    if (!username || !password) {
        showError(loginError, 'Username and password are required');
        return;
    }

    try {
        const response = await apiCall('/login', { username, password });
        const result = await response.json();

        if (result.success) {
            // Login successful - show welcome screen
            welcomeMessage.textContent = `Welcome, ${result.username}!`;
            loginFormElement.reset();
            showForm('welcome');
        } else {
            showError(loginError, result.message || 'Login failed');
        }
    } catch (error) {
        showError(loginError, 'Failed to connect to server. Make sure the backend is running.');
        console.error('Login error:', error);
    }
}

// Event Listeners
document.getElementById('showRegister')?.addEventListener('click', () => showForm('register'));
document.getElementById('showLogin')?.addEventListener('click', () => showForm('login'));
document.getElementById('logout')?.addEventListener('click', () => showForm('login'));

loginFormElement.addEventListener('submit', handleLogin);
registerFormElement.addEventListener('submit', handleRegister);

// Initialize
showForm('login');
