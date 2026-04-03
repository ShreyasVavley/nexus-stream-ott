# Nexus Stream - OTT Platform Backend

A hand-crafted, lightweight OTT (Over-The-Top) backend and frontend implementation. Built with Python (FastAPI) and a clean, premium Vanilla CSS UI.

## Features
- **Subscription Middleware**: Prevents expired users from accessing content.
- **Trending View**: SQL-driven analytics showing the top 5 most viewed movies in the last 24 hours.
- **Normalized SQLite Schema**: Clean data structure for Users, Content, and Subscriptions.
- **Premium UI**: Cinematic dark-mode interface with smooth transitions and real-time interaction.

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Start the backend: `uvicorn main:app --reload`
3. Serve the frontend: `python -m http.server 3000` or just open `index.html`.

## Built With
- FastAPI & SQLite
- Vanilla HTML / CSS / JS
- Cinematic Design Principles
