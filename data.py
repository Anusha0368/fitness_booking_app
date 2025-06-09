import datetime
from pytz import timezone

# Assuming classes are created in IST 
IST = timezone('Asia/Kolkata')

# Seed data for fitness classes
# Each class has: name, date/time (in IST), instructor, and available slots. 
classes_data = [
    {
        "id": "c1",
        "name": "Yoga Basics",
        "datetime": IST.localize(datetime.datetime(2025, 6, 9, 10, 0)), # June 9, 10:00 AM IST
        "instructor": "Priya Sharma",
        "total_slots": 15,
        "available_slots": 15
    },
    {
        "id": "c2",
        "name": "Zumba Dance",
        "datetime": IST.localize(datetime.datetime(2025, 6, 9, 17, 30)), # June 9, 5:30 PM IST
        "instructor": "Amit Singh",
        "total_slots": 20,
        "available_slots": 20
    },
    {
        "id": "c3",
        "name": "HIIT Express",
        "datetime": IST.localize(datetime.datetime(2025, 6, 10, 8, 0)), # June 10, 8:00 AM IST
        "instructor": "Vikram Das",
        "total_slots": 10,
        "available_slots": 10
    }
]

# In-memory store for bookings
# Each booking has: class_id, client_name, client_email 
bookings_data = []

def get_all_classes():
    """Returns a list of all upcoming fitness classes."""
    # In a real app, you'd filter for upcoming classes based on current time
    return classes_data

def get_class_by_id(class_id):
    """Returns a single class by its ID."""
    for cls in classes_data:
        if cls['id'] == class_id:
            return cls
    return None

def update_class_slots(class_id, change):
    """Reduces available slots for a class.""" 
    for cls in classes_data:
        if cls['id'] == class_id:
            cls['available_slots'] += change
            return True
    return False

def add_booking(class_id, client_name, client_email):
    """Adds a new booking.""" 
    booking = {
        "booking_id": f"b{len(bookings_data) + 1}", # Simple unique ID
        "class_id": class_id,
        "client_name": client_name,
        "client_email": client_email,
        "booking_time": datetime.datetime.now(IST)
    }
    bookings_data.append(booking)
    return booking

def get_bookings_by_email(email):
    """Returns all bookings made by a specific email address.""" 
    return [booking for booking in bookings_data if booking['client_email'].lower() == email.lower()]

def change_timezone_for_all_classes(new_tz_str):
    """
    Adjusts class times to a new timezone.
    Classes created in IST, on change of timezone all the slots should be changed accordingly. 
    """
    try:
        new_tz = timezone(new_tz_str)
    except Exception:
        return False # Invalid timezone string

    for cls in classes_data:
        # Assuming datetime objects are timezone-aware and localized to IST
        if cls['datetime'].tzinfo is None or cls['datetime'].tzinfo.utcoffset(cls['datetime']) is None:
            # If not localized, localize to IST first (this shouldn't happen with our seed data)
            cls['datetime'] = IST.localize(cls['datetime'].replace(tzinfo=None))

        # Convert to the new timezone
        cls['datetime'] = cls['datetime'].astimezone(new_tz)
    return True