from flask import Flask, jsonify, request
from data import get_all_classes, get_class_by_id, update_class_slots, add_booking, get_bookings_by_email, change_timezone_for_all_classes
from utils import APIError, handle_api_error, validate_json_input, is_valid_email
import logging

app = Flask(__name__)
app.register_error_handler(APIError, handle_api_error)

# Basic logging setup 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def home():
    """A simple home endpoint for testing."""
    return "Welcome to the Fitness Booking API!"

@app.route('/classes', methods=['GET'])
def get_classes():
    """Returns a list of all upcoming fitness classes."""
    logging.info("Fetching all classes.")
    classes = get_all_classes()
    # Format datetime objects for JSON serialization
    formatted_classes = []
    for cls in classes:
        formatted_cls = cls.copy()
        formatted_cls['datetime'] = cls['datetime'].isoformat() # Convert to ISO 8601 string
        formatted_classes.append(formatted_cls)
    return jsonify(formatted_classes)

@app.route('/book', methods=['POST'])
@validate_json_input(['class_id', 'client_name', 'client_email']) # Basic input validation 
def book_class():
    """Accepts a booking request and validates slots.""" 
    data = request.get_json()
    class_id = data['class_id']
    client_name = data['client_name']
    client_email = data['client_email']

    logging.info(f"Attempting to book class {class_id} for {client_email}")

    # Input validation 
    if not is_valid_email(client_email):
        raise APIError("Invalid client_email format.", status_code=400)
    if not client_name.strip():
        raise APIError("Client name cannot be empty.", status_code=400)

    fitness_class = get_class_by_id(class_id)

    if not fitness_class:
        raise APIError(f"Class with ID '{class_id}' not found.", status_code=404)

    if fitness_class['available_slots'] <= 0:
        # Handle overbooking and edge cases 
        raise APIError(f"No slots available for '{fitness_class['name']}'.", status_code=400)

    # Reduce available slots upon successful booking 
    update_class_slots(class_id, -1)
    booking = add_booking(class_id, client_name, client_email)

    logging.info(f"Successfully booked class {class_id} for {client_email}. Booking ID: {booking['booking_id']}")
    return jsonify({
        "message": "Booking successful!",
        "booking_id": booking['booking_id'],
        "class_name": fitness_class['name'],
        "client_name": booking['client_name'],
        "client_email": booking['client_email'],
        "remaining_slots": fitness_class['available_slots']
    }), 201

@app.route('/bookings', methods=['GET'])
def get_client_bookings():
    """Returns all bookings made by a specific email address."""
    client_email = request.args.get('email')

    if not client_email:
        raise APIError("Missing 'email' query parameter.", status_code=400)

    if not is_valid_email(client_email):
        raise APIError("Invalid email format for query parameter.", status_code=400)

    logging.info(f"Fetching bookings for email: {client_email}")
    bookings = get_bookings_by_email(client_email)

    if not bookings:
        return jsonify({"message": f"No bookings found for {client_email}."}), 404

    # Format datetime objects for JSON serialization
    formatted_bookings = []
    for booking in bookings:
        formatted_booking = booking.copy()
        formatted_booking['booking_time'] = booking['booking_time'].isoformat()
        formatted_bookings.append(formatted_booking)

    return jsonify(formatted_bookings)

@app.route('/admin/change_timezone', methods=['POST'])
@validate_json_input(['new_timezone'])
def change_timezone():
    """
    Endpoint to change the timezone for all classes.
    Classes created in IST, on change of timezone all the slots should be changed accordingly. 
    """
    data = request.get_json()
    new_tz_str = data['new_timezone']

    logging.info(f"Attempting to change timezone to: {new_tz_str}")

    if change_timezone_for_all_classes(new_tz_str):
        logging.info("Timezone changed successfully for all classes.")
        return jsonify({"message": f"Timezone successfully changed to {new_tz_str} for all classes."}), 200
    else:
        raise APIError(f"Invalid timezone string provided: {new_tz_str}", status_code=400)


if __name__ == '__main__':
    # For development: allows Flask to pick up changes without manual restart
    # Also provides a cleaner way to run from the command line
    app.run(debug=True, port=5000)