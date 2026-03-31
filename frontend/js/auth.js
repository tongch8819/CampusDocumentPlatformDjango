// js/auth.js

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const loginError = document.getElementById('loginError');

    // Only attach the login listener if we are on the login page
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault(); // Prevent the page from reloading

            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            try {
                // We use standard fetch here instead of apiFetch because 
                // we don't need to attach a token to get a token.
                // Note: BASE_URL is defined in api.js, which is loaded before auth.js
                const response = await fetch(`${BASE_URL}token/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username, password }),
                });

                if (response.ok) {
                    const data = await response.json();
                    
                    // Store the tokens securely in the browser
                    localStorage.setItem('access_token', data.access);
                    localStorage.setItem('refresh_token', data.refresh);
                    
                    // Hide any previous errors
                    loginError.classList.add('d-none');
                    
                    // Redirect to the main dashboard
                    window.location.href = 'category.html';
                } else {
                    // Show the error alert defined in Bootstrap
                    loginError.classList.remove('d-none');
                    document.getElementById('password').value = ''; // Clear the password field
                }
            } catch (error) {
                console.error("Login Error:", error);
                loginError.textContent = "Unable to connect to the server.";
                loginError.classList.remove('d-none');
            }
        });
    }
});

/**
 * Utility function to check if a user is logged in.
 * You will call this at the top of category.html, upload.html, etc.
 */
function requireAuth() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = 'index.html';
    }
}

/**
 * Utility function to log the user out.
 */
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = 'index.html';
}