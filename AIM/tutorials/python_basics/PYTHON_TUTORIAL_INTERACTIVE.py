# Simple Python Examples - Start Here!
# This file has basic examples you can run and modify

print("=== WELCOME TO PYTHON! ===")
print("Let's learn step by step...\n")

# 1. VARIABLES - Storing Information
print("1. VARIABLES - Like labeled boxes to store things")
name = "Alice"              # Text (string)
age = 25                    # Number (integer)
height = 5.6               # Decimal number (float)
is_student = True          # True/False (boolean)

print(f"Name: {name}")
print(f"Age: {age}")
print(f"Height: {height} feet")
print(f"Is student: {is_student}")
print()

# 2. LISTS - Multiple items in order
print("2. LISTS - Collections of items")
fruits = ["apple", "banana", "orange", "grape"]
numbers = [1, 2, 3, 4, 5]

print(f"Fruits: {fruits}")
print(f"First fruit: {fruits[0]}")      # Index starts at 0
print(f"Last fruit: {fruits[-1]}")      # -1 means last item
print(f"Number of fruits: {len(fruits)}")
print()

# 3. DICTIONARIES - Key-Value Pairs (like a phone book)
print("3. DICTIONARIES - Key-value pairs")
person = {
    "name": "John",
    "age": 30,
    "city": "New York",
    "job": "Teacher"
}

print(f"Person info: {person}")
print(f"Name: {person['name']}")
print(f"Age: {person['age']}")
print()

# 4. IF STATEMENTS - Making Decisions
print("4. IF STATEMENTS - Making decisions")
temperature = 75

if temperature > 80:
    weather = "Hot"
elif temperature > 60:
    weather = "Nice"
else:
    weather = "Cold"

print(f"Temperature is {temperature}°F - That's {weather}!")
print()

# 5. LOOPS - Repeating Actions
print("5. LOOPS - Repeating actions")

print("Counting to 5:")
for i in range(1, 6):       # range(1, 6) gives 1, 2, 3, 4, 5
    print(f"  Count: {i}")

print("\nGoing through fruits:")
for fruit in fruits:
    print(f"  I like {fruit}")
print()

# 6. FUNCTIONS - Reusable Code Blocks
print("6. FUNCTIONS - Reusable code blocks")

def greet_person(name, age):
    """This function greets a person"""
    message = f"Hello {name}! You are {age} years old."
    return message

def calculate_area(length, width):
    """Calculate area of rectangle"""
    area = length * width
    return area

# Using the functions
greeting = greet_person("Sarah", 28)
print(greeting)

room_area = calculate_area(12, 10)
print(f"Room area: {room_area} square feet")
print()

# 7. CLASSES - Creating Your Own Data Types
print("7. CLASSES - Creating your own data types")

class Dog:
    """A simple dog class"""
    
    def __init__(self, name, breed, age):
        """Initialize a new dog"""
        self.name = name
        self.breed = breed
        self.age = age
        self.tricks = []
    
    def bark(self):
        """Make the dog bark"""
        return f"{self.name} says Woof!"
    
    def learn_trick(self, trick):
        """Teach the dog a trick"""
        self.tricks.append(trick)
        return f"{self.name} learned {trick}!"
    
    def show_info(self):
        """Show dog information"""
        info = f"{self.name} is a {self.age} year old {self.breed}"
        if self.tricks:
            info += f" who knows: {', '.join(self.tricks)}"
        return info

# Creating dog objects
buddy = Dog("Buddy", "Golden Retriever", 3)
max_dog = Dog("Max", "German Shepherd", 5)

print(buddy.bark())
print(buddy.learn_trick("sit"))
print(buddy.learn_trick("roll over"))
print(buddy.show_info())
print()

# 8. ERROR HANDLING - Dealing with Problems
print("8. ERROR HANDLING - Dealing with problems")

def safe_divide(a, b):
    """Safely divide two numbers"""
    try:
        result = a / b
        return f"{a} ÷ {b} = {result}"
    except ZeroDivisionError:
        return "Error: Cannot divide by zero!"
    except TypeError:
        return "Error: Please use numbers only!"

print(safe_divide(10, 2))      # Normal case
print(safe_divide(10, 0))      # Division by zero
print(safe_divide("10", 2))    # Wrong type
print()

# 9. WORKING WITH FILES (Simple Example)
print("9. WORKING WITH FILES")

# Writing to a file
student_data = {
    "name": "Emma",
    "grade": "A",
    "subjects": ["Math", "Science", "English"]
}

try:
    # Convert to JSON and save
    import json
    with open("student.json", "w") as file:
        json.dump(student_data, file, indent=2)
    print("✅ Student data saved to student.json")
    
    # Read it back
    with open("student.json", "r") as file:
        loaded_data = json.load(file)
    print(f"✅ Loaded data: {loaded_data}")
    
except Exception as e:
    print(f"❌ File error: {e}")

print()

# 10. PRACTICAL EXAMPLE - Simple Calculator
print("10. PRACTICAL EXAMPLE - Simple Calculator")

class Calculator:
    """A simple calculator class"""
    
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a, b):
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a, b):
        result = a * b
        self.history.append(f"{a} × {b} = {result}")
        return result
    
    def divide(self, a, b):
        if b == 0:
            return "Error: Division by zero!"
        result = a / b
        self.history.append(f"{a} ÷ {b} = {result}")
        return result
    
    def show_history(self):
        if not self.history:
            return "No calculations yet!"
        return "Calculation history:\n" + "\n".join(self.history)

# Using the calculator
calc = Calculator()

print(f"5 + 3 = {calc.add(5, 3)}")
print(f"10 - 4 = {calc.subtract(10, 4)}")
print(f"6 × 7 = {calc.multiply(6, 7)}")
print(f"15 ÷ 3 = {calc.divide(15, 3)}")
print()
print(calc.show_history())
print()

# 11. UNDERSTANDING YOUR PROJECT CODE
print("11. UNDERSTANDING YOUR PROJECT CODE")
print("Your AIM project uses these concepts:")
print("- Classes (like FastUIParser)")
print("- Methods (functions inside classes)")
print("- Dictionaries (for storing data)")
print("- Error handling (try/except)")
print("- File operations (reading JSON)")
print("- Type hints (Dict[str, Any])")
print("- Imports (bringing in other modules)")
print()

print("🎉 CONGRATULATIONS! You've seen the basics of Python!")
print("💡 TIP: Try modifying the values above and run this file again!")
print("📚 Next: Look at your project files and see if you can identify these patterns!")
