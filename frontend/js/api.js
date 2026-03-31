// Base URL for our Django backend
const BASE_URL = 'http://127.0.0.1:8000/api/';

/**
 * A wrapper for the native fetch API that automatically attaches 
 * the JWT Access token to the headers.
 */
async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem('access_token');
    
    // Set up default headers, allowing overrides
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    // If we have a token, attach it for authorization
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    // If we are uploading a file (FormData), the browser automatically sets the 
    // Content-Type boundary, so we must delete our manual one.
    if (options.body instanceof FormData) {
        delete headers['Content-Type'];
    }

    const response = await fetch(`${BASE_URL}${endpoint}`, {
        ...options,
        headers,
    });

    // Handle 401 Unauthorized (Token expired)
    if (response.status === 401) {
        console.error("Session expired. Please log in again.");
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = 'index.html'; // Redirect to login
        throw new Error("Unauthorized");
    }

    return response;
}