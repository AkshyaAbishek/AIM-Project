# Python Programming Concepts Explained
# Using examples from your AIM project

"""
=== PYTHON BASICS EXPLAINED ===
This guide explains Python concepts using code from your actuarial project.
"""

# 1. COMMENTS AND DOCSTRINGS
# ===========================

# This is a single-line comment (starts with #)
# Comments explain what code does but don't run

"""
This is a multi-line docstring (triple quotes)
Docstrings document what functions/classes do
They appear at the top of modules, classes, and functions
"""

# 2. IMPORTS - BRINGING CODE FROM OTHER FILES
# ============================================

import json                    # Built-in module for JSON data
import logging                 # Built-in module for logging
from typing import Dict, Any   # Import specific items from typing module
from datetime import datetime  # Import datetime class from datetime module

# What this means:
# - json: lets you work with JSON data (like {"name": "John"})
# - logging: lets you record what your program is doing
# - Dict, Any: help with type hints (explained later)
# - datetime: lets you work with dates and times

# 3. CLASSES - BLUEPRINTS FOR OBJECTS
# ====================================

class FastUIParser:
    """
    A class is like a blueprint for creating objects.
    Think of it like a cookie cutter - it defines the shape,
    but you can make many cookies (objects) from it.
    """
    
    def __init__(self):
        """
        __init__ is a special method called when you create an object.
        It's like the constructor - it sets up the object.
        'self' refers to the specific object being created.
        """
        # self.logger creates an attribute (property) of this object
        self.logger = logging.getLogger(__name__)
        # This creates a logger for this specific class
    
    def parse(self, fast_ui_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        This is a method (function inside a class).
        
        PARAMETERS EXPLAINED:
        - self: refers to this specific object
        - fast_ui_data: Dict[str, Any] means a dictionary where:
          * keys are strings (str)
          * values can be anything (Any)
          
        RETURN TYPE:
        - -> Dict[str, Any]: means this function returns a dictionary
        
        TYPE HINTS:
        - Dict[str, Any] is a "type hint" - it tells other programmers
          what type of data to expect, but Python doesn't enforce it
        """
        # try/except is error handling
        try:
            # Code that might fail goes here
            self.logger.info("Starting FAST UI data parsing")
            
            # VARIABLES
            parsed_data = {}  # Creates an empty dictionary
            
            # CONDITIONAL STATEMENTS (if/else)
            if self._is_nested_structure(fast_ui_data):
                # If condition is True, do this
                parsed_data = self._parse_nested_structure(fast_ui_data)
            else:
                # If condition is False, do this instead
                parsed_data = self._parse_flat_structure(fast_ui_data)
            
            # FUNCTION CALLS
            cleaned_data = self._clean_data(parsed_data)
            # This calls another method and stores the result
            
            # DICTIONARIES - Key-Value Pairs
            cleaned_data["_parsing_metadata"] = {
                "parsed_at": datetime.now().isoformat(),
                "original_fields_count": len(fast_ui_data),
                "parsed_fields_count": len(cleaned_data) - 1,
                "parser_version": "1.0.0"
            }
            # This adds a new key-value pair to the dictionary
            
            return cleaned_data  # Returns the result
            
        except Exception as e:
            # If any error occurs, this block runs
            self.logger.error(f"FAST UI parsing failed: {str(e)}")
            # f"text {variable}" is an f-string - it inserts variable values
            raise ParsingError(f"Failed to parse FAST UI data: {str(e)}")
            # 'raise' throws an error to the caller

# 4. METHODS AND FUNCTIONS
# =========================

    def _is_nested_structure(self, data: Dict[str, Any]) -> bool:
        """
        Methods starting with _ are "private" - meant for internal use only.
        
        RETURN TYPE: bool means True or False
        """
        
        # LISTS - Ordered collections
        nested_indicators = ["applicant", "policy", "coverage", "beneficiary"]
        # Lists use square brackets [], items separated by commas
        
        # FOR LOOPS - Repeat code for each item
        for indicator in nested_indicators:
            # This repeats for each item in the list
            # 'indicator' becomes each value: "applicant", "policy", etc.
            
            # BOOLEAN LOGIC (and, or, not)
            if indicator in data and isinstance(data[indicator], dict):
                # 'in' checks if something exists in a collection
                # 'isinstance()' checks if something is a specific type
                # 'and' means both conditions must be True
                return True
        
        # Another for loop with .values()
        for value in data.values():
            # .values() gets all values from a dictionary
            if isinstance(value, dict):
                return True
        
        return False  # If no nested structure found

# 5. DATA TYPES IN PYTHON
# ========================

# Numbers
age = 25                    # Integer (whole number)
price = 99.99              # Float (decimal number)

# Text
name = "John Doe"          # String (text)
description = 'Also a string'  # Single or double quotes work

# Boolean (True/False)
is_active = True
is_expired = False

# Collections
numbers = [1, 2, 3, 4]     # List (ordered, changeable)
person = {                 # Dictionary (key-value pairs)
    "name": "John",
    "age": 30,
    "city": "New York"
}

# None (represents "nothing")
result = None

# 6. COMMON OPERATIONS
# ====================

# String operations
text = "Hello World"
print(len(text))           # Length: 11
print(text.upper())        # HELLO WORLD
print(text.lower())        # hello world

# List operations
fruits = ["apple", "banana", "orange"]
fruits.append("grape")     # Add item
print(len(fruits))         # Length: 4

# Dictionary operations
person = {"name": "John", "age": 30}
person["email"] = "john@email.com"  # Add new key-value
print(person["name"])      # Get value: "John"

# 7. CONTROL FLOW
# ================

# If statements
age = 18
if age >= 18:
    print("Adult")
elif age >= 13:
    print("Teenager")
else:
    print("Child")

# For loops
for i in range(5):         # 0, 1, 2, 3, 4
    print(f"Number: {i}")

# While loops
count = 0
while count < 3:
    print(f"Count: {count}")
    count += 1             # Same as: count = count + 1

# 8. FUNCTIONS
# ============

def calculate_total(price, tax_rate):
    """
    Functions are reusable blocks of code.
    They take inputs (parameters) and can return outputs.
    """
    tax = price * tax_rate
    total = price + tax
    return total           # Send result back to caller

# Using the function
final_price = calculate_total(100, 0.08)  # $108.00

# 9. ERROR HANDLING
# ==================

try:
    # Code that might fail
    result = 10 / 0        # This will cause an error
except ZeroDivisionError:
    # Handle specific error
    print("Cannot divide by zero!")
except Exception as e:
    # Handle any other error
    print(f"Something went wrong: {e}")
finally:
    # This always runs, error or not
    print("Cleanup code here")

# 10. FILE OPERATIONS (from your project)
# =======================================

# Reading JSON files
try:
    with open("data.json", "r") as file:
        data = json.load(file)  # Load JSON into Python dictionary
except FileNotFoundError:
    print("File not found!")

# Writing JSON files
data = {"name": "John", "age": 30}
with open("output.json", "w") as file:
    json.dump(data, file, indent=2)  # Save dictionary as JSON

# 11. OBJECT-ORIENTED CONCEPTS
# ============================

class Car:
    """Example class to show OOP concepts"""
    
    def __init__(self, brand, model):
        # Attributes (properties)
        self.brand = brand
        self.model = model
        self.speed = 0
    
    def accelerate(self, amount):
        # Methods (actions the object can do)
        self.speed += amount
        return f"Speed is now {self.speed} mph"
    
    def brake(self):
        self.speed = 0
        return "Car stopped"

# Creating objects (instances)
my_car = Car("Toyota", "Camry")      # Create a car object
print(my_car.brand)                  # Access attribute: "Toyota"
print(my_car.accelerate(30))         # Call method: "Speed is now 30 mph"

# 12. MODULES AND PACKAGES
# =========================

# Your project structure:
# AIM/
#   ├── src/
#   │   ├── parsers/
#   │   │   └── fast_ui_parser.py    # This file
#   │   └── aim_processor.py
#   └── example.py

# Importing from your own modules:
# from src.parsers.fast_ui_parser import FastUIParser

# 13. COMMON PYTHON PATTERNS IN YOUR PROJECT
# ==========================================

# List comprehension (compact way to create lists)
squared_numbers = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]

# Dictionary comprehension
word_lengths = {word: len(word) for word in ["apple", "banana", "orange"]}

# Checking if key exists in dictionary
if "name" in person:
    print(person["name"])

# Getting dictionary value with default
age = person.get("age", 0)  # Returns 0 if "age" key doesn't exist

# F-strings for formatting
name = "John"
age = 30
message = f"Hello, my name is {name} and I am {age} years old"

"""
KEY TAKEAWAYS FOR BEGINNERS:

1. Python is readable - it's designed to look like English
2. Indentation matters - it shows which code belongs together
3. Everything is an object - strings, numbers, functions, etc.
4. Use descriptive variable names
5. Functions and classes help organize code
6. Comments explain WHY you wrote code, not just what it does
7. Error handling prevents crashes
8. Start small and build up complexity

NEXT STEPS:
1. Try modifying small parts of the code
2. Add print() statements to see what variables contain
3. Practice with simple examples before complex ones
4. Don't worry about understanding everything at once!
"""
