# Great British Bike Off

A cycling and food blogging website showcasing the best cycling routes and food discoveries across Britain.

## Architecture

- **Frontend**: Static HTML, CSS, and JavaScript
- **Backend**: Python serverless functions running on AWS Lambda via Netlify
- **Hosting**: Netlify static site hosting with serverless functions
- **Deployment**: Automated deployment from GitHub

## Features

- 🚴‍♂️ Featured cycling routes with difficulty ratings
- 🍽️ Food discovery posts with ratings and locations
- 📝 Blog posts about cycling adventures
- 📧 Contact form with serverless backend
- 📱 Responsive design for all devices

## Local Development

1. Install Netlify CLI:
   ```bash
   npm install -g netlify-cli
   ```

2. Start local development server:
   ```bash
   netlify dev
   ```

3. Open your browser to `http://localhost:8888`

## Deployment

### Option 1: Deploy to Netlify via GitHub

1. Push this repository to GitHub
2. Connect your GitHub repository to Netlify
3. Netlify will automatically deploy on every push to main branch

### Option 2: Manual Deploy

1. Install Netlify CLI and login:
   ```bash
   npm install -g netlify-cli
   netlify login
   ```

2. Deploy:
   ```bash
   netlify deploy --prod
   ```

## Project Structure

```
great-british-bike-off/
├── index.html              # Main HTML file
├── styles.css              # CSS styles
├── script.js               # Frontend JavaScript
├── netlify/
│   └── functions/
│       ├── get-posts.py    # API endpoint for blog posts/routes/food
│       └── contact.py      # Contact form handler
├── netlify.toml            # Netlify configuration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## API Endpoints

- `GET /.netlify/functions/get-posts?type=blog` - Get blog posts
- `GET /.netlify/functions/get-posts?type=route` - Get cycling routes
- `GET /.netlify/functions/get-posts?type=food` - Get food posts
- `POST /.netlify/functions/contact` - Submit contact form

## Customization

### Adding New Content

Edit the sample data in `netlify/functions/get-posts.py` to add your own:
- Blog posts
- Cycling routes
- Food discoveries

### Styling

Modify `styles.css` to customize the appearance:
- Colors are defined using CSS custom properties
- Responsive breakpoints are at 768px
- Grid layouts automatically adapt to screen size

### Functionality

Extend `script.js` to add new features:
- Search functionality
- Filtering by category/difficulty
- User authentication
- Comments system

## Environment Variables

For production, you may want to add:
- `DATABASE_URL` - Database connection string
- `EMAIL_API_KEY` - Email service API key
- `ANALYTICS_ID` - Google Analytics tracking ID

## License

MIT License - feel free to use this project as a starting point for your own cycling blog!