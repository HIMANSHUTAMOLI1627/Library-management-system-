Steps to Run

1. Clone the repository:

git clone <repository-url>
cd library-management-system


2. Install Flask: Since third-party libraries are restricted, ensure you have Flask installed.

pip install flask


3. Run the application:

python app.py


4. Access the API: The API will run locally on http://127.0.0.1:5000.


5. Testing: Use tools like Postman or curl to test the endpoints.

Example for login:

curl -X POST http://127.0.0.1:5000/auth/login \
-H "Content-Type: application/json" \
-d '{"username": "admin", "password": "password"}'

Design Choices

1. Token-Based Authentication

Implemented a simple token-based authentication to ensure secure access to the API.

Tokens are generated using hashlib and are stored in-memory for simplicity.


2. In-Memory Storage

Used Python lists to store books and members for simplicity, adhering to the constraint of not using third-party libraries.

This choice avoids the complexity of integrating a database for this basic implementation.


3. RESTful API Design

Endpoints follow REST principles with resource-based URLs (/books, /members).

HTTP methods (GET, POST, PUT, DELETE) are used for CRUD operations.


4. Pagination and Search

Pagination and search are implemented for the /books endpoint to handle large datasets efficiently.

Query parameters (query, page, per_page) allow dynamic filtering and paginated responses.



---

Assumptions and Limitations

Assumptions

1. Authentication:

Only one user (admin) is hardcoded for simplicity.

Token expiration is not implemented.



2. Data Structure:

Books and members are stored in-memory and reset when the server restarts.



3. Minimal Validation:

Input validation is minimal to keep the implementation straightforward.



4. Search Logic:

Searches are case-insensitive and match substrings in titles or authors.




Limitations

1. No Persistent Storage:

All data is lost upon server restart as there is no database integration.



2. Scalability:

In-memory storage and token management are not suitable for large-scale applications.



3. Security:

The hardcoded username/password and lack of HTTPS make this unsuitable for production.



4. Pagination:

Pagination is basic and does not support advanced features like total page count or next/previous links.
