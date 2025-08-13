"""
Diagnostic script to check Flask routing
"""
import os
import sys
import traceback

try:
    print("Importing web_app...")
    import web_app
    
    print("\nAll registered routes:")
    for rule in sorted(web_app.app.url_map.iter_rules(), key=lambda x: str(x)):
        print(f"Route: {rule}, Methods: {rule.methods}, Endpoint: {rule.endpoint}")
    
    print("\nChecking specific routes:")
    routes = [rule.endpoint for rule in web_app.app.url_map.iter_rules()]
    print(f"'/' exists: {'index' in routes}")
    print(f"'/help' exists: {'help_page' in routes}")
    print(f"'/upload' exists: {'upload_file' in routes}")
    print(f"'/view-data' exists: {'view_data' in routes}")
    print(f"'/compare' exists: {'compare' in routes}")
    
    print("\nView functions:")
    for endpoint, view_func in web_app.app.view_functions.items():
        print(f"Endpoint: {endpoint}, Function: {view_func.__name__ if hasattr(view_func, '__name__') else view_func}")
    
    print("\nBlueprints:")
    if hasattr(web_app.app, 'blueprints'):
        for name, blueprint in web_app.app.blueprints.items():
            print(f"Blueprint: {name}")
    else:
        print("No blueprints found")

except Exception as e:
    print(f"ERROR: {str(e)}")
    print("Traceback:")
    traceback.print_exc()
