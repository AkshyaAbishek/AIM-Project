import os
import sys
import traceback

print("Starting AIM Web Application...")
print(f"Current working directory: {os.getcwd()}")

try:
    # Set app environment variables
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    
    # Try to import the Flask app
    print("Importing web_app...")
    import web_app
    
    print("Successfully imported web_app")
    print("Starting Flask server...")
    
    # Run the Flask app
    web_app.app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False
    )
    
except Exception as e:
    print(f"ERROR: {str(e)}")
    print("Traceback:")
    traceback.print_exc()
