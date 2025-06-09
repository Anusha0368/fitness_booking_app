Fitness Studio Booking API
This project implements a simple booking API for a fictional fitness studio using Python and the Flask framework. It allows clients to view available classes, book spots, and retrieve their bookings. The API uses an in-memory SQLite database for data storage and handles timezone conversions.

Table of Contents
Features

Technical Stack

Setup Instructions

API Endpoints

GET /classes

POST /book

GET /bookings

Error Handling

Timezone Management

Logging

Running Tests

Features
View Classes: Retrieve a list of all upcoming fitness classes with details like name, date/time, instructor, and available slots.

Book Class: Book a spot in a specific class, with validation for slot availability and automatic reduction of available slots.

View Bookings: Get a list of all bookings made by a particular client email address.

Timezone Aware: Classes are stored internally in UTC and can be displayed in various timezones based on client requests.

Technical Stack
Backend Framework: Flask

Database: SQLite (in-memory)

Date/Time Handling: datetime module, pytz library

Logging: Python's built-in logging module

Testing: pytest (for unit tests)

Setup Instructions
Clone the repository (or save the app.py and requirements.txt files):
Since this is a single-file application, you can simply save the app.py content into a file named app.py and the requirements.txt content into a file named requirements.txt in the same directory.

Create a Virtual Environment (Recommended):

python3 -m venv venv

Activate the Virtual Environment:

On macOS/Linux:

source venv/bin/activate

On Windows (Command Prompt):

venv\Scripts\activate.bat

On Windows (PowerShell):

venv\Scripts\Activate.ps1

Install Dependencies:

pip install -r requirements.txt

Run the Flask Application:

python app.py

The API will start running on http://127.0.0.1:5000/.

API Endpoints
You can use curl or Postman/Insomnia to interact with the API.

GET /classes
Returns a list of all upcoming fitness classes, including their names, date/time, instructor, and available slots.

URL: /classes

Method: GET

Query Parameters:

timezone (optional): A valid IANA timezone string (e.g., America/New_York, Europe/London, Asia/Kolkata). If not provided, times will be displayed in Asia/Kolkata (IST).

Example Request (default timezone):

curl http://127.0.0.1:5000/classes

Example Request (specific timezone):

curl "http://127.0.0.1:5000/classes?timezone=America/New_York"

Example Response (truncated):

[
  {
    "available_slots": 15,
    "date_time": "2025-06-10 07:00 IST+0530",
    "id": 1,
    "instructor": "Priya Sharma",
    "name": "Yoga Basics",
    "total_slots": 15
  },
  {
    "available_slots": 20,
    "date_time": "2025-06-10 18:30 IST+0530",
    "id": 2,
    "instructor": "Rahul Singh",
    "name": "Zumba Dance",
    "total_slots": 20
  }
  // ... more classes
]

POST /book
Accepts a booking request for a class. It validates if slots are available and reduces the available slots upon successful booking.

URL: /book

Method: POST

Headers: Content-Type: application/json

Request Body:

{
  "class_id": 1,
  "client_name": "John Doe",
  "client_email": "john.doe@example.com"
}

Example Request:

curl -X POST -H "Content-Type: application/json" -d '{
  "class_id": 1,
  "client_name": "John Doe",
  "client_email": "john.doe@example.com"
}' http://127.0.0.1:5000/book

Example Success Response (Status 201 Created):

{
  "message": "Booking successful!",
  "class_name": "Yoga Basics"
}

Example Error Responses:

400 Bad Request (Missing fields):

{"error": "Missing required fields: class_id, client_name, client_email"}

404 Not Found (Class not found):

{"error": "Class not found"}

409 Conflict (No available slots):

{"error": "No available slots for this class"}

GET /bookings
Returns all bookings made by a specific email address.

URL: /bookings

Method: GET

Query Parameters:

email (mandatory): The email address of the client.

timezone (optional): A valid IANA timezone string. If not provided, times will be displayed in Asia/Kolkata (IST).

Example Request:

curl "http://127.0.0.1:5000/bookings?email=john.doe@example.com"

Example Request (specific timezone):

curl "http://127.0.0.1:5000/bookings?email=john.doe@example.com&timezone=Europe/London"

Example Response (truncated):

[
  {
    "booking_id": 1,
    "booking_time": "2025-06-07 23:30:00 IST+0530",
    "class_date_time": "2025-06-10 07:00 IST+0530",
    "class_name": "Yoga Basics",
    "client_email": "john.doe@example.com",
    "client_name": "John Doe",
    "instructor": "Priya Sharma"
  }
]

Error Handling
The API provides meaningful HTTP status codes and JSON error messages for various scenarios, including:

400 Bad Request: Missing or invalid input fields.

404 Not Found: Resource (e.g., class) not found.

409 Conflict: Business logic conflicts, such as no available slots for a class.

500 Internal Server Error: Unexpected server-side issues or database errors.

Timezone Management
All class datetime and booking booking_time values are stored in the database as UTC ISO 8601 strings.

When a class is initially seeded or created, its IST time is converted to UTC before storage.

When retrieving classes or bookings, the API can convert these UTC times to a user-specified timezone (via the timezone query parameter) or default to Asia/Kolkata (IST) for display.

Logging
Basic logging is implemented using Python's logging module to track API requests, database operations, and errors. Log messages are printed to the console.

Running Tests
To run the unit tests, you'll need pytest installed (pip install pytest).

Navigate to the project root directory.

Run pytest:

pytest

(Note: You might need to create a tests/ directory and a test_api.py file within it for pytest to discover tests. See test_api.py below.)
