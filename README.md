# Hack and Hunt API

Welcome to the Hack and Hunt API! This project is a Django-based web application that provides APIs for managing user accounts and game-related functionalities like leaderboards, levels, and riddles.

## Table of Contents
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Project Structure
```
hackandhunt-api/
├── .gitignore
├── LICENSE
├── manage.py
├── db.sqlite3
├── hackandhunt_api/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
│       └── __init__.py
├── apis/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── permissions.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   ├── models/
│   ├── serializers/
│

```

## Installation
To get started with the Hack and Hunt API, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/ShishirRijal/hackandhunt-api.git
   cd hackandhunt-api
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:

   Create a `.env` file in the root directory and add the following environment variables:

   ```plaintext
   SECRET_KEY=your_secret_key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. Apply migrations:

   ```bash
   python manage.py migrate
   ```

6. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

## Running the Application
To start the application, run:

```bash
python manage.py runserver
```

This will start the server on [http://localhost:8000](http://localhost:8000).

## API Documentation

### User Endpoints
- `POST /api/signup/`: Register a new user
- `POST /api/login/`: Authenticate a user and return a token
- `GET /api/profile/`: Get the profile of the logged-in user

### Level Endpoints
- `POST /api/levels/`: Create level
- `GET /api/levels/`: Get all levels
- `GET /api/levels/{id}/`: Get level
- `PATCH /api/levels/{id}/`: Update level
- `DELETE /api/riddles/{id}/`: Delete level

### Riddle Endpoints
- `POST /api/riddles/`: Create new riddle
- `GET /api/riddles/`: Get all riddles
- `GET /api/riddles/{id}/`: Get riddle
- `GET /api/riddles?level={id}/`: Get riddles of particular level
- `POST /api/riddles/{id}/verify/`: Verify the riddle answer
- `PATCH /api/riddles/{id}/`: Update riddle
- `DELETE /api/riddles/{id}/`: Delete riddle

### Leaderboard Endpoints
- `GET /api/leaderboard/`: Get the leaderboard
- `GET /api/current-level/`: Get current level of logged-in user


### Example Requests

**Register a New User**

```bash
curl -X POST http://localhost:8000/api/signup/ \
    -H "Content-Type: application/json" \
    -d '{"username": "john_doe", "password": "password123", "email": "john@example.com", "name": "John Doe"}
```

**User Login**

```bash
curl -X POST http://localhost:8000/api/login/ \
    -H "Content-Type: application/json" \
    -d '{"email": "john@example.com", "password": "password123"}'
```


## Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature-branch`)
6. Create a new Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

Feel free to modify this README to better suit the specifics and nuances of your project.
