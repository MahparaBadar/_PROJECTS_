# Recipe Fetcher Application Overview

## Description
Recipe Fetcher is a web application that helps users discover recipes based on their favorite cuisines. It integrates user authentication, favorite cuisine registration, and recipe retrieval using Google Custom Search JSON API, with a user-friendly interface powered by Streamlit.

## Technologies and Dependencies

- **Backend:**
  - **FastAPI:** For building high-performance APIs.
  - **SQLModel:** For database interactions.
  - **Google Generative AI:** For content generation.
  - **OAuth2 and Passlib:** For secure authentication and password management.
  - **Logging:** For tracking application events.

- **Frontend:**
  - **Streamlit:** For creating the web interface.

- **Database:**
  - **PostgreSQL:** For storing user data and favorite cuisines.

- **Containerization and Deployment:**
  - **Docker:** For packaging application components.
  - **Docker Compose:** For orchestrating multi-container setups.

## Application Workflow

1. **User Registration and Authentication:**
   - Users sign up and log in using FastAPI endpoints, with passwords securely hashed and stored.
   - Token-based authentication (OAuth2) manages user sessions.

2. **Favorite Cuisine Management:**
   - Authenticated users can register their favorite cuisines, stored in PostgreSQL.

3. **Recipe Retrieval:**
   - Users request recipes based on their favorite cuisines.
   - The backend fetches recipes using the Google Custom Search API and formats them in Markdown.

4. **Content Generation:**
   - Users provide prompts to generate content using Google Generative AI.

## Docker Configuration

- **Backend:**
  - Python 3.12 base image, dependencies installed via Poetry, exposed on port 8000.

- **Frontend:**
  - Python 3.12 base image, dependencies installed via Poetry, exposed on port 8501.

- **Compose File:**
  - Defines backend, frontend, and database services, with environment variables and persistent storage.

## Conclusion
Recipe Fetcher leverages modern technologies to provide a seamless experience for discovering new recipes, combining robust backend services, an intuitive frontend, and AI capabilities for personalized culinary content.
