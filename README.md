# Trip Planner

A modern web application for planning trips with AI-powered recommendations.

## Features

- Personalized travel recommendations based on user preferences
- Smart budget planning and optimization
- AI-powered itinerary generation
- Interactive user interface with dark mode support
- Responsive design for all devices

## Technologies Used

- HTML5, CSS3, JavaScript
- Bootstrap 5
- Custom animations and transitions
- Node.js and Express for backend
- Python with Flask for ML service
- MongoDB for database

## Run Commands

### Backend
```bash
cd backend
npm install
npm start
```

### ML Service
```bash
cd ml-service
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
# For static demo page
cd frontend/public
# Open demo.html in browser

# For React application (if applicable)
cd frontend
npm install
npm start
```

## Demo

Open `frontend/public/demo.html` in your browser to see the application in action.

## Getting Started

1. Clone the repository
2. Set up MongoDB, backend, and ML service following the instructions above
3. Navigate to the frontend/public directory
4. Open demo.html in your browser or start the React application with npm start

## Deployment Options

### Quick Deploy (Demo Site Only)
```bash
# Deploy the static demo site to Netlify
npm install -g netlify-cli
netlify deploy
```

### Full Application Deployment
#### Using Docker (Recommended)
```bash
# Start all services
docker-compose up -d

# To stop services
docker-compose down
```

#### Cloud Deployment
- **Frontend**: Deploy to Netlify, Vercel, or GitHub Pages
- **Backend**: Deploy to Heroku, Railway, or Render
- **ML Service**: Deploy to Heroku or Railway
- **Database**: Use MongoDB Atlas

## Screenshots

![Trip Planner Screenshot](https://via.placeholder.com/800x400) 