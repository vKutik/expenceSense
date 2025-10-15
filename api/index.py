"""
Vercel entry point for the expense tracker application
"""
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app
from app import app

# Export the app for Vercel
application = app

if __name__ == "__main__":
    app.run()
