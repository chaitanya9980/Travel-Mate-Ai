"""
Firebase Configuration for TravelMate AI
Replace with your actual Firebase credentials
"""

import os
import json

# Firebase configuration - Replace with your actual config
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyBsVS43MVKVljQezNhoEAgpCN6JQ8jb7hA",
    "authDomain": "traval-meta-ai.firebaseapp.com",
    "projectId": "traval-meta-ai",
    "storageBucket": "traval-meta-ai.firebasestorage.app",
    "messagingSenderId": "1028167973278",
    "appId": "1:1028167973278:web:dd8fb1556aafa542597e8f",
    "measurementId": "G-Q2E49C25SR",
    "databaseURL": "https://traval-meta-ai-default-rtdb.firebaseio.com/"
}

# Try to initialize Firebase
firebase_app = None
db_ref = None

try:
    import firebase_admin
    from firebase_admin import credentials, db
    
    # Check if service account key exists
    service_account_path = os.path.join(os.path.dirname(__file__), 'serviceAccountKey.json')
    
    if os.path.exists(service_account_path):
        cred = credentials.Certificate(service_account_path)
        firebase_app = firebase_admin.initialize_app(cred, {
            'databaseURL': FIREBASE_CONFIG['databaseURL']
        })
        db_ref = db
        FIREBASE_ENABLED = True
        print("Firebase: Connected successfully! Using Firebase Realtime Database.")
    else:
        FIREBASE_ENABLED = False
        print("Firebase: serviceAccountKey.json not found. Using mock database.")
except ImportError:
    FIREBASE_ENABLED = False
    print("Firebase: firebase-admin not installed. Using mock database.")
except Exception as e:
    FIREBASE_ENABLED = False
    print(f"Firebase: Initialization failed. Using mock database. Error: {e}")

class FirebaseDB:
    """
    Firebase Database Helper Class
    Provides methods for CRUD operations on Firebase Realtime Database
    """

    @staticmethod
    def _get_ref(path):
        """Get database reference"""
        if FIREBASE_ENABLED and db_ref:
            return db_ref.reference(path)
        return None

    @staticmethod
    def create_user(user_data):
        """Create a new user"""
        ref = FirebaseDB._get_ref(f"/users/{user_data['id']}")
        if ref:
            ref.set(user_data)
            return True
        return False

    @staticmethod
    def get_user(user_id):
        """Get user by ID"""
        ref = FirebaseDB._get_ref(f"/users/{user_id}")
        if ref:
            return ref.get()
        return None

    @staticmethod
    def get_user_by_email(email):
        """Get user by email"""
        ref = FirebaseDB._get_ref("/users")
        if ref:
            users = ref.get()
            if users:
                for user_id, user_data in users.items():
                    if user_data.get('email') == email:
                        return user_data
        return None

    @staticmethod
    def get_all_users():
        """Get all users"""
        ref = FirebaseDB._get_ref("/users")
        if ref:
            return ref.get() or {}
        return None

    @staticmethod
    def update_user(user_id, data):
        """Update user data"""
        ref = FirebaseDB._get_ref(f"/users/{user_id}")
        if ref:
            ref.update(data)
            return True
        return False

    @staticmethod
    def create_destination(destination_data):
        """Create a new destination"""
        ref = FirebaseDB._get_ref(f"/destinations/{destination_data['id']}")
        if ref:
            ref.set(destination_data)
            return True
        return False

    @staticmethod
    def get_destination(dest_id):
        """Get destination by ID"""
        ref = FirebaseDB._get_ref(f"/destinations/{dest_id}")
        if ref:
            return ref.get()
        return None

    @staticmethod
    def get_destinations():
        """Get all destinations"""
        ref = FirebaseDB._get_ref("/destinations")
        if ref:
            return ref.get() or {}
        return None

    @staticmethod
    def update_destination(dest_id, data):
        """Update destination data"""
        ref = FirebaseDB._get_ref(f"/destinations/{dest_id}")
        if ref:
            ref.update(data)
            return True
        return False

    @staticmethod
    def delete_destination(dest_id):
        """Delete destination"""
        ref = FirebaseDB._get_ref(f"/destinations/{dest_id}")
        if ref:
            ref.delete()
            return True
        return False

    @staticmethod
    def create_package(package_data):
        """Create a new package"""
        ref = FirebaseDB._get_ref(f"/packages/{package_data['id']}")
        if ref:
            ref.set(package_data)
            return True
        return False

    @staticmethod
    def get_package(pkg_id):
        """Get package by ID"""
        ref = FirebaseDB._get_ref(f"/packages/{pkg_id}")
        if ref:
            return ref.get()
        return None

    @staticmethod
    def get_packages():
        """Get all packages"""
        ref = FirebaseDB._get_ref("/packages")
        if ref:
            return ref.get() or {}
        return None

    @staticmethod
    def update_package(pkg_id, data):
        """Update package data"""
        ref = FirebaseDB._get_ref(f"/packages/{pkg_id}")
        if ref:
            ref.update(data)
            return True
        return False

    @staticmethod
    def delete_package(pkg_id):
        """Delete package"""
        ref = FirebaseDB._get_ref(f"/packages/{pkg_id}")
        if ref:
            ref.delete()
            return True
        return False

    @staticmethod
    def create_booking(booking_data):
        """Create a new booking"""
        ref = FirebaseDB._get_ref(f"/bookings/{booking_data['id']}")
        if ref:
            ref.set(booking_data)
            return True
        return False

    @staticmethod
    def get_booking(booking_id):
        """Get booking by ID"""
        ref = FirebaseDB._get_ref(f"/bookings/{booking_id}")
        if ref:
            return ref.get()
        return None

    @staticmethod
    def get_bookings():
        """Get all bookings"""
        ref = FirebaseDB._get_ref("/bookings")
        if ref:
            return ref.get() or {}
        return None

    @staticmethod
    def get_bookings_by_email(email):
        """Get bookings by user email"""
        ref = FirebaseDB._get_ref("/bookings")
        if ref:
            bookings = ref.get() or {}
            return {k: v for k, v in bookings.items() if v.get('email') == email}
        return None

    @staticmethod
    def update_booking_status(booking_id, status):
        """Update booking status"""
        ref = FirebaseDB._get_ref(f"/bookings/{booking_id}")
        if ref:
            ref.update({'status': status})
            return True
        return False

    @staticmethod
    def update_booking(booking_id, data):
        """Update booking data"""
        ref = FirebaseDB._get_ref(f"/bookings/{booking_id}")
        if ref:
            ref.update(data)
            return True
        return False

    @staticmethod
    def create_review(review_data):
        """Create a new review"""
        ref = FirebaseDB._get_ref(f"/reviews/{review_data['id']}")
        if ref:
            ref.set(review_data)
            return True
        return False

    @staticmethod
    def get_review(review_id):
        """Get review by ID"""
        ref = FirebaseDB._get_ref(f"/reviews/{review_id}")
        if ref:
            return ref.get()
        return None

    @staticmethod
    def get_reviews():
        """Get all reviews"""
        ref = FirebaseDB._get_ref("/reviews")
        if ref:
            return ref.get() or {}
        return None

    @staticmethod
    def get_reviews_by_package(package_id):
        """Get reviews by package ID"""
        ref = FirebaseDB._get_ref("/reviews")
        if ref:
            reviews = ref.get() or {}
            return {k: v for k, v in reviews.items() if v.get('package_id') == package_id}
        return None

    @staticmethod
    def approve_review(review_id):
        """Approve a review"""
        ref = FirebaseDB._get_ref(f"/reviews/{review_id}")
        if ref:
            ref.update({'approved': True})
            return True
        return False

    @staticmethod
    def delete_review(review_id):
        """Delete a review"""
        ref = FirebaseDB._get_ref(f"/reviews/{review_id}")
        if ref:
            ref.delete()
            return True
        return False

    @staticmethod
    def create_notification(notification_data):
        """Create a new notification"""
        ref = FirebaseDB._get_ref(f"/notifications/{notification_data['id']}")
        if ref:
            ref.set(notification_data)
            return True
        return False

    @staticmethod
    def get_notifications():
        """Get all notifications"""
        ref = FirebaseDB._get_ref("/notifications")
        if ref:
            return ref.get() or {}
        return None

    @staticmethod
    def delete_notification(notification_id):
        """Delete a notification"""
        ref = FirebaseDB._get_ref(f"/notifications/{notification_id}")
        if ref:
            ref.delete()
            return True
        return False

    @staticmethod
    def initialize_sample_data():
        """Initialize database with sample data"""
        # Sample destinations
        sample_destinations = {
            "DEST001": {
                "id": "DEST001",
                "name": "Goa",
                "description": "Beautiful beaches, vibrant nightlife, and Portuguese heritage",
                "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800",
                "category": "Beaches",
                "rating": 4.5,
                "reviews_count": 128
            },
            "DEST002": {
                "id": "DEST002",
                "name": "Manali",
                "description": "Snow-capped mountains, adventure sports, and scenic valleys",
                "image": "https://images.unsplash.com/photo-1626010448982-4d629b1a0151?w=800",
                "category": "Mountains",
                "rating": 4.7,
                "reviews_count": 95
            },
            "DEST003": {
                "id": "DEST003",
                "name": "Kerala",
                "description": "Backwaters, houseboats, and lush green landscapes",
                "image": "https://images.unsplash.com/photo-1609766857041-ed402ea8069a?w=800",
                "category": "Backwaters",
                "rating": 4.6,
                "reviews_count": 87
            },
            "DEST004": {
                "id": "DEST004",
                "name": "Jaipur",
                "description": "Royal palaces, forts, and rich Rajasthani culture",
                "image": "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=800",
                "category": "Heritage",
                "rating": 4.4,
                "reviews_count": 76
            },
            "DEST005": {
                "id": "DEST005",
                "name": "Kashmir",
                "description": "Paradise on Earth with stunning valleys and lakes",
                "image": "https://images.unsplash.com/photo-1566837497312-7be7830a7a7a?w=800",
                "category": "Mountains",
                "rating": 4.8,
                "reviews_count": 64
            },
            "DEST006": {
                "id": "DEST006",
                "name": "Andaman",
                "description": "Pristine beaches, coral reefs, and water sports",
                "image": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800",
                "category": "Beaches",
                "rating": 4.6,
                "reviews_count": 52
            }
        }

        # Sample packages
        sample_packages = {
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

        # Sample reviews
        sample_reviews = {
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

        # Sample notifications
        sample_notifications = {
            "1": {"id": "1", "title": "20% Discount on Goa Packages!", "message": "Book before Sunday to avail this offer.", "type": "promo"},
            "2": {"id": "2", "title": "New Destination Added", "message": "Explore the beautiful Andaman Islands now!", "type": "info"},
            "3": {"id": "3", "title": "Summer Special", "message": "Get up to 30% off on all mountain destinations.", "type": "promo"}
        }

        # Write to Firebase
        dest_ref = FirebaseDB._get_ref("/destinations")
        if dest_ref:
            dest_ref.set(sample_destinations)

        pkg_ref = FirebaseDB._get_ref("/packages")
        if pkg_ref:
            pkg_ref.set(sample_packages)

        rev_ref = FirebaseDB._get_ref("/reviews")
        if rev_ref:
            rev_ref.set(sample_reviews)

        notif_ref = FirebaseDB._get_ref("/notifications")
        if notif_ref:
            notif_ref.set(sample_notifications)

        return True

# Instructions for Firebase Setup:
"""
1. Go to https://firebase.google.com/ and create a new project
2. Enable Realtime Database in Firebase Console
3. Go to Project Settings > Service Accounts
4. Click "Generate new private key" to download serviceAccountKey.json
5. Place the serviceAccountKey.json file in the TravelMate folder
6. Install firebase-admin: pip install firebase-admin
7. The app will automatically use Firebase when the key file is present
8. If Firebase is not configured, the app will use mock database (in-memory)
"""
