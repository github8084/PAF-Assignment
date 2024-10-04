To run the project with Docker, follow these steps:

1. Ensure Docker and Docker Compose are installed on your machine.
2. Clone this repository: git clone https://github.com/github8084/PAF-Assignment
3. Navigate to the project directory: cd <your-repository>
4. Start the application using Docker Compose: docker-compose up --build


Testing the API with `curl` Commands

1. Sign Up a User:

curl -X POST http://127.0.0.1:5000/signup -H "Content-Type: application/json" -d "{\"email\": \"user@gmail.com\", \"password\": \"password123\"}"


2. Sign In (Get Token):

curl -X POST http://127.0.0.1:5000/signin -H "Content-Type: application/json" -d "{\"email\": \"user@gmail.com\", \"password\": \"password123\"}"

This will return an `access_token` and `refresh_token`.

3. Access a Protected Route:

curl -X GET http://127.0.0.1:5000/protected -H "Authorization: Bearer <access_token>"


4. Refresh the Token:

curl -X POST http://127.0.0.1:5000/refresh -H "Authorization: Bearer <refresh_token>"


5. Logout (Revoke Token):

curl -X POST http://127.0.0.1:5000/logout -H "Authorization: Bearer <access_token>"
