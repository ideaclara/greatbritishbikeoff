// API Base URL - will be updated with your Netlify function URL
const API_BASE_URL = '/.netlify/functions';

// Load blog posts on page load
document.addEventListener('DOMContentLoaded', function() {
    loadBlogPosts();
    loadRoutes();
    loadFoodPosts();
    
    // Handle contact form submission
    document.getElementById('contact-form').addEventListener('submit', handleContactForm);
});

// Load blog posts
async function loadBlogPosts() {
    const blogGrid = document.getElementById('blog-grid');
    blogGrid.innerHTML = '<div class="loading">Loading blog posts...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/get-posts?type=blog`);
        const posts = await response.json();
        
        if (posts.length === 0) {
            blogGrid.innerHTML = '<div class="loading">No blog posts yet. Check back soon!</div>';
            return;
        }
        
        blogGrid.innerHTML = posts.map(post => `
            <div class="card">
                <div class="card-image">${post.emoji || '📝'}</div>
                <div class="card-content">
                    <h3>${post.title}</h3>
                    <p>${post.excerpt}</p>
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

// Load cycling routes
async function loadRoutes() {
    const routesGrid = document.getElementById('routes-grid');
    routesGrid.innerHTML = '<div class="loading">Loading routes...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/get-posts?type=route`);
        const routes = await response.json();
        
        if (routes.length === 0) {
            routesGrid.innerHTML = createSampleRoutes();
            return;
        }
        
        routesGrid.innerHTML = routes.map(route => `
            <div class="card">
                <div class="card-image">${route.emoji || '🚴‍♂️'}</div>
                <div class="card-content">
                    <h3>${route.title}</h3>
                    <p>${route.description}</p>
                    <div class="card-meta">
                        <span>📏 ${route.distance} miles</span>
                        <span>⛰️ ${route.difficulty}</span>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading routes:', error);
        routesGrid.innerHTML = createSampleRoutes();
    }
}

// Load food posts
async function loadFoodPosts() {
    const foodGrid = document.getElementById('food-grid');
    foodGrid.innerHTML = '<div class="loading">Loading food discoveries...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/get-posts?type=food`);
        const foodPosts = await response.json();
        
        if (foodPosts.length === 0) {
            foodGrid.innerHTML = createSampleFoodPosts();
            return;
        }
        
        foodGrid.innerHTML = foodPosts.map(food => `
            <div class="card">
                <div class="card-image">${food.emoji || '🍽️'}</div>
                <div class="card-content">
                    <h3>${food.title}</h3>
                    <p>${food.description}</p>
                    <div class="card-meta">
                        <span>📍 ${food.location}</span>
                        <span>⭐ ${food.rating}/5</span>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading food posts:', error);
        foodGrid.innerHTML = createSampleFoodPosts();
    }
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
                <p>A perfect weekend exploring the rolling hills and charming villages of the Cotswolds, with stops at local pubs and farm shops.</p>
                <div class="card-meta">
                    <span>📅 ${new Date().toLocaleDateString()}</span>
                    <span>🏷️ Adventure</span>
                </div>
            </div>
        </div>
        <div class="card">
            <div class="card-image">🍰</div>
            <div class="card-content">
                <h3>Best Cake Stops in Yorkshire</h3>
                <p>Discovering the finest tea rooms and bakeries along the Yorkshire Dales cycling routes.</p>
                <div class="card-meta">
                    <span>📅 ${new Date().toLocaleDateString()}</span>
                    <span>🏷️ Food</span>
                </div>
            </div>
        </div>
    `;
}

function createSampleRoutes() {
    return `
        <div class="card">
            <div class="card-image">🚴‍♂️</div>
            <div class="card-content">
                <h3>Thames Path Challenge</h3>
                <p>Follow the historic Thames Path from Oxford to Windsor, with plenty of riverside pubs along the way.</p>
                <div class="card-meta">
                    <span>📏 45 miles</span>
                    <span>⛰️ Easy</span>
                </div>
            </div>
        </div>
        <div class="card">
            <div class="card-image">⛰️</div>
            <div class="card-content">
                <h3>Peak District Loop</h3>
                <p>Challenging route through the stunning Peak District with breathtaking views and hearty pub meals.</p>
                <div class="card-meta">
                    <span>📏 62 miles</span>
                    <span>⛰️ Hard</span>
                </div>
            </div>
        </div>
        <div class="card">
            <div class="card-image">🌊</div>
            <div class="card-content">
                <h3>Cornwall Coastal Ride</h3>
                <p>Spectacular coastal cycling with fresh seafood stops and stunning ocean views.</p>
                <div class="card-meta">
                    <span>📏 38 miles</span>
                    <span>⛰️ Medium</span>
                </div>
            </div>
        </div>
    `;
}

function createSampleFoodPosts() {
    return `
        <div class="card">
            <div class="card-image">🍺</div>
            <div class="card-content">
                <h3>The King's Head, Chipping Campden</h3>
                <p>Traditional Cotswolds pub with excellent local ales and hearty cyclist-friendly portions.</p>
                <div class="card-meta">
                    <span>📍 Chipping Campden</span>
                    <span>⭐ 4.5/5</span>
                </div>
            </div>
        </div>
        <div class="card">
            <div class="card-image">🥧</div>
            <div class="card-content">
                <h3>Betty's Tea Rooms</h3>
                <p>Iconic Yorkshire tea room serving the best fat rascals and afternoon tea in Harrogate.</p>
                <div class="card-meta">
                    <span>📍 Harrogate</span>
                    <span>⭐ 5/5</span>
                </div>
            </div>
        </div>
        <div class="card">
            <div class="card-image">🦞</div>
            <div class="card-content">
                <h3>The Seafood Restaurant</h3>
                <p>Fresh Cornwall seafood with stunning harbor views - perfect after a coastal ride.</p>
                <div class="card-meta">
                    <span>📍 Padstow</span>
                    <span>⭐ 4.8/5</span>
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