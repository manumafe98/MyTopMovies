# My Top Movies

Welcome to My Top Movies! This Python application allows you to create an account, sign in, and rank and review your favorite movies. It provides a backend built with the FastAPI framework and uses a PostgreSQL database to store user information and movie lists.

## Features

- User Registration: Create a new account with a unique username, email, and password.
- User Login: Sign in to your account using your username and password.
- Add Movies: Add your favorite movies to your list.
- Rank Movies: Rank your movies based on your personal preference.
- Review Movies: Write and update reviews for the movies in your list.

## Endpoints

- `GET /` : Renders the home page with the user's movie list, allowing ranking and review updates.
- `GET /edit/{movie_id}` : Renders the edit page for a specific movie, where you can update its ranking and review.
- `POST /edit/{movie_id}` : Handles the form submission in the edit page.
- `GET /add` : Renders the add page to search and select movies to add to your list.
- `POST /add` : Handles the form submission in the add page.
- `GET /delete/{movie_id}` : Deletes a movie from your list.
- `GET /get_movie_data/{movie_id}` : Retrieves detailed movie information from an external API and adds it to your list.
- `GET /user/signup` : Renders the signup page to create a new user account.
- `POST /user/signup` : Handles the form submission in the signup page.
- `GET /user/signin` : Renders the signin page for users to sign in to their accounts.
- `POST /user/signin` : Handles the form submission in the signin page.
- `GET /logout` : Logs out the current user and redirects to the login page.
- `GET /forgot_password` : Renders the forgot password page for users to change their password.
- `POST /forgot_password` : Handles the form submission in the forgot password page.

## Setup and Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>

   ```

2. Install docker for your os
3. Execute docker compose command to get the containers up:
   ```bash
   docker compose up -d
   ```
4. Finally check localhost:8000 in your browser
