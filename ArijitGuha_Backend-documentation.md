### API Endpoints
- Register
    - URL: /register
    - Method: POST
    - Description: Registers a new user.
    - Request Body:
        - ```username (string)```: The username of the user.
        - ``` password (string)```: The password of the user.
    - Response:Redirects to the login page on successful registration.
- Login
    - URL: /login
    - Method: POST
    - Description: Authenticates a user and generates an access token.
    - Request Body:
        - ```username (string)```: The username of the user.
        - ```password (string)```: The password of the user.
    - Response:JSON object containing the access token on successful login.
- Home
    - URL: /
    - Method: POST
    - Description: Gets song recommendations based on the provided song details.
    - Request Headers:
    - x-access-token (string): The access token obtained from the login endpoint.
    Request Body:
        - ```name (string)```: The name of the song.
        - ```year (integer)```: The year of the song.
        - ```artists (string)```: The artist(s) of the song.
    - Response:JSON array containing the recommended songs.
- Logout
    - URL: /logout
    - Method: GET
    - Description: Logs out the currently authenticated user.
    - Response:Redirects to the login page.

### Authentication
The API uses JWT (JSON Web Tokens) for authentication. To access protected endpoints, you need to include the access token obtained from the login endpoint in the x-access-token header of the request.

### Error Handling
The API returns appropriate error responses in case of invalid requests or authentication failures.

- ```400 Bad Request```: If the request body is missing or invalid.
- ```401 Unauthorized```: If the access token is missing or invalid.

### Database
The API uses an SQLite database (songs.db) to store user information and song recommendations. The database schema consists of two tables:

- User: Stores user details such as username and password.
- Recommendation: Stores recommended songs for each user.
### Song Recommendation
The API uses the recommend_songs function from the model module to generate song recommendations based on the provided song details. The recommendations are stored in the database and returned as a JSON response.

### CORS Support
The API supports Cross-Origin Resource Sharing (CORS) to allow requests from different domains. The CORS headers are configured using the Flask-CORS extension.

### Deployment
The API can be deployed using any web server that supports Python and Flask. Make sure to set the appropriate environment variables and configurations for production deployment.
