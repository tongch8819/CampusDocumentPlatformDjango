// js/ui.js

document.addEventListener('DOMContentLoaded', () => {
    // 1. Immediately protect the page. If no token exists, redirect to login.
    if (typeof requireAuth === 'function') {
        requireAuth();
    }

    const resourceGrid = document.getElementById('resourceGrid');
    const searchBtn = document.getElementById('searchBtn');
    const searchInput = document.getElementById('searchInput');

    // 2. If we are on the category page, load the materials
    if (resourceGrid) {
        loadMaterials(); // Initial load

        // Allow searching by clicking the button
        searchBtn.addEventListener('click', () => {
            loadMaterials(searchInput.value);
        });

        // Allow searching by pressing "Enter" in the input field
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                loadMaterials(searchInput.value);
            }
        });
    }
});

/**
 * Fetches materials from the Django backend.
 * Optionally appends a search query to the URL.
 */
async function loadMaterials(searchQuery = '') {
    const grid = document.getElementById('resourceGrid');
    
    try {
        let endpoint = 'resources/list/';
        if (searchQuery) {
            // Encode the query so spaces and special characters don't break the URL
            endpoint += `?search=${encodeURIComponent(searchQuery)}`;
        }

        const response = await apiFetch(endpoint);
        
        if (response.ok) {
            const materials = await response.json();
            renderMaterials(materials);
        } else {
            grid.innerHTML = `<div class="alert alert-danger">Failed to load resources.</div>`;
        }
    } catch (error) {
        console.error("Fetch Error:", error);
        grid.innerHTML = `<div class="alert alert-danger">Network error. Please try again.</div>`;
    }
}

function renderMaterials(materials, containerId = 'resourceGrid') {
    const grid = document.getElementById(containerId);
    if (!grid) return; 

    grid.innerHTML = ''; 

    if (materials.length === 0) {
        grid.innerHTML = '<div class="col-12"><p class="text-center text-muted fs-5 mt-4">No materials found.</p></div>';
        return;
    }

    // 1. Safely decode token to get the current user ID
    let currentUserId = null;
    const token = localStorage.getItem('access_token');
    if (token) {
        try {
            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            currentUserId = JSON.parse(window.atob(base64)).user_id;
        } catch (e) {
            console.error("Token decode error in renderMaterials");
        }
    }

    materials.forEach(mat => {
        const tagsHtml = mat.tags.map(tag => `<span class="badge bg-info text-dark me-1 mb-1">${tag.name}</span>`).join('');
        const uploadDate = new Date(mat.upload_time).toLocaleDateString();
        const heartIcon = mat.is_favorited ? '♥' : '♡';
        const heartClass = mat.is_favorited ? 'btn-danger' : 'btn-outline-danger';

        // 2. Check ownership to conditionally render the trash can button
        const isOwner = currentUserId && mat.uploader.id == currentUserId;
        const deleteBtnHtml = isOwner 
            ? `<button class="btn btn-outline-danger delete-card-btn" data-id="${mat.id}" title="Delete Document">🗑️</button>` 
            : '';

        const cardHtml = `
            <div class="col-md-6 col-lg-4 mb-4 card-wrapper">
                <div class="card h-100 shadow-sm border-0">
                    <div class="card-body d-flex flex-column">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <h5 class="card-title text-truncate mb-0" title="${mat.title}">${mat.title}</h5>
                            <button class="btn btn-sm ${heartClass} favorite-toggle" data-id="${mat.id}">
                                ${heartIcon}
                            </button>
                        </div>
                        
                        <h6 class="card-subtitle mb-3 text-muted small">Uploaded by ${mat.uploader.username}</h6>
                        <div class="mb-3">${tagsHtml || '<span class="badge bg-secondary">Untagged</span>'}</div>
                        
                        <div class="mt-auto">
                            <p class="card-text small text-muted mb-2">Date: ${uploadDate}</p>
                            <div class="d-flex gap-2">
                                <a href="details.html?id=${mat.id}" class="btn btn-primary flex-grow-1">View Details</a>
                                ${deleteBtnHtml}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        grid.innerHTML += cardHtml;
    });
}

// --- GLOBAL CARD INTERACTIVITY (Favorites & Deletions) ---
document.addEventListener('click', async (e) => {
    
    // 1. Handle Favorite Toggle
    const favBtn = e.target.closest('.favorite-toggle');
    if (favBtn) {
        const materialId = favBtn.getAttribute('data-id');
        favBtn.disabled = true; 
        try {
            const response = await apiFetch(`resources/${materialId}/favorite/`, { method: 'POST' });
            if (response.ok) {
                if (favBtn.textContent.trim() === '♡') {
                    favBtn.textContent = '♥';
                    favBtn.classList.replace('btn-outline-danger', 'btn-danger');
                } else {
                    favBtn.textContent = '♡';
                    favBtn.classList.replace('btn-danger', 'btn-outline-danger');
                }
            }
        } catch (error) {
            console.error("Favorite toggle failed", error);
        } finally {
            favBtn.disabled = false;
        }
    }

    // 2. Handle Dashboard Card Deletion
    const delBtn = e.target.closest('.delete-card-btn');
    if (delBtn) {
        const materialId = delBtn.getAttribute('data-id');
        if (confirm("Permanently delete this document? This cannot be undone.")) {
            delBtn.disabled = true;
            try {
                const response = await apiFetch(`resources/${materialId}/delete/`, { method: 'DELETE' });
                if (response.ok) {
                    // Instantly remove the card from the screen without reloading the page
                    delBtn.closest('.card-wrapper').remove(); 
                } else {
                    alert("Failed to delete the document.");
                    delBtn.disabled = false;
                }
            } catch (error) {
                console.error("Delete failed", error);
                alert("Network error.");
                delBtn.disabled = false;
            }
        }
    }
});
// ... existing ui.js code ...

// --- UPLOAD PAGE LOGIC ---
const uploadForm = document.getElementById('uploadForm');

if (uploadForm) {
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Stop standard form submission

        const titleInput = document.getElementById('resourceTitle');
        const fileInput = document.getElementById('resourceFile');
        const statusDiv = document.getElementById('uploadStatus');
        const uploadBtnText = document.getElementById('uploadBtnText');
        const uploadSpinner = document.getElementById('uploadSpinner');
        const submitBtn = document.getElementById('uploadBtn');

        // Basic validation
        if (!fileInput.files.length) {
            showStatus('Please select a file.', 'danger');
            return;
        }

        // Prepare the UI for loading
        submitBtn.disabled = true;
        uploadBtnText.textContent = 'Processing... ';
        uploadSpinner.classList.remove('d-none');
        statusDiv.classList.add('d-none');

        // Package the data for a multipart/form-data request
        const formData = new FormData();
        formData.append('title', titleInput.value);
        formData.append('file', fileInput.files[0]);

        try {
            // apiFetch handles the Authorization header and correctly ignores Content-Type for FormData
            const response = await apiFetch('resources/upload/', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                showStatus(`Success! File categorized as: ${result.status}. View it on the dashboard.`, 'success');
                uploadForm.reset(); // Clear the form
            } else {
                // Handle specific errors, like duplicates (409)
                showStatus(result.error || 'Upload failed. Please try again.', 'danger');
            }
        } catch (error) {
            console.error("Upload Error:", error);
            showStatus('Network error occurred.', 'danger');
        } finally {
            // Restore the UI state
            submitBtn.disabled = false;
            uploadBtnText.textContent = 'Upload and Process';
            uploadSpinner.classList.add('d-none');
        }
    });

    // Helper function to show Bootstrap alerts
    function showStatus(message, type) {
        const statusDiv = document.getElementById('uploadStatus');
        statusDiv.textContent = message;
        statusDiv.className = `alert alert-${type} mt-3`;
        statusDiv.classList.remove('d-none');
    }
}



// --- DETAILS PAGE LOGIC ---
const detailContent = document.getElementById('detailContent');
if (detailContent) {
    // Get the material ID from the URL (e.g., details.html?id=1)
    const urlParams = new URLSearchParams(window.location.search);
    const materialId = urlParams.get('id');

    if (!materialId) {
        window.location.href = 'category.html'; // Kick them back if no ID
    } else {
        loadMaterialDetails(materialId);
    }
}

async function loadMaterialDetails(id) {
    try {
        const response = await apiFetch(`resources/${id}/`);
        if (!response.ok) throw new Error("Material not found");
        
        const mat = await response.json();
        
        // Populate basic info
        document.getElementById('docTitle').textContent = mat.title;
        document.getElementById('docUploader').textContent = mat.uploader.username;
        document.getElementById('docDate').textContent = new Date(mat.upload_time).toLocaleDateString();
        document.getElementById('docText').textContent = mat.extracted_text || "No text could be extracted.";
        document.getElementById('downloadBtn').href = mat.file_url;

        // Populate tags
        const tagsHtml = mat.tags.map(tag => `<span class="badge bg-info text-dark me-1">${tag.name}</span>`).join('');
        document.getElementById('docTags').innerHTML = tagsHtml || '<span class="badge bg-secondary">Untagged</span>';

        // 1. Safely decode the JWT (Handles Base64Url encoding and padding)
        const token = localStorage.getItem('access_token');
        let currentUserId = null;
        try {
            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            const tokenPayload = JSON.parse(window.atob(base64));
            currentUserId = tokenPayload.user_id;
        } catch (e) {
            console.error("Error decoding token:", e);
        }

        // 2. Use '==' instead of '===' to prevent String vs Integer mismatches
        if (currentUserId && mat.uploader.id == currentUserId) {
            
            // Show owner controls
            document.getElementById('ownerControls').classList.remove('d-none');
            
            // 3. Safely handle old files that might not have sharing settings yet
            const currentPermission = mat.sharing_settings ? mat.sharing_settings.permission_type : 'PRIVATE';
            document.getElementById('sharingSelect').value = currentPermission;
            
            // Wire up the update permission button
            document.getElementById('updateShareBtn').addEventListener('click', async () => {
                const newPerm = document.getElementById('sharingSelect').value;
                const res = await apiFetch(`resources/${id}/share/`, {
                    method: 'PATCH',
                    body: JSON.stringify({ permission_type: newPerm })
                });
                if (res.ok) {
                    const status = document.getElementById('shareStatus');
                    status.classList.remove('d-none');
                    setTimeout(() => status.classList.add('d-none'), 3000);
                }
            });
            
            // Wire up the Details Page Delete button
            const deleteBtn = document.getElementById('deleteDocBtn');
            if (deleteBtn) {
                deleteBtn.addEventListener('click', async (e) => {
                    e.preventDefault(); 
                    
                    if (confirm("Are you sure you want to permanently delete this document? This cannot be undone.")) {
                        
                        deleteBtn.disabled = true;
                        deleteBtn.textContent = "Deleting...";

                        try {
                            const res = await apiFetch(`resources/${id}/delete/`, { method: 'DELETE' });
                            
                            if (res.ok) {
                                // 1. Give visual feedback without blocking the thread with an alert()
                                deleteBtn.textContent = "Deleted!";
                                deleteBtn.classList.replace('btn-outline-danger', 'btn-success');
                                
                                // 2. Push the navigation to the very end of the execution stack
                                setTimeout(() => {
                                    window.location.href = 'category.html';
                                }, 400); // Wait 400ms so the user sees the "Deleted!" success state

                            } else {
                                const errorData = await res.json();
                                alert(errorData.detail || "Failed to delete the document.");
                                deleteBtn.disabled = false;
                                deleteBtn.textContent = "Delete Document";
                            }
                        } catch (error) {
                            console.error("Delete Error:", error);
                            alert("A network error occurred.");
                            deleteBtn.disabled = false;
                            deleteBtn.textContent = "Delete Document";
                        }
                    }
                });
            }
        }
        
        // Wire up the Favorite button
        document.getElementById('favoriteBtn').addEventListener('click', async () => {
            const res = await apiFetch(`resources/${id}/favorite/`, { method: 'POST' });
            if (res.ok) {
                const data = await res.json();
                alert(data.message); // Simple alert for now
            }
        });

        // Hide spinner and show content
        document.getElementById('loadingSpinner').classList.add('d-none');
        detailContent.classList.remove('d-none');

    } catch (error) {
        console.error(error);
        document.getElementById('loadingSpinner').innerHTML = '<div class="alert alert-danger">Error loading material or you do not have permission to view it.</div>';
    }
}


// ... existing ui.js code ...

// --- PROFILE PAGE LOGIC ---
const profileTabs = document.getElementById('profileTabs');

if (profileTabs) {
    loadProfileData();
}

async function loadProfileData() {
    try {
        // 1. Decode the JWT token to get the current user's ID
        const token = localStorage.getItem('access_token');
        const tokenPayload = JSON.parse(atob(token.split('.')[1]));
        const currentUserId = tokenPayload.user_id;

        // 2. Fetch both lists simultaneously for better performance
        const [uploadsRes, favoritesRes] = await Promise.all([
            apiFetch(`resources/list/?uploader=${currentUserId}`),
            apiFetch(`resources/list/?is_favorited=true`)
        ]);

        // 3. Render Uploads
        if (uploadsRes.ok) {
            const uploads = await uploadsRes.json();
            renderMaterials(uploads, 'myUploadsGrid');
        } else {
            document.getElementById('myUploadsGrid').innerHTML = '<div class="alert alert-danger">Failed to load uploads.</div>';
        }

        // 4. Render Favorites
        if (favoritesRes.ok) {
            const favorites = await favoritesRes.json();
            renderMaterials(favorites, 'myFavoritesGrid');
        } else {
            document.getElementById('myFavoritesGrid').innerHTML = '<div class="alert alert-danger">Failed to load favorites.</div>';
        }

    } catch (error) {
        console.error("Profile Load Error:", error);
        document.getElementById('myUploadsGrid').innerHTML = '<div class="alert alert-danger">Network error.</div>';
        document.getElementById('myFavoritesGrid').innerHTML = '<div class="alert alert-danger">Network error.</div>';
    }
}