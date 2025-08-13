"""
Wrapper script to run example_main.py with proper imports
"""
import os
import sys

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add src directory to Python path
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

print(f"Added to Python path: {src_path}")

# Now run the script with exec to avoid import issues
exec(open(os.path.join(current_dir, 'app', 'example_main.py')).read())
