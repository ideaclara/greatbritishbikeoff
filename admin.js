// Admin panel JavaScript
const API_BASE_URL = '/.netlify/functions';

// Get password from environment or use default
async function getAdminPassword() {
    try {
        const response = await fetch(`${API_BASE_URL}/get-config`);
        const config = await response.json();
        return config.adminPassword || 'bikeoff2025';
    } catch (error) {
        return 'bikeoff2025'; // Fallback password
    }
}

// Check authentication on page load
document.addEventListener('DOMContentLoaded', function() {
    // Check if already logged in
    if (sessionStorage.getItem('adminAuthenticated') === 'true') {
        showAdminPanel();
    }
    
    // Handle login form
    document.getElementById('login-form').addEventListener('submit', handleLogin);
});

// Handle login
async function handleLogin(e) {
    e.preventDefault();
    const password = document.getElementById('password').value;
    const adminPassword = await getAdminPassword();
    
    if (password === adminPassword) {
        sessionStorage.setItem('adminAuthenticated', 'true');
        showAdminPanel();
    } else {
        alert('Incorrect password!');
        document.getElementById('password').value = '';
    }
}

// Show admin panel after successful login
function showAdminPanel() {
    document.getElementById('login-container').style.display = 'none';
    document.getElementById('admin-panel').style.display = 'block';
    
    loadExistingPosts();
    
    // Handle form submission
    document.getElementById('blog-form').addEventListener('submit', handleFormSubmit);
}

// Extract YouTube video ID from URL
function extractYouTubeId(url) {
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
    const match = url.match(regExp);
    return (match && match[2].length === 11) ? match[2] : null;
}

// Preview YouTube video
function previewYouTube() {
    const url = document.getElementById('youtube-url').value;
    const preview = document.getElementById('youtube-preview');
    
    if (!url) {
        preview.style.display = 'none';
        return;
    }
    
    const videoId = extractYouTubeId(url);
    if (!videoId) {
        alert('Invalid YouTube URL. Please use a valid YouTube video URL.');
        return;
    }
    
    // Show thumbnail
    const thumbnail = document.getElementById('youtube-thumbnail');
    thumbnail.src = `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`;
    
    // Try to get video title (this would need YouTube API in production)
    document.getElementById('youtube-title').textContent = 'YouTube Video';
    
    preview.style.display = 'block';
}

// Handle form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const postData = {
        title: formData.get('title'),
        excerpt: formData.get('excerpt'),
        content: formData.get('content'),
        category: formData.get('category'),
        emoji: formData.get('emoji') || '📝',
        youtubeUrl: formData.get('youtube-url'),
        date: new Date().toISOString(),
        id: Date.now() // Simple ID generation
    };
    
    // Add YouTube video ID if URL provided
    if (postData.youtubeUrl) {
        postData.youtubeId = extractYouTubeId(postData.youtubeUrl);
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/create-post`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(postData)
        });
        
        if (response.ok) {
            alert('Post created successfully!');
            e.target.reset();
            document.getElementById('youtube-preview').style.display = 'none';
            loadExistingPosts();
        } else {
            throw new Error('Failed to create post');
        }
    } catch (error) {
        console.error('Error creating post:', error);
        
        // Fallback: Save to localStorage for demo purposes
        const posts = JSON.parse(localStorage.getItem('blogPosts') || '[]');
        posts.unshift(postData);
        localStorage.setItem('blogPosts', JSON.stringify(posts));
        
        alert('Post saved locally! (In production, this would save to your database)');
        e.target.reset();
        document.getElementById('youtube-preview').style.display = 'none';
        loadExistingPosts();
    }
}

// Load existing posts
async function loadExistingPosts() {
    const container = document.getElementById('posts-container');
    
    try {
        // Try to load from API first
        const response = await fetch(`${API_BASE_URL}/get-posts?type=blog`);
        const posts = await response.json();
        displayPosts(posts);
    } catch (error) {
        // Fallback to localStorage
        const posts = JSON.parse(localStorage.getItem('blogPosts') || '[]');
        displayPosts(posts);
    }
}

// Display posts in admin panel
function displayPosts(posts) {
    const container = document.getElementById('posts-container');
    
    if (posts.length === 0) {
        container.innerHTML = '<p>No posts yet. Create your first post above!</p>';
        return;
    }
    
    container.innerHTML = posts.map(post => `
        <div class="post-item">
            <div class="post-info">
                <h4>${post.title}</h4>
                <p>${post.category} • ${new Date(post.date).toLocaleDateString()}</p>
                ${post.youtubeId ? '<p>📹 Includes YouTube video</p>' : ''}
            </div>
            <div class="post-actions">
                <button class="btn-secondary" onclick="editPost(${post.id})">Edit</button>
                <button class="btn-secondary" onclick="deletePost(${post.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

// Edit post (placeholder)
function editPost(id) {
    alert('Edit functionality would be implemented here. For now, you can delete and recreate the post.');
}

// Delete post
function deletePost(id) {
    if (!confirm('Are you sure you want to delete this post?')) {
        return;
    }
    
    // For demo purposes, delete from localStorage
    const posts = JSON.parse(localStorage.getItem('blogPosts') || '[]');
    const updatedPosts = posts.filter(post => post.id !== id);
    localStorage.setItem('blogPosts', JSON.stringify(updatedPosts));
    
    loadExistingPosts();
    alert('Post deleted!');
}

// Auto-resize textareas
document.addEventListener('input', function(e) {
    if (e.target.tagName === 'TEXTAREA') {
        e.target.style.height = 'auto';
        e.target.style.height = e.target.scrollHeight + 'px';
    }
});