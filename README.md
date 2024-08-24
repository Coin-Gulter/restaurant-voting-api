
---

# Restaurant Voting API

## Project Description

The Restaurant Voting API is a Django-based application designed for employees of a company to vote on restaurant menus for lunch. The app includes features for user registration, authentication, restaurant and menu management, and voting. It uses Django REST Framework and JWT for authentication.
Also could be deployed by Docker (docker-compose) or using CMD.

## Features

- **User Registration and Authentication:** Users can register, obtain JWT tokens, and authenticate API requests.
- **Restaurant Management:** Owners can create and manage their restaurants.
- **Menu Management:** Owners can upload menus for their restaurants and make them public or private.
- **Voting:** Users can vote for their preferred menu of the day. Results can be aggregated and viewed.

## Installation (without docker)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Coin-Gulter/restaurant-voting-api.git
   cd restaurant-voting-api
   ```

2. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Write your DB parameters into ".env" file:**
    Parameters:
        - IMAGE_NAME = coingualter/inforce_lunch:1.0
        - PORT = 5000
    needed only when you work with docker (docker-compose)

4. **Set up the database:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## Installation (with docker)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Coin-Gulter/restaurant-voting-api.git
   cd restaurant-voting-api
   ```

2. **Write your server parameters into ".env" file:**
    Where parameter "PORT" means port to connect to the api server.
    Better not to uses DB parameters because they used to connect to the docker postgresql DB.

5. **Run the development docker compose server:**
   ```bash
   docker compose -f docker-compose.yaml up -d
   ```

## Endpoints

### Authentication

1. **Register User**
   - **URL:** `/authentication/register/`
   - **Method:** `POST`
   - **Description:** Register a new user.
   - **Request Body:**
     ```json
     {
       "username": "newuser",
       "password": "password",
       "email": "newuser@example.com",
       "name": "New User"
     }
     ```

2. **Obtain JWT Token**
   - **URL:** `/authentication/token/`
   - **Method:** `POST`
   - **Description:** Obtain JWT access and refresh tokens.
   - **Request Body:**
     ```json
     {
       "username": "username",
       "password": "password"
     }
     ```

3. **Refresh JWT Token**
   - **URL:** `/authentication/token/refresh/`
   - **Method:** `POST`
   - **Description:** Refresh the JWT access token using the refresh token.
   - **Request Body:**
     ```json
     {
       "refresh": "refresh_token"
     }
     ```

4. **Get User Details**
   - **URL:** `/authentication/getuser/`
   - **Method:** `GET`
   - **Description:** Retrieve authenticated user's details.
   - **Headers:**
     ```
     Authorization: Bearer <access_token>
     ```

### Restaurant Management

1. **Create Restaurant**
   - **URL:** `/restaurants/create/`
   - **Method:** `POST`
   - **Description:** Create a new restaurant.
   - **Request Body:**
     ```json
     {
       "name": "Restaurant Name",
       "address": "123 Street",
       "phone": "1234567890",
       "description": "A nice place",
       "is_public": true
     }
     ```

### Menu Management

1. **Upload Menu**
   - **URL:** `/restaurants/menus/`
   - **Method:** `POST`
   - **Description:** Upload a new menu for a restaurant.
   - **Request Body:**
     ```json
     {
       "restaurant": 1,
       "date": "2024-08-24",
       "items": {
         "items": ["Pizza", "Pasta", "Salad"]
       }
     }
     ```

2. **Get Today's Menu**
   - **URL:** `/restaurants/menus/today/`
   - **Method:** `GET`
   - **Description:** Retrieve the current day's menu for the user's restaurants or public restaurants.
   - **Headers:**
     ```
     Authorization: Bearer <access_token>
     ```

### Voting

1. **Submit a Vote**
   - **URL:** `/voting/vote/`
   - **Method:** `POST`
   - **Description:** Submit a vote for a menu.
   - **Request Body:**
     ```json
     {
       "menu_id": 1
     }
     ```
   - **Headers:**
     ```
     Authorization: Bearer <access_token>
     ```

2. **Get Today's Voting Results**
   - **URL:** `/voting/results/today/`
   - **Method:** `GET`
   - **Description:** Retrieve today's voting results, aggregated by restaurant.
   - **Headers:**
     ```
     Authorization: Bearer <access_token>
     ```

## Running Tests

To run tests using PyTest, use the following command in the main project directory:

```bash
pytest
```

This will execute all tests in the project, ensuring the functionality of your application.

## License

This project is licensed under the MIT License.

---