"""
TravelMate AI - Smart Travel Management System
A comprehensive travel booking web application with Flask
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from datetime import datetime
import random
import string
import os
from werkzeug.utils import secure_filename
from functools import wraps

# Import configurations
try:
    from firebase_config import FirebaseDB, FIREBASE_ENABLED
except ImportError:
    FIREBASE_ENABLED = False
    FirebaseDB = None

try:
    from cloudinary_config import CloudinaryManager, CLOUDINARY_ENABLED
except ImportError:
    CLOUDINARY_ENABLED = False
    CloudinaryManager = None

try:
    from onesignal_config import OneSignalManager, ONESIGNAL_ENABLED
except ImportError:
    ONESIGNAL_ENABLED = False
    OneSignalManager = None

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Upload configuration
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def login_required(f):
    """Decorator to require login for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please login to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin login for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin'):
            flash('Admin access required.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== ID GENERATORS ====================
def generate_user_id():
    return "USR" + ''.join(random.choices(string.digits, k=4))

def generate_package_id():
    return "PKG" + ''.join(random.choices(string.digits, k=4))

def generate_booking_id():
    return "BK" + ''.join(random.choices(string.digits, k=5))

def generate_review_id():
    return "REV" + ''.join(random.choices(string.digits, k=4))

def generate_destination_id():
    return "DEST" + ''.join(random.choices(string.digits, k=3))

def generate_notification_id():
    return str(random.randint(1, 10000))

def generate_category_id():
    """Generate category ID"""
    return "CAT" + ''.join(random.choices(string.digits, k=3))

# ==================== DATA HELPERS ====================
def get_users():
    """Get users from Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        result = FirebaseDB.get_all_users()
        return result if result else {}
    return users

def get_user(user_id):
    """Get user by ID from Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        return FirebaseDB.get_user(user_id)
    return users.get(user_id)

def get_user_by_email(email):
    """Get user by email from Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        return FirebaseDB.get_user_by_email(email)
    for user in users.values():
        if user.get('email') == email:
            return user
    return None

def save_user(user_data):
    """Save user to Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        FirebaseDB.create_user(user_data)
    users[user_data['id']] = user_data

def update_user_data(user_id, data):
    """Update user in Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        FirebaseDB.update_user(user_id, data)
    if user_id in users:
        users[user_id].update(data)

def get_destinations_data():
    """Get destinations from Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        try:
            result = FirebaseDB.get_destinations()
            return result if result else {}
        except Exception as e:
            # Firebase error, fall back to mock data
            import logging
            logging.error(f'Firebase get_destinations failed: {e}')
            return destinations
    return destinations

def get_destination_data(dest_id):
    """Get destination by ID from Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        return FirebaseDB.get_destination(dest_id)
    return destinations.get(dest_id)

def save_destination(dest_data):
    """Save destination to Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        FirebaseDB.create_destination(dest_data)
    destinations[dest_data['id']] = dest_data

def update_destination_data(dest_id, data):
    """Update destination in Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        FirebaseDB.update_destination(dest_id, data)
    if dest_id in destinations:
        destinations[dest_id].update(data)

def delete_destination_data(dest_id):
    """Delete destination from Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        FirebaseDB.delete_destination(dest_id)
    if dest_id in destinations:
        del destinations[dest_id]

def get_packages_data():
    """Get packages from Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        try:
            result = FirebaseDB.get_packages()
            return result if result else {}
        except Exception as e:
            # Firebase error, fall back to mock data
            import logging
            logging.error(f'Firebase get_packages failed: {e}')
            return packages
    return packages

def get_package_data(pkg_id):
    """Get package by ID from Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        return FirebaseDB.get_package(pkg_id)
    return packages.get(pkg_id)

def save_package(pkg_data):
    """Save package to Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        FirebaseDB.create_package(pkg_data)
    packages[pkg_data['id']] = pkg_data

def update_package_data(pkg_id, data):
    """Update package in Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        FirebaseDB.update_package(pkg_id, data)
    if pkg_id in packages:
        packages[pkg_id].update(data)

def delete_package_data(pkg_id):
    """Delete package from Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        FirebaseDB.delete_package(pkg_id)
    if pkg_id in packages:
        del packages[pkg_id]

def get_bookings_data():
    """Get bookings from Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        result = FirebaseDB.get_bookings()
        return result if result else {}
    return bookings

def get_booking_data(booking_id):
    """Get booking by ID from Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        return FirebaseDB.get_booking(booking_id)
    return bookings.get(booking_id)

def save_booking(booking_data):
    """Save booking to Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        FirebaseDB.create_booking(booking_data)
    bookings[booking_data['id']] = booking_data

def update_booking_data(booking_id, data):
    """Update booking in Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        FirebaseDB.update_booking(booking_id, data)
    if booking_id in bookings:
        bookings[booking_id].update(data)

def get_bookings_by_user_email(email):
    """Get bookings by user email"""
    if FIREBASE_ENABLED and FirebaseDB:
        result = FirebaseDB.get_bookings_by_email(email)
        return result if result else {}
    return {k: v for k, v in bookings.items() if v.get('email') == email}

def get_reviews_data():
    """Get reviews from Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        try:
            result = FirebaseDB.get_reviews()
            return result if result else {}
        except Exception as e:
            # Firebase error, fall back to mock data
            import logging
            logging.error(f'Firebase get_reviews failed: {e}')
            return reviews
    return reviews

def get_review_data(review_id):
    """Get review by ID from Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        return FirebaseDB.get_review(review_id)
    return reviews.get(review_id)

def save_review(review_data):
    """Save review to Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        FirebaseDB.create_review(review_data)
    reviews[review_data['id']] = review_data

def approve_review_data(review_id):
    """Approve review in Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        FirebaseDB.approve_review(review_id)
    if review_id in reviews:
        reviews[review_id]['approved'] = True

def get_notifications_data():
    """Get notifications from Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        try:
            result = FirebaseDB.get_notifications()
            return list(result.values()) if result else []
        except Exception as e:
            # Firebase error, fall back to mock data
            import logging
            logging.error(f'Firebase get_notifications failed: {e}')
            return notifications
    return notifications

def save_notification(notification_data):
    """Save notification to Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        FirebaseDB.create_notification(notification_data)
    notifications.append(notification_data)


# ==================== CATEGORY HELPERS ====================
def get_categories_data():
    """Get categories from Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        try:
            result = FirebaseDB.get_categories()
            return result if result else {}
        except AttributeError:
            # Firebase doesn't have categories implemented yet, use mock data
            pass
    return categories


def get_category_data(cat_id):
    """Get category by ID from Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        try:
            return FirebaseDB.get_category(cat_id)
        except AttributeError:
            # Firebase doesn't have categories implemented yet, use mock data
            pass
    return categories.get(cat_id)


def save_category(cat_data):
    """Save category to Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        try:
            FirebaseDB.create_category(cat_data)
        except AttributeError:
            # Firebase doesn't have categories implemented yet, use mock data
            pass
    categories[cat_data['id']] = cat_data


def update_category_data(cat_id, data):
    """Update category in Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        try:
            FirebaseDB.update_category(cat_id, data)
        except AttributeError:
            # Firebase doesn't have categories implemented yet, use mock data
            pass
    if cat_id in categories:
        categories[cat_id].update(data)


def delete_category_data(cat_id):
    """Delete category from Firebase or mock database"""
    if FIREBASE_ENABLED and FirebaseDB:
        try:
            FirebaseDB.delete_category(cat_id)
        except AttributeError:
            # Firebase doesn't have categories implemented yet, use mock data
            pass
    if cat_id in categories:
        del categories[cat_id]


# ==================== MOCK DATABASE (Replace with Firebase) ====================
# In production, replace these with Firebase Realtime Database calls
users = {}
destinations = {
    "DEST001": {
        "id": "DEST001",
        "name": "Goa",
        "description": "Beautiful beaches, vibrant nightlife, and Portuguese heritage",
        "full_description": "Goa is India's smallest state by area and the fourth smallest by population. Located on the west coast of India in the region known as the Konkan, it is bounded by the state of Maharashtra to the north, and by Karnataka to the east and south, while the Arabian Sea forms its western coast.",
        "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800",
        "gallery": [
            "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800",
            "https://images.unsplash.com/photo-1519046904884-53103b34b206?w=800",
            "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800",
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800"
        ],
        "category": "Beaches",
        "rating": 4.5,
        "reviews_count": 128,
        "location": "Goa, India",
        "best_time": "October to March",
        "attractions": "Baga Beach, Calangute Beach, Dudhsagar Falls, Fort Aguada, Basilica of Bom Jesus",
        "views": 0
    },
    "DEST002": {
        "id": "DEST002",
        "name": "Manali",
        "description": "Snow-capped mountains, adventure sports, and scenic valleys",
        "full_description": "Manali is a resort town nestled in the mountains of the Indian state of Himachal Pradesh near the northern end of the Kullu Valley. It is located in the Kullu district, about 270 km north of the state capital, Shimla.",
        "image": "https://images.unsplash.com/photo-1626010448982-4d629b1a0151?w=800",
        "gallery": [
            "https://images.unsplash.com/photo-1626010448982-4d629b1a0151?w=800",
            "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800",
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
            "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=800"
        ],
        "category": "Mountains",
        "rating": 4.7,
        "reviews_count": 95,
        "location": "Himachal Pradesh, India",
        "best_time": "October to June",
        "attractions": "Solang Valley, Rohtang Pass, Hidimba Devi Temple, Manu Temple, Vashisht Hot Springs",
        "views": 0
    },
    "DEST003": {
        "id": "DEST003",
        "name": "Kerala",
        "description": "Backwaters, houseboats, and lush green landscapes",
        "full_description": "Kerala, a state on India's tropical Malabar Coast, has nearly 600km of Arabian Sea shoreline. It's known for its palm-lined beaches and backwaters, a network of canals. Inland are the Western Ghats, mountains whose slopes support tea, coffee and spice plantations as well as wildlife.",
        "image": "https://images.unsplash.com/photo-1609766857041-ed402ea8069a?w=800",
        "gallery": [
            "https://images.unsplash.com/photo-1609766857041-ed402ea8069a?w=800",
            "https://images.unsplash.com/photo-1595658658481-d53d3f999875?w=800",
            "https://images.unsplash.com/photo-1582510003544-4d00b7e74208?w=800",
            "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=800"
        ],
        "category": "Backwaters",
        "rating": 4.6,
        "reviews_count": 87,
        "location": "Kerala, India",
        "best_time": "September to March",
        "attractions": "Alleppey Backwaters, Munnar Tea Gardens, Kochi Fort, Kovalam Beach, Periyar Wildlife Sanctuary",
        "views": 0
    },
    "DEST004": {
        "id": "DEST004",
        "name": "Jaipur",
        "description": "Royal palaces, forts, and rich Rajasthani culture",
        "full_description": "Jaipur is the capital and the largest city of the Indian state of Rajasthan. As of 2011, the city had a population of 3.1 million, making it the tenth most populous city in the country. Jaipur is also known as the Pink City, due to the dominant color scheme of its buildings.",
        "image": "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=800",
        "gallery": [
            "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=800",
            "https://images.unsplash.com/photo-1567157577867-05ccb1388e66?w=800",
            "https://images.unsplash.com/photo-1595658658481-d53d3f999875?w=800",
            "https://images.unsplash.com/photo-1589820296156-2454bb8a6d54?w=800"
        ],
        "category": "Heritage",
        "rating": 4.4,
        "reviews_count": 76,
        "location": "Rajasthan, India",
        "best_time": "October to March",
        "attractions": "Hawa Mahal, Amber Fort, City Palace, Jantar Mantar, Jal Mahal",
        "views": 0
    },
    "DEST005": {
        "id": "DEST005",
        "name": "Kashmir",
        "description": "Paradise on Earth with stunning valleys and lakes",
        "full_description": "Kashmir is the northernmost geographical region of the Indian subcontinent. Until the mid-19th century, the term Kashmir geographically denoted only the Kashmir Valley between the Great Himalayas and the Pir Panjal Range.",
        "image": "https://images.unsplash.com/photo-1566837497312-7be7830a7a7a?w=800",
        "gallery": [
            "https://images.unsplash.com/photo-1566837497312-7be7830a7a7a?w=800",
            "https://images.unsplash.com/photo-1589820296156-2454bb8a6d54?w=800",
            "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=800",
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800"
        ],
        "category": "Mountains",
        "rating": 4.8,
        "reviews_count": 64,
        "location": "Jammu & Kashmir, India",
        "best_time": "April to October",
        "attractions": "Dal Lake, Gulmarg, Pahalgam, Sonamarg, Shankaracharya Temple",
        "views": 0
    },
    "DEST006": {
        "id": "DEST006",
        "name": "Andaman",
        "description": "Pristine beaches, coral reefs, and water sports",
        "full_description": "The Andaman and Nicobar Islands, a Union territory of India comprising 572 islands of which 37 are inhabited, are a group of islands at the juncture of the Bay of Bengal and the Andaman Sea.",
        "image": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800",
        "gallery": [
            "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800",
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
            "https://images.unsplash.com/photo-1519046904884-53103b34b206?w=800",
            "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800"
        ],
        "category": "Beaches",
        "rating": 4.6,
        "reviews_count": 52,
        "location": "Port Blair, Andaman & Nicobar Islands, India",
        "best_time": "October to May",
        "attractions": "Radhanagar Beach, Cellular Jail, Ross Island, Havelock Island, Neil Island",
        "views": 0
    }
}

packages = {
    "PKG1001": {
        "id": "PKG1001",
        "destination_id": "DEST001",
        "name": "Goa Beach Paradise",
        "duration": "3 Days / 2 Nights",
        "price": 5000,
        "original_price": 6500,
        "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800",
        "highlights": ["Beach hopping", "Water sports", "Nightlife", "Seafood dinner"],
        "inclusions": ["Hotel stay", "Breakfast", "Airport transfer", "Sightseeing"],
        "rating": 4.5,
        "reviews_count": 45
    },
    "PKG1002": {
        "id": "PKG1002",
        "destination_id": "DEST002",
        "name": "Manali Adventure",
        "duration": "5 Days / 4 Nights",
        "price": 9000,
        "original_price": 12000,
        "image": "https://images.unsplash.com/photo-1626010448982-4d629b1a0151?w=800",
        "highlights": ["Solang Valley", "Rohtang Pass", "Paragliding", "River rafting"],
        "inclusions": ["Resort stay", "All meals", "Adventure activities", "Guide"],
        "rating": 4.7,
        "reviews_count": 38
    },
    "PKG1003": {
        "id": "PKG1003",
        "destination_id": "DEST003",
        "name": "Kerala Backwaters",
        "duration": "4 Days / 3 Nights",
        "price": 8500,
        "original_price": 11000,
        "image": "https://images.unsplash.com/photo-1609766857041-ed402ea8069a?w=800",
        "highlights": ["Houseboat stay", "Alleppey backwaters", "Kathakali show", "Ayurvedic spa"],
        "inclusions": ["Houseboat", "All meals", "Spa session", "Cultural show"],
        "rating": 4.6,
        "reviews_count": 42
    },
    "PKG1004": {
        "id": "PKG1004",
        "destination_id": "DEST004",
        "name": "Jaipur Royal Heritage",
        "duration": "3 Days / 2 Nights",
        "price": 6000,
        "original_price": 8000,
        "image": "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=800",
        "highlights": ["Amber Fort", "City Palace", "Hawa Mahal", "Elephant ride"],
        "inclusions": ["Heritage hotel", "Breakfast", "Guide", "Monument entry"],
        "rating": 4.4,
        "reviews_count": 35
    },
    "PKG1005": {
        "id": "PKG1005",
        "destination_id": "DEST005",
        "name": "Kashmir Paradise",
        "duration": "6 Days / 5 Nights",
        "price": 15000,
        "original_price": 20000,
        "image": "https://images.unsplash.com/photo-1566837497312-7be7830a7a7a?w=800",
        "highlights": ["Dal Lake shikara", "Gulmarg", "Pahalgam", "Mughal Gardens"],
        "inclusions": ["Houseboat stay", "All meals", "Skiing", "Sightseeing"],
        "rating": 4.8,
        "reviews_count": 28
    },
    "PKG1006": {
        "id": "PKG1006",
        "destination_id": "DEST006",
        "name": "Andaman Island Escape",
        "duration": "5 Days / 4 Nights",
        "price": 18000,
        "original_price": 25000,
        "image": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800",
        "highlights": ["Radhanagar Beach", "Cellular Jail", "Scuba diving", "Island hopping"],
        "inclusions": ["Beach resort", "Breakfast", "Ferry tickets", "Water sports"],
        "rating": 4.6,
        "reviews_count": 31
    }
}

bookings = {}
reviews = {
    "REV1001": {
        "id": "REV1001",
        "user_name": "Rahul Sharma",
        "package_id": "PKG1001",
        "rating": 5,
        "comment": "Amazing trip to Goa! The beaches were pristine and the nightlife was fantastic. Highly recommended!",
        "date": "2024-03-01",
        "approved": True
    },
    "REV1002": {
        "id": "REV1002",
        "user_name": "Priya Patel",
        "package_id": "PKG1002",
        "rating": 4,
        "comment": "Manali was beautiful! Loved the snow activities. The hotel could have been better though.",
        "date": "2024-02-28",
        "approved": True
    },
    "REV1003": {
        "id": "REV1003",
        "user_name": "Amit Kumar",
        "package_id": "PKG1003",
        "rating": 5,
        "comment": "Kerala backwaters was a dream come true. The houseboat experience was unforgettable!",
        "date": "2024-02-25",
        "approved": True
    }
}

notifications = [
    {"id": 1, "title": "20% Discount on Goa Packages!", "message": "Book before Sunday to avail this offer.", "type": "promo"},
    {"id": 2, "title": "New Destination Added", "message": "Explore the beautiful Andaman Islands now!", "type": "info"},
    {"id": 3, "title": "Summer Special", "message": "Get up to 30% off on all mountain destinations.", "type": "promo"}
]

categories = {
    "CAT001": {
        "id": "CAT001",
        "name": "Beaches",
        "description": "Pristine beaches and coastal destinations",
        "icon": "fas fa-umbrella-beach",
        "color": "#4361ee",
        "active": True,
        "destination_count": 2
    },
    "CAT002": {
        "id": "CAT002",
        "name": "Mountains",
        "description": "Majestic mountain ranges and hill stations",
        "icon": "fas fa-mountain",
        "color": "#7209b7",
        "active": True,
        "destination_count": 2
    },
    "CAT003": {
        "id": "CAT003",
        "name": "Backwaters",
        "description": "Serene backwaters and houseboat experiences",
        "icon": "fas fa-water",
        "color": "#3a0ca3",
        "active": True,
        "destination_count": 1
    },
    "CAT004": {
        "id": "CAT004",
        "name": "Heritage",
        "description": "Royal palaces, forts, and rich cultural heritage",
        "icon": "fas fa-landmark",
        "color": "#f72585",
        "active": True,
        "destination_count": 1
    }
}

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page with hero, search, popular packages, and reviews"""
    all_packages = get_packages_data()
    all_reviews = get_reviews_data()
    all_destinations = get_destinations_data()
    all_notifications = get_notifications_data()

    featured_packages = list(all_packages.values())[:4]
    approved_reviews = [r for r in all_reviews.values() if r.get('approved', True)]
    popular_destinations = sorted(all_destinations.values(), key=lambda x: x['reviews_count'], reverse=True)[:3]
    return render_template('index.html',
                         packages=featured_packages,
                         reviews=approved_reviews,
                         destinations=popular_destinations,
                         notifications=all_notifications)

@app.route('/search')
def search():
    """Search destinations and packages"""
    query = request.args.get('q', '').lower()
    results = []

    all_destinations = get_destinations_data()
    all_packages = get_packages_data()

    if query:
        # Search in destinations
        for dest in all_destinations.values():
            if query in dest['name'].lower() or query in dest['description'].lower():
                results.append({'type': 'destination', 'data': dest})

        # Search in packages
        for pkg in all_packages.values():
            if query in pkg['name'].lower():
                results.append({'type': 'package', 'data': pkg})

    return render_template('search.html', query=query, results=results)

@app.route('/destinations')
def destinations_page():
    """All destinations page"""
    category = request.args.get('category', 'all')
    all_destinations = get_destinations_data()
    all_categories = get_categories_data()

    if category == 'all':
        dest_list = list(all_destinations.values())
    else:
        dest_list = [d for d in all_destinations.values() if d['category'].lower() == category.lower()]

    # Get active categories for filter dropdown (pass the full dict with ID keys)
    active_categories = {k: v for k, v in all_categories.items() if v.get('active', True)}
    
    return render_template('destinations.html', destinations=dest_list, categories=active_categories, current_category=category)

@app.route('/destination/<dest_id>')
def destination_detail(dest_id):
    """Individual destination page"""
    destination = get_destination_data(dest_id)
    if not destination:
        flash('Destination not found!', 'error')
        return redirect(url_for('destinations_page'))

    # Get packages for this destination
    all_packages = get_packages_data()
    dest_packages = [p for p in all_packages.values() if p['destination_id'] == dest_id]

    # Get reviews for packages in this destination
    all_reviews = get_reviews_data()
    dest_reviews = []
    for pkg in dest_packages:
        pkg_reviews = [r for r in all_reviews.values() if r['package_id'] == pkg['id'] and r.get('approved', True)]
        dest_reviews.extend(pkg_reviews)

    # Sort reviews by date (newest first)
    dest_reviews = sorted(dest_reviews, key=lambda x: x.get('date', ''), reverse=True)[:10]

    # Increment view count
    current_views = destination.get('views', 0)
    update_destination_data(dest_id, {'views': current_views + 1})

    return render_template('destination_detail.html', destination=destination, packages=dest_packages, reviews=dest_reviews)


@app.route('/explore/<dest_id>')
def explore(dest_id):
    """Full destination explore page with rich details"""
    destination = get_destination_data(dest_id)
    if not destination:
        flash('Destination not found!', 'error')
        return redirect(url_for('destinations_page'))

    # Get packages for this destination
    all_packages = get_packages_data()
    dest_packages = [p for p in all_packages.values() if p['destination_id'] == dest_id]

    # Get reviews for packages in this destination
    all_reviews = get_reviews_data()
    dest_reviews = []
    for pkg in dest_packages:
        pkg_reviews = [r for r in all_reviews.values() if r['package_id'] == pkg['id'] and r.get('approved', True)]
        dest_reviews.extend(pkg_reviews)

    # Sort reviews by date (newest first)
    dest_reviews = sorted(dest_reviews, key=lambda x: x.get('date', ''), reverse=True)

    # Get similar destinations (same category, excluding current)
    all_destinations = get_destinations_data()
    similar_destinations = [
        d for d in all_destinations.values()
        if d['category'] == destination['category'] and d['id'] != dest_id
    ]

    # Increment view count
    current_views = destination.get('views', 0)
    update_destination_data(dest_id, {'views': current_views + 1})

    return render_template('explore.html',
                         destination=destination,
                         packages=dest_packages,
                         reviews=dest_reviews,
                         similar_destinations=similar_destinations)

@app.route('/packages')
def packages_page():
    """All packages page"""
    dest_filter = request.args.get('destination', 'all')
    price_range = request.args.get('price', 'all')

    all_packages = get_packages_data()
    all_destinations = get_destinations_data()

    pkg_list = list(all_packages.values())

    if dest_filter != 'all':
        pkg_list = [p for p in pkg_list if p['destination_id'] == dest_filter]

    if price_range == 'under5k':
        pkg_list = [p for p in pkg_list if p['price'] < 5000]
    elif price_range == '5k-10k':
        pkg_list = [p for p in pkg_list if 5000 <= p['price'] <= 10000]
    elif price_range == 'above10k':
        pkg_list = [p for p in pkg_list if p['price'] > 10000]

    return render_template('packages.html', packages=pkg_list, destinations=all_destinations)

@app.route('/package/<pkg_id>')
def package_detail(pkg_id):
    """Individual package page"""
    package = get_package_data(pkg_id)
    if not package:
        flash('Package not found!', 'error')
        return redirect(url_for('packages_page'))

    # Get reviews for this package
    all_reviews = get_reviews_data()
    pkg_reviews = [r for r in all_reviews.values() if r['package_id'] == pkg_id and r.get('approved', True)]
    destination = get_destination_data(package['destination_id'])

    return render_template('package_detail.html', package=package, reviews=pkg_reviews, destination=destination)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')

        # Check if email already exists
        existing_user = get_user_by_email(email)
        if existing_user:
            flash('Email already registered!', 'error')
            return redirect(url_for('register'))

        user_id = generate_user_id()
        user_data = {
            'id': user_id,
            'name': name,
            'email': email,
            'phone': phone,
            'password': password,  # In production, hash this!
            'created_at': datetime.now().strftime('%Y-%m-%d'),
            'favorites': []
        }
        save_user(user_data)

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check credentials
        user = get_user_by_email(email)
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(url_for('index'))

        flash('Invalid email or password!', 'error')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/booking/<pkg_id>', methods=['GET', 'POST'])
def booking(pkg_id):
    """Booking page"""
    package = get_package_data(pkg_id)
    if not package:
        flash('Package not found!', 'error')
        return redirect(url_for('packages_page'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        travel_date = request.form.get('travel_date')
        num_people = int(request.form.get('num_people', 1))
        special_requests = request.form.get('special_requests', '')

        booking_id = generate_booking_id()
        total_price = package['price'] * num_people

        booking_data = {
            'id': booking_id,
            'package_id': pkg_id,
            'name': name,
            'email': email,
            'phone': phone,
            'travel_date': travel_date,
            'num_people': num_people,
            'total_price': total_price,
            'special_requests': special_requests,
            'status': 'Pending',
            'booking_date': datetime.now().strftime('%Y-%m-%d'),
            'payment_status': 'Pending'
        }
        save_booking(booking_data)

        # Send notification if OneSignal is enabled
        if ONESIGNAL_ENABLED and OneSignalManager:
            destination = get_destination_data(package['destination_id'])
            dest_name = destination['name'] if destination else 'Unknown'
            # OneSignalManager.send_booking_confirmation(
            #     user_player_id, booking_id, dest_name, travel_date
            # )

        flash(f'Booking successful! Your booking ID is {booking_id}', 'success')
        return redirect(url_for('booking_confirmation', booking_id=booking_id))

    # Get today's date for the minimum travel date field
    from datetime import date
    today_date = date.today().strftime('%Y-%m-%d')
    
    return render_template('booking.html', package=package, today_date=today_date)

@app.route('/booking/confirmation/<booking_id>')
def booking_confirmation(booking_id):
    """Booking confirmation page"""
    booking = get_booking_data(booking_id)
    if not booking:
        flash('Booking not found!', 'error')
        return redirect(url_for('index'))

    package = get_package_data(booking['package_id'])
    return render_template('booking_confirmation.html', booking=booking, package=package)

@app.route('/trip/<booking_id>')
def trip_share(booking_id):
    """Public trip share page"""
    booking = get_booking_data(booking_id)
    if not booking:
        return render_template('trip_share.html', error="Trip not found")

    package = get_package_data(booking['package_id'])
    destination = get_destination_data(package['destination_id']) if package else None
    all_reviews = get_reviews_data()
    pkg_reviews = [r for r in all_reviews.values() if r['package_id'] == booking['package_id'] and r.get('approved', True)]

    return render_template('trip_share.html', booking=booking, package=package, destination=destination, reviews=pkg_reviews)

@app.route('/reviews')
def reviews_page():
    """All reviews page"""
    all_reviews = get_reviews_data()
    approved_reviews = [r for r in all_reviews.values() if r.get('approved', True)]
    return render_template('reviews.html', reviews=approved_reviews)

@app.route('/submit-review', methods=['POST'])
def submit_review():
    """Submit a review"""
    package_id = request.form.get('package_id')
    user_name = request.form.get('user_name')
    rating = int(request.form.get('rating'))
    comment = request.form.get('comment')

    review_id = generate_review_id()
    review_data = {
        'id': review_id,
        'user_name': user_name,
        'package_id': package_id,
        'rating': rating,
        'comment': comment,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'approved': False  # Requires admin approval
    }
    save_review(review_data)

    flash('Thank you for your review! It will be visible after admin approval.', 'success')
    return redirect(url_for('package_detail', pkg_id=package_id))

@app.route('/recommendations')
def recommendations():
    """Smart destination recommendations"""
    all_destinations = get_destinations_data()
    # Simple recommendation logic based on popularity and ratings
    recommended = sorted(all_destinations.values(), key=lambda x: (x['rating'], x['reviews_count']), reverse=True)[:4]
    return render_template('recommendations.html', destinations=recommended)

# ==================== ADMIN ROUTES ====================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Simple admin auth (in production, use proper authentication)
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))

        flash('Invalid credentials!', 'error')

    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard"""
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    all_users = get_users()
    all_bookings = get_bookings_data()
    all_destinations = get_destinations_data()
    all_packages = get_packages_data()
    all_reviews = get_reviews_data()

    stats = {
        'total_users': len(all_users),
        'total_bookings': len(all_bookings),
        'total_destinations': len(all_destinations),
        'total_packages': len(all_packages),
        'pending_reviews': len([r for r in all_reviews.values() if not r.get('approved', False)]),
        'pending_bookings': len([b for b in all_bookings.values() if b['status'] == 'Pending'])
    }

    recent_bookings = sorted(all_bookings.values(), key=lambda x: x['booking_date'], reverse=True)[:5]
    pending_reviews = [r for r in all_reviews.values() if not r.get('approved', False)]

    return render_template('admin/dashboard.html', stats=stats, bookings=recent_bookings, reviews=pending_reviews)

@app.route('/admin/destinations', methods=['GET', 'POST'])
@admin_required
def admin_destinations():
    """Manage destinations with enhanced image handling"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        full_description = request.form.get('full_description', '')
        category = request.form.get('category')
        location = request.form.get('location', '')
        best_time = request.form.get('best_time', '')
        attractions = request.form.get('attractions', '')
        send_notification = request.form.get('send_notification') == 'on'
        image_url = ''
        gallery_urls = []

        # Handle main image upload
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename and allowed_file(file.filename):
                if CLOUDINARY_ENABLED and CloudinaryManager:
                    try:
                        result = CloudinaryManager.upload_image(file, folder='travelmate/destinations')
                        if result.get('success'):
                            image_url = result['url']
                        else:
                            flash(f'Image upload failed: {result.get("error", "Unknown error")}', 'error')
                            return redirect(url_for('admin_destinations'))
                    except Exception as e:
                        flash(f'Cloudinary upload error: {str(e)}', 'error')
                        return redirect(url_for('admin_destinations'))
                else:
                    # Save locally if Cloudinary is not configured
                    try:
                        filename = secure_filename(file.filename)
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(filepath)
                        image_url = url_for('static', filename=f'uploads/{filename}', _external=True)
                    except Exception as e:
                        flash(f'Local upload error: {str(e)}', 'error')
                        return redirect(url_for('admin_destinations'))

        # Handle gallery images upload
        if 'gallery_files' in request.files:
            gallery_files = request.files.getlist('gallery_files')
            for gfile in gallery_files[:5]:  # Max 5 gallery images
                if gfile and gfile.filename and allowed_file(gfile.filename):
                    if CLOUDINARY_ENABLED and CloudinaryManager:
                        try:
                            result = CloudinaryManager.upload_image(gfile, folder='travelmate/destinations/gallery')
                            if result.get('success'):
                                gallery_urls.append(result['url'])
                            else:
                                flash(f'Gallery image upload failed: {result.get("error", "Unknown error")}', 'warning')
                        except Exception as e:
                            flash(f'Gallery upload error: {str(e)}', 'warning')
                    else:
                        try:
                            filename = secure_filename(gfile.filename)
                            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                            gfile.save(filepath)
                            gallery_urls.append(url_for('static', filename=f'uploads/{filename}', _external=True))
                        except Exception as e:
                            flash(f'Gallery local upload error: {str(e)}', 'warning')

        # Use a default image if none provided
        if not image_url:
            image_url = 'https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=800'

        dest_id = generate_destination_id()
        dest_data = {
            'id': dest_id,
            'name': name,
            'description': description,
            'full_description': full_description,
            'category': category,
            'location': location,
            'best_time': best_time,
            'attractions': attractions,
            'image': image_url,
            'gallery': gallery_urls,
            'rating': 0,
            'reviews_count': 0,
            'views': 0,
            'created_at': datetime.now().strftime('%Y-%m-%d')
        }
        save_destination(dest_data)

        # Send notification to users if enabled
        if send_notification:
            notif_id = generate_notification_id()
            notif_data = {
                'id': notif_id,
                'title': f'New Destination: {name}!',
                'message': f'Explore the beautiful {name}. {description[:100]}...',
                'type': 'new_destination',
                'destination_id': dest_id,
                'created_at': datetime.now().strftime('%Y-%m-%d')
            }
            save_notification(notif_data)

            # Send via OneSignal if enabled
            if ONESIGNAL_ENABLED and OneSignalManager:
                OneSignalManager.send_notification_to_all(
                    f'New Destination: {name}!',
                    f'Explore the beautiful {name}. {description[:100]}...'
                )

        flash('Destination added successfully!', 'success')
        return redirect(url_for('admin_destinations'))

    all_destinations = get_destinations_data()
    all_categories = get_categories_data()

    # Calculate stats
    total_views = sum(d.get('views', 0) for d in all_destinations.values())
    ratings = [d.get('rating', 0) for d in all_destinations.values() if d.get('rating', 0) > 0]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0
    total_reviews = sum(d.get('reviews_count', 0) for d in all_destinations.values())

    return render_template('admin/destinations.html',
                         destinations=all_destinations,
                         categories=all_categories,
                         total_views=total_views,
                         avg_rating=avg_rating,
                         total_reviews=total_reviews)


@app.route('/admin/destination/edit/<dest_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_destination(dest_id):
    """Edit destination with enhanced image and gallery handling"""
    destination = get_destination_data(dest_id)
    if not destination:
        flash('Destination not found!', 'error')
        return redirect(url_for('admin_destinations'))

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        full_description = request.form.get('full_description', '')
        category = request.form.get('category')
        location = request.form.get('location', '')
        best_time = request.form.get('best_time', '')
        attractions = request.form.get('attractions', '')

        # Start with existing image and gallery
        image_url = destination.get('image', '')
        gallery_urls = list(destination.get('gallery', []))  # Make a copy

        # Handle new main image upload
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename and allowed_file(file.filename):
                # Delete old image if it's from Cloudinary
                if CLOUDINARY_ENABLED and CloudinaryManager and image_url and 'cloudinary' in image_url:
                    try:
                        public_id = CloudinaryManager.extract_public_id_from_url(image_url)
                        if public_id:
                            CloudinaryManager.delete_image(public_id)
                            logger = __import__('logging').getLogger(__name__)
                            logger.info(f"Deleted old main image: {public_id}")
                    except Exception as e:
                        flash(f'Failed to delete old image: {str(e)}', 'warning')

                # Upload new image
                if CLOUDINARY_ENABLED and CloudinaryManager:
                    try:
                        result = CloudinaryManager.upload_image(file, folder='travelmate/destinations')
                        if result.get('success'):
                            image_url = result['url']
                        else:
                            flash(f'Image upload failed: {result.get("error", "Unknown error")}', 'error')
                            return redirect(url_for('admin_destinations'))
                    except Exception as e:
                        flash(f'Cloudinary upload error: {str(e)}', 'error')
                        return redirect(url_for('admin_destinations'))
                else:
                    # Save locally
                    try:
                        filename = secure_filename(file.filename)
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(filepath)
                        image_url = url_for('static', filename=f'uploads/{filename}', _external=True)
                    except Exception as e:
                        flash(f'Local upload error: {str(e)}', 'error')
                        return redirect(url_for('admin_destinations'))

        # Handle gallery image deletions (sent via hidden field or session)
        images_to_delete = request.form.get('images_to_delete', '')
        if images_to_delete:
            import json
            try:
                delete_urls = json.loads(images_to_delete)
                for del_url in delete_urls:
                    if CLOUDINARY_ENABLED and CloudinaryManager and 'cloudinary' in del_url:
                        try:
                            public_id = CloudinaryManager.extract_public_id_from_url(del_url)
                            if public_id:
                                result = CloudinaryManager.delete_image(public_id)
                                logger = __import__('logging').getLogger(__name__)
                                if result.get('success'):
                                    logger.info(f"Deleted gallery image: {public_id}")
                                else:
                                    logger.warning(f"Failed to delete gallery image: {result.get('error')}")
                        except Exception as e:
                            logger = __import__('logging').getLogger(__name__)
                            logger.error(f"Error deleting gallery image: {e}")
                
                # Remove deleted images from gallery list
                gallery_urls = [url for url in gallery_urls if url not in delete_urls]
            except Exception as e:
                logger = __import__('logging').getLogger(__name__)
                logger.error(f"Error processing gallery deletions: {e}")

        # Handle new gallery image uploads
        if 'gallery_files' in request.files:
            gallery_files = request.files.getlist('gallery_files')
            for gfile in gallery_files:
                if gfile and gfile.filename and allowed_file(gfile.filename):
                    if CLOUDINARY_ENABLED and CloudinaryManager:
                        try:
                            result = CloudinaryManager.upload_image(gfile, folder='travelmate/destinations/gallery')
                            if result.get('success'):
                                gallery_urls.append(result['url'])
                            else:
                                flash(f'Gallery image upload failed: {result.get("error", "Unknown error")}', 'warning')
                        except Exception as e:
                            flash(f'Gallery upload error: {str(e)}', 'warning')
                    else:
                        try:
                            filename = secure_filename(gfile.filename)
                            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                            gfile.save(filepath)
                            gallery_urls.append(url_for('static', filename=f'uploads/{filename}', _external=True))
                        except Exception as e:
                            flash(f'Gallery local upload error: {str(e)}', 'warning')

        dest_data = {
            'name': name,
            'description': description,
            'full_description': full_description,
            'category': category,
            'location': location,
            'best_time': best_time,
            'attractions': attractions,
            'image': image_url,
            'gallery': gallery_urls
        }
        update_destination_data(dest_id, dest_data)

        flash('Destination updated successfully!', 'success')
        return redirect(url_for('admin_destinations'))

    return redirect(url_for('admin_destinations'))


# Utility function for Firebase Storage deletion (if needed)
def delete_firebase_storage_file(download_url):
    """
    Delete a file from Firebase Storage given its download URL
    This is a placeholder - requires Firebase Admin SDK setup
    """
    try:
        # This would require Firebase Admin SDK with Storage bucket access
        # Example pseudo-code:
        # from firebase_admin import storage
        # bucket = storage.bucket()
        # blob = bucket.blob(blob_path_from_url(download_url))
        # blob.delete()
        logger = __import__('logging').getLogger(__name__)
        logger.info(f"Firebase Storage deletion would delete: {download_url}")
        return True
    except Exception as e:
        logger = __import__('logging').getLogger(__name__)
        logger.error(f"Firebase Storage deletion failed: {e}")
        return False


@app.route('/admin/destination/delete/<dest_id>', methods=['POST'])
@admin_required
def admin_delete_destination(dest_id):
    """Delete destination with proper image cleanup using CloudinaryManager"""
    destination = get_destination_data(dest_id)
    if not destination:
        flash('Destination not found!', 'error')
        return redirect(url_for('admin_destinations'))

    # Handle image deletion using CloudinaryManager
    cleanup_result = None
    if CLOUDINARY_ENABLED and CloudinaryManager:
        try:
            cleanup_result = CloudinaryManager.cleanup_destination_images(destination)
            if cleanup_result.get('success'):
                deleted_count = len(cleanup_result.get('deleted', []))
                failed_count = len(cleanup_result.get('failed', []))
                if deleted_count > 0:
                    flash(f'Successfully deleted {deleted_count} images from Cloudinary', 'success')
                if failed_count > 0:
                    flash(f'Failed to delete {failed_count} images: {cleanup_result.get("failed")}', 'warning')
            else:
                flash(f'Image cleanup failed: {cleanup_result.get("error", "Unknown error")}', 'warning')
        except Exception as e:
            flash(f'Image cleanup error: {str(e)}', 'warning')
    else:
        # Handle Firebase Storage or local storage cleanup if needed
        # This would require additional implementation based on your storage setup
        logger = __import__('logging').getLogger(__name__)
        logger.info("Cloudinary not enabled, skipping image cleanup")

    # Delete from database
    delete_destination_data(dest_id)
    
    flash('Destination deleted successfully!', 'success')
    return redirect(url_for('admin_destinations'))

@app.route('/admin/packages')
@admin_required
def admin_packages():
    """Manage packages"""
    all_packages = get_packages_data()
    all_destinations = get_destinations_data()
    return render_template('admin/packages.html', packages=all_packages, destinations=all_destinations)

@app.route('/admin/package/add', methods=['GET', 'POST'])
@admin_required
def admin_add_package():
    """Add new package"""
    if request.method == 'POST':
        destination_id = request.form.get('destination_id')
        name = request.form.get('name')
        duration = request.form.get('duration')
        price = float(request.form.get('price'))
        original_price = float(request.form.get('original_price'))
        description = request.form.get('description', '')
        highlights = request.form.get('highlights', '').split('\n')
        inclusions = request.form.get('inclusions', '').split('\n')
        exclusions = request.form.get('exclusions', '').split('\n')

        # Get destination image as default
        destination = get_destination_data(destination_id)
        image_url = destination.get('image', '') if destination else ''

        # Handle file upload
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename and allowed_file(file.filename):
                if CLOUDINARY_ENABLED and CloudinaryManager:
                    result = CloudinaryManager.upload_image(file)
                    if result.get('success'):
                        image_url = result['url']
                else:
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    image_url = url_for('static', filename=f'uploads/{filename}', _external=True)

        pkg_id = generate_package_id()
        pkg_data = {
            'id': pkg_id,
            'destination_id': destination_id,
            'name': name,
            'duration': duration,
            'price': price,
            'original_price': original_price,
            'description': description,
            'image': image_url,
            'highlights': [h.strip() for h in highlights if h.strip()],
            'inclusions': [i.strip() for i in inclusions if i.strip()],
            'exclusions': [e.strip() for e in exclusions if e.strip()],
            'rating': 0,
            'reviews_count': 0,
            'created_at': datetime.now().strftime('%Y-%m-%d')
        }
        save_package(pkg_data)

        flash('Package added successfully!', 'success')
        return redirect(url_for('admin_packages'))

    all_destinations = get_destinations_data()
    return render_template('admin/package_form.html', destinations=all_destinations, action='add')

@app.route('/admin/package/edit/<pkg_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_package(pkg_id):
    """Edit package"""
    package = get_package_data(pkg_id)
    if not package:
        flash('Package not found!', 'error')
        return redirect(url_for('admin_packages'))

    if request.method == 'POST':
        destination_id = request.form.get('destination_id')
        name = request.form.get('name')
        duration = request.form.get('duration')
        price = float(request.form.get('price'))
        original_price = float(request.form.get('original_price'))
        description = request.form.get('description', '')
        highlights = request.form.get('highlights', '').split('\n')
        inclusions = request.form.get('inclusions', '').split('\n')
        exclusions = request.form.get('exclusions', '').split('\n')

        # Start with existing image
        image_url = package.get('image', '')

        # Handle file upload
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename and allowed_file(file.filename):
                if CLOUDINARY_ENABLED and CloudinaryManager:
                    result = CloudinaryManager.upload_image(file)
                    if result.get('success'):
                        image_url = result['url']
                else:
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    image_url = url_for('static', filename=f'uploads/{filename}', _external=True)

        pkg_data = {
            'destination_id': destination_id,
            'name': name,
            'duration': duration,
            'price': price,
            'original_price': original_price,
            'description': description,
            'image': image_url,
            'highlights': [h.strip() for h in highlights if h.strip()],
            'inclusions': [i.strip() for i in inclusions if i.strip()],
            'exclusions': [e.strip() for e in exclusions if e.strip()]
        }
        update_package_data(pkg_id, pkg_data)

        flash('Package updated successfully!', 'success')
        return redirect(url_for('admin_packages'))

    all_destinations = get_destinations_data()
    return render_template('admin/package_form.html', 
                         package=package, 
                         destinations=all_destinations, 
                         action='edit')

@app.route('/admin/package/delete/<pkg_id>', methods=['POST'])
@admin_required
def admin_delete_package(pkg_id):
    """Delete package"""
    package = get_package_data(pkg_id)
    if not package:
        flash('Package not found!', 'error')
        return redirect(url_for('admin_packages'))

    # Delete image from Cloudinary if it's a Cloudinary URL
    if CLOUDINARY_ENABLED and CloudinaryManager:
        image_url = package.get('image', '')
        if 'cloudinary' in image_url:
            # Extract public_id from URL
            try:
                public_id = image_url.split('/')[-1].split('.')[0]
                CloudinaryManager.delete_image(public_id)
            except:
                pass  # Ignore deletion errors

    delete_package_data(pkg_id)
    flash('Package deleted successfully!', 'success')
    return redirect(url_for('admin_packages'))

@app.route('/admin/package/<pkg_id>')
@admin_required
def admin_package_detail(pkg_id):
    """View package details"""
    package = get_package_data(pkg_id)
    if not package:
        flash('Package not found!', 'error')
        return redirect(url_for('admin_packages'))

    destination = get_destination_data(package['destination_id'])
    all_reviews = get_reviews_data()
    package_reviews = [r for r in all_reviews.values() if r['package_id'] == pkg_id]
    
    return render_template('admin/package_detail.html', 
                         package=package, 
                         destination=destination,
                         reviews=package_reviews)

@app.route('/admin/bookings')
def admin_bookings():
    """Manage bookings"""
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    status_filter = request.args.get('status', 'all')
    all_bookings = get_bookings_data()
    all_packages = get_packages_data()

    if status_filter == 'all':
        booking_list = list(all_bookings.values())
    else:
        booking_list = [b for b in all_bookings.values() if b['status'] == status_filter]

    return render_template('admin/bookings.html', bookings=booking_list, packages=all_packages)

@app.route('/admin/booking/update/<booking_id>', methods=['POST'])
def admin_update_booking(booking_id):
    """Update booking status"""
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    new_status = request.form.get('status')
    booking = get_booking_data(booking_id)
    if booking:
        update_booking_data(booking_id, {'status': new_status})

        # Send notification if OneSignal is enabled
        if ONESIGNAL_ENABLED and OneSignalManager:
            package = get_package_data(booking['package_id'])
            destination = get_destination_data(package['destination_id']) if package else None
            dest_name = destination['name'] if destination else 'Unknown'
            # OneSignalManager.send_booking_status_update(
            #     user_player_id, booking_id, new_status, dest_name
            # )

        flash(f'Booking {booking_id} updated to {new_status}!', 'success')

    return redirect(url_for('admin_bookings'))

@app.route('/admin/reviews')
def admin_reviews():
    """Manage reviews"""
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    all_reviews = get_reviews_data()
    return render_template('admin/reviews.html', reviews=list(all_reviews.values()))

@app.route('/admin/review/approve/<review_id>', methods=['POST'])
def admin_approve_review(review_id):
    """Approve a review"""
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    approve_review_data(review_id)
    flash('Review approved!', 'success')

    return redirect(url_for('admin_reviews'))

@app.route('/admin/users')
def admin_users():
    """Manage users"""
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    all_users = get_users()
    return render_template('admin/users.html', users=all_users)



# ==================== CATEGORY MANAGEMENT ROUTES ====================
@app.route('/admin/categories', methods=['GET', 'POST'])
@admin_required
def admin_categories():
    """Manage categories"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        icon = request.form.get('icon', 'fas fa-tag')
        color = request.form.get('color', '#4361ee')
        active = request.form.get('active') == 'on'

        cat_id = generate_category_id()
        cat_data = {
            'id': cat_id,
            'name': name,
            'description': description,
            'icon': icon,
            'color': color,
            'active': active,
            'destination_count': 0
        }
        save_category(cat_data)

        flash('Category added successfully!', 'success')
        return redirect(url_for('admin_categories'))

    all_categories = get_categories_data()
    all_destinations = get_destinations_data()

    # Calculate destination count for each category
    for cat_id, cat in all_categories.items():
        cat['destination_count'] = len([d for d in all_destinations.values() if d.get('category') == cat['name']])

    total_destinations = len(all_destinations)

    return render_template('admin/categories.html',
                         categories=all_categories,
                         total_destinations=total_destinations)


@app.route('/admin/category/edit/<cat_id>', methods=['POST'])
@admin_required
def admin_edit_category(cat_id):
    """Edit category"""
    category = get_category_data(cat_id)
    if not category:
        flash('Category not found!', 'error')
        return redirect(url_for('admin_categories'))

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        icon = request.form.get('icon', 'fas fa-tag')
        color = request.form.get('color', '#4361ee')
        active = request.form.get('active') == 'on'

        cat_data = {
            'name': name,
            'description': description,
            'icon': icon,
            'color': color,
            'active': active
        }
        update_category_data(cat_id, cat_data)

        flash('Category updated successfully!', 'success')
        return redirect(url_for('admin_categories'))

    return redirect(url_for('admin_categories'))


@app.route('/admin/category/delete/<cat_id>', methods=['POST'])
@admin_required
def admin_delete_category(cat_id):
    """Delete category"""
    category = get_category_data(cat_id)
    if not category:
        flash('Category not found!', 'error')
        return redirect(url_for('admin_categories'))

    # Check if any destinations use this category
    all_destinations = get_destinations_data()
    using_destinations = [d for d in all_destinations.values() if d.get('category') == category['name']]

    if using_destinations:
        flash(f'Cannot delete category! {len(using_destinations)} destination(s) are using it.', 'error')
        return redirect(url_for('admin_categories'))

    delete_category_data(cat_id)
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('admin_categories'))


@app.route('/api/categories')
def api_categories():
    """API endpoint for active categories"""
    all_categories = get_categories_data()
    active_categories = {k: v for k, v in all_categories.items() if v.get('active', True)}
    return jsonify(active_categories)


@app.route('/admin/init-firebase')
def admin_init_firebase():
    """Initialize Firebase with sample data"""
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    if not FIREBASE_ENABLED:
        flash('Firebase is not enabled. Please add serviceAccountKey.json first.', 'error')
        return redirect(url_for('admin_dashboard'))

    # Initialize sample data
    FirebaseDB.initialize_sample_data()
    flash('Firebase initialized with sample data!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/firebase-status')
def admin_firebase_status():
    """Check Firebase connection status"""
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    return jsonify({
        'firebase_enabled': FIREBASE_ENABLED,
        'cloudinary_enabled': CLOUDINARY_ENABLED,
        'onesignal_enabled': ONESIGNAL_ENABLED
    })

# ==================== USER DASHBOARD ROUTES ====================

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    user = get_user(session['user_id'])
    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('index'))

    user_email = user.get('email')
    user_bookings = get_bookings_by_user_email(user_email) if user_email else {}
    booking_list = list(user_bookings.values()) if user_bookings else []
    booking_list.sort(key=lambda x: x.get('booking_date', ''), reverse=True)

    latest_booking = booking_list[0] if booking_list else None
    latest_package = get_package_data(latest_booking['package_id']) if latest_booking else None
    favorite_count = len(user.get('favorites', []))

    completion_fields = [user.get('name'), user.get('email'), user.get('phone')]
    completed = sum(1 for value in completion_fields if value)
    profile_completion = int(round((completed / len(completion_fields)) * 100)) if completion_fields else 0

    return render_template(
        'profile.html',
        user=user,
        booking_count=len(booking_list),
        favorite_count=favorite_count,
        latest_booking=latest_booking,
        latest_package=latest_package,
        profile_completion=profile_completion
    )

@app.route('/my-bookings')
@login_required
def my_bookings():
    """User's bookings page"""
    user = get_user(session['user_id'])
    user_email = user.get('email') if user else None

    # Get bookings for this user (by email)
    user_bookings = get_bookings_by_user_email(user_email)
    booking_list = list(user_bookings.values()) if user_bookings else []
    booking_list.sort(key=lambda x: x.get('booking_date', ''), reverse=True)
    all_packages = get_packages_data()

    return render_template('my_bookings.html', bookings=booking_list, packages=all_packages)

@app.route('/favorites')
@login_required
def favorites():
    """User's favorite destinations"""
    user = get_user(session['user_id'])
    favorite_ids = user.get('favorites', []) if user else []

    # Get favorite destinations
    favorite_destinations = [get_destination_data(fid) for fid in favorite_ids if get_destination_data(fid)]

    return render_template('favorites.html', favorites=favorite_destinations)

@app.route('/toggle-favorite/<dest_id>')
def toggle_favorite(dest_id):
    """Toggle favorite destination"""
    if not session.get('user_id'):
        return jsonify({'success': False, 'message': 'Please login first'})

    user = get_user(session['user_id'])
    if not user:
        return jsonify({'success': False, 'message': 'User not found'})

    if 'favorites' not in user:
        user['favorites'] = []

    if dest_id in user['favorites']:
        user['favorites'].remove(dest_id)
        update_user_data(session['user_id'], {'favorites': user['favorites']})
        return jsonify({'success': True, 'action': 'removed'})
    else:
        user['favorites'].append(dest_id)
        update_user_data(session['user_id'], {'favorites': user['favorites']})
        return jsonify({'success': True, 'action': 'added'})

# ==================== API ROUTES ====================

@app.route('/api/destinations')
def api_destinations():
    """API endpoint for destinations"""
    all_destinations = get_destinations_data()
    return jsonify(list(all_destinations.values()))

@app.route('/api/packages')
def api_packages():
    """API endpoint for packages"""
    all_packages = get_packages_data()
    return jsonify(list(all_packages.values()))

@app.route('/api/notifications')
def api_notifications():
    """API endpoint for notifications"""
    all_notifications = get_notifications_data()
    return jsonify(all_notifications)

@app.route('/api/send-notification', methods=['POST'])
def api_send_notification():
    """API endpoint to send notification (admin only)"""
    if not session.get('admin'):
        return jsonify({'success': False, 'error': 'Admin access required'})

    data = request.get_json()
    title = data.get('title')
    message = data.get('message')
    notification_type = data.get('type', 'info')

    if not title or not message:
        return jsonify({'success': False, 'error': 'Title and message required'})

    # Save notification to database
    notif_id = generate_notification_id()
    notif_data = {
        'id': notif_id,
        'title': title,
        'message': message,
        'type': notification_type
    }
    save_notification(notif_data)

    # Send via OneSignal
    if ONESIGNAL_ENABLED and OneSignalManager:
        result = OneSignalManager.send_notification_to_all(title, message)
        return jsonify(result)

    return jsonify({'success': True, 'message': 'Notification saved (OneSignal not configured)'})

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
