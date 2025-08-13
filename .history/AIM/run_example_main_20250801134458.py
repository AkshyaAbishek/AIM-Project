"""
Wrapper script to run example_main.py with proper imports
"""
import os
import sys

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Add parent directory to path
sys.path.insert(0, parent_dir)

# Import the main script as a module
from app.example_main import main

if __name__ == "__main__":
    main()
