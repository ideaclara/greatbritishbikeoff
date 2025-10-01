// API Base URL - will be updated with your Netlify function URL
const API_BASE_URL = '/.netlify/functions';

// Current filter state
let currentFilter = 'all';

// Load blog posts on page load
document.addEventListener('DOMContentLoaded', function() {
    loadBlogPosts();
    
    // Handle contact form submission
    document.getElementById('contact-form').addEventListener('submit', handleContactForm);
});

// Load blog posts
async function loadBlogPosts(filter = 'all') {
    const blogGrid = document.getElementById('blog-grid');
    blogGrid.innerHTML = '<div class="loading">Loading blog posts...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/get-posts?type=blog`);
        const posts = await response.json();
        
        if (posts.length === 0) {
            blogGrid.innerHTML = createSampleBlogPosts();
            return;
        }
        
        // Filter posts if needed
        const filteredPosts = filter === 'all' ? posts : posts.filter(post => 
            post.category.toLowerCase() === filter.toLowerCase()
        );
        
        if (filteredPosts.length === 0) {
            blogGrid.innerHTML = '<div class="loading">No posts found for this category.</div>';
            return;
        }
        
        blogGrid.innerHTML = filteredPosts.map(post => `
            <div class="card">
                <div class="card-image">${post.emoji || '📝'}</div>
                <div class="card-content">
                    <h3>${post.title}</h3>
                    <p>${post.excerpt}</p>
                    <a href="#" class="read-more">Read More →</a>
                    <div class="card-meta">
                        <span>📅 ${new Date(post.date).toLocaleDateString()}</span>
                        <span>🏷️ ${post.category}</span>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading blog posts:', error);
        blogGrid.innerHTML = createSampleBlogPosts();
    }
}

// Filter posts by category
function filterPosts(category) {
    currentFilter = category;
    
    // Update active category card
    document.querySelectorAll('.category-card').forEach(card => {
        card.classList.remove('active');
    });
    
    if (category !== 'all') {
        event.target.closest('.category-card').classList.add('active');
    }
    
    // Load filtered posts
    loadBlogPosts(category);
    
    // Scroll to blog section
    document.getElementById('blog').scrollIntoView({
        behavior: 'smooth'
    });
}

// Handle contact form submission
async function handleContactForm(e) {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        message: document.getElementById('message').value
    };
    
    const submitButton = e.target.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    submitButton.textContent = 'Sending...';
    submitButton.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/contact`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            alert('Message sent successfully! We\'ll get back to you soon.');
            e.target.reset();
        } else {
            throw new Error('Failed to send message');
        }
    } catch (error) {
        console.error('Error sending message:', error);
        alert('Sorry, there was an error sending your message. Please try again.');
    } finally {
        submitButton.textContent = originalText;
        submitButton.disabled = false;
    }
}

// Sample data functions (fallback when API is not available)
function createSampleBlogPosts() {
    return `
        <div class="card">
            <div class="card-image">🚴‍♂️</div>
            <div class="card-content">
                <h3>Cotswolds Cycling Adventure</h3>
                <p>A perfect weekend exploring the rolling hills and charming villages of the Cotswolds, discovering hidden gems and sampling local delicacies along the way.</p>
                <a href="#" class="read-more">Read More →</a>
                <div class="card-meta">
                    <span>📅 ${new Date().toLocaleDateString()}</span>
                    <span>🏷️ Cycling</span>
                </div>
            </div>
        </div>
        <div class="card">
            <div class="card-image">🍰</div>
            <div class="card-content">
                <h3>Best Cake Stops in Yorkshire</h3>
                <p>Discovering the finest tea rooms and bakeries along the Yorkshire Dales cycling routes. From traditional Yorkshire parkin to modern artisan treats.</p>
                <a href="#" class="read-more">Read More →</a>
                <div class="card-meta">
                    <span>📅 ${new Date().toLocaleDateString()}</span>
                    <span>🏷️ Food</span>
                </div>
            </div>
        </div>
        <div class="card">
            <div class="card-image">⚙️</div>
            <div class="card-content">
                <h3>Essential Gear for British Weather</h3>
                <p>A comprehensive guide to staying comfortable and safe while cycling through Britain's unpredictable weather conditions.</p>
                <a href="#" class="read-more">Read More →</a>
                <div class="card-meta">
                    <span>📅 ${new Date().toLocaleDateString()}</span>
                    <span>🏷️ Gear</span>
                </div>
            </div>
        </div>
        <div class="card">
            <div class="card-image">🗺️</div>
            <div class="card-content">
                <h3>Scotland's North Coast 500</h3>
                <p>An epic journey around Scotland's stunning coastline, featuring dramatic landscapes, historic castles, and unforgettable Highland hospitality.</p>
                <a href="#" class="read-more">Read More →</a>
                <div class="card-meta">
                    <span>📅 ${new Date().toLocaleDateString()}</span>
                    <span>🏷️ Travel</span>
                </div>
            </div>
        </div>
    `;
}



// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});