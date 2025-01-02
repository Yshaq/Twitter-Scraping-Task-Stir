# GitHub Trending Topics Scraper

This application logs into Twitter, scrapes the top 5 trending topics using Selenium with Python, and displays them on a frontend built with React and Vite.

https://github.com/user-attachments/assets/af2d97ba-8df4-4cc8-ad8a-7870caa62be3

## Features

- Automated web scraping of Twitter trending topics.
- Backend powered by Python and Flask.
- Frontend powered by React and Vite.

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your system.
- Environment variables set up as described below.

## Setup Instructions

### Step 1: Clone the Repository
```bash
git clone <repository_url>
cd <repository_name>
```

### Step 2: Configure Environment Variables
1. Copy the `.env_template` file to `.env`:
   ```bash
   cp .env_template .env
   ```
2. Fill in the required details in the `.env` file:
   - `MONGODB_URI`
   - `TWITTER_EMAIL`
   - `TWITTER_USERNAME`
   - `TWITTER_PASSWORD`
   - `USE_PROXY` (= 0 or 1)
   - `PROXY_HOST` (The below are Optional, only needed if you want to use proxy)
   - `PROXY_PORT`
   - `PROXY_USER`
   - `PROXY_PASS`

### Step 3: Build and Run the Application
1. Build the Docker containers:
   ```bash
   docker compose build
   ```
2. Start the application:
   ```bash
   docker compose up
   ```

### Step 4: Access the Application
- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend: [http://localhost:5000](http://localhost:5000)

## Usage
Visit [http://localhost:5173](http://localhost:5173) in your browser to use the application.
