# Palindrome Checker

A comprehensive Python module for checking palindromes in numbers and strings, with various related operations.

## Features

- **Number Palindrome Checking**: Efficiently determine if a number is a palindrome
- **String Palindrome Checking**: Check if words or phrases are palindromes (ignoring case and spaces)
- **Palindrome Range Finding**: Find all palindromic numbers within a range
- **Next Palindrome Finding**: Find the next palindromic number after a given number
- **Longest Palindromic Substring**: Find the longest palindromic substring in a text
- **Interactive Menu**: User-friendly command-line interface

## Functions

### `is_palindrome_number(number)`
Checks if a given number is a palindrome.

**Parameters:**
- `number` (int): The number to check for palindrome

**Returns:**
- `bool`: True if the number is a palindrome, False otherwise

**Example:**
```python
print(is_palindrome_number(121))   # True
print(is_palindrome_number(123))   # False
```

### `is_palindrome_string(text)`
Checks if a given string is a palindrome (ignoring case, spaces, and punctuation).

**Parameters:**
- `text` (str): The string to check for palindrome

**Returns:**
- `bool`: True if the string is a palindrome, False otherwise

**Example:**
```python
print(is_palindrome_string("racecar"))                    # True
print(is_palindrome_string("A man a plan a canal Panama")) # True
```

### `find_palindromes_in_range(start, end)`
Finds all palindromic numbers in a given range.

**Parameters:**
- `start` (int): The starting number of the range
- `end` (int): The ending number of the range

**Returns:**
- `list`: A list of all palindromic numbers in the range

**Example:**
```python
palindromes = find_palindromes_in_range(100, 200)
print(palindromes)  # [101, 111, 121, 131, 141, 151, 161, 171, 181, 191]
```

### `find_next_palindrome(number)`
Finds the next palindromic number after a given number.

**Parameters:**
- `number` (int): The number to find the next palindrome after

**Returns:**
- `int`: The next palindromic number after the given number

### `longest_palindromic_substring(text)`
Finds the longest palindromic substring in a given text.

**Parameters:**
- `text` (str): The text to search for palindromes

**Returns:**
- `str`: The longest palindromic substring

## Usage

### Running the Script
```bash
python palindrome_checker.py
```

This will show a menu with the following options:
1. Check if a number is palindrome
2. Check if a string/phrase is palindrome
3. Find palindromes in a number range
4. Find the next palindrome after a number
5. Find longest palindromic substring
6. Run demonstration with sample data
7. Exit

### Using as a Module
```python
from palindrome_checker import is_palindrome_number, is_palindrome_string

# Check if a number is palindrome
result = is_palindrome_number(12321)
print(f"12321 is palindrome: {result}")

# Check if a string is palindrome
result = is_palindrome_string("Madam")
print(f"'Madam' is palindrome: {result}")
```

## Algorithm Complexity

- **is_palindrome_number()**: O(log n) time complexity (where n is the number)
- **is_palindrome_string()**: O(n) time complexity (where n is string length)
- **find_palindromes_in_range()**: O(m * log k) where m is range size and k is average number size
- **longest_palindromic_substring()**: O(n²) time complexity using expand around centers

## Requirements

- Python 3.6+
- No external dependencies (uses only built-in Python features)

## Examples

```python
# Basic palindrome checking
print(is_palindrome_number(121))    # True
print(is_palindrome_number(123))    # False
print(is_palindrome_string("level")) # True
print(is_palindrome_string("hello")) # False

# Finding multiple palindromes
palindromes = find_palindromes_in_range(10, 100)
print(palindromes)   # [11, 22, 33, 44, 55, 66, 77, 88, 99]

# Finding the next palindrome
next_pal = find_next_palindrome(150)
print(f"The next palindrome after 150 is {next_pal}")

# Longest palindromic substring
longest = longest_palindromic_substring("babad")
print(f"Longest palindrome in 'babad': '{longest}'")
```

## Interactive Menu Features

When you run the script directly, you get a menu-driven interface with:

1. **Number Palindrome Check**: Enter any number to see if it's a palindrome
2. **String Palindrome Check**: Enter text to check if it's a palindrome
3. **Range Search**: Find all palindromes within a number range
4. **Next Palindrome**: Find the next palindromic number
5. **Substring Search**: Find the longest palindromic substring in text
6. **Demo Mode**: See examples with sample data
7. **Exit**: Quit the program

## Special Features

- **Case-insensitive string checking**: "Madam" and "madam" both work
- **Ignores spaces and punctuation**: "A man a plan a canal Panama" is detected as palindrome
- **Handles negative numbers**: Uses absolute value for number palindrome checking
- **Smart display**: Shows results in formatted, easy-to-read layout
- **Error handling**: Validates all user input and provides helpful error messages

## License

This project is open source and available under the MIT License.
