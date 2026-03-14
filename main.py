"""
TravelMate AI - Smart Travel Management System
Main Entry Point

Run this file to start the Flask application.
"""

import sys
import os

# Add TravelMate directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'TravelMate'))

from TravelMate.app import app

if __name__ == '__main__':
    print("=" * 50)
    print("TravelMate AI - Smart Travel Management System")
    print("=" * 50)
    print("\nStarting server...")
    print("Open http://localhost:5000 in your browser")
    print("\nAdmin Login: username: admin, password: admin123")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
