"""
Palindrome Checker Module

This module contains functions to check if numbers and strings are palindromes.
"""

import math

def is_palindrome_number(number):
    """
    Check if a given number is a palindrome.
    
    Args:
        number (int): The number to check for palindrome
        
    Returns:
        bool: True if the number is a palindrome, False otherwise
        
    Examples:
        >>> is_palindrome_number(121)
        True
        >>> is_palindrome_number(123)
        False
        >>> is_palindrome_number(1221)
        True
        >>> is_palindrome_number(12321)
        True
    """
    # Convert to string and check if it reads the same forwards and backwards
    number_str = str(abs(number))  # Use absolute value to handle negative numbers
    return number_str == number_str[::-1]


def is_palindrome_string(text):
    """
    Check if a given string is a palindrome (ignoring case and spaces).
    
    Args:
        text (str): The string to check for palindrome
        
    Returns:
        bool: True if the string is a palindrome, False otherwise
        
    Examples:
        >>> is_palindrome_string("racecar")
        True
        >>> is_palindrome_string("A man a plan a canal Panama")
        True
        >>> is_palindrome_string("hello")
        False
        >>> is_palindrome_string("Madam")
        True
    """
    # Remove spaces and convert to lowercase for comparison
    cleaned_text = ''.join(text.split()).lower()
    # Remove non-alphanumeric characters
    cleaned_text = ''.join(char for char in cleaned_text if char.isalnum())
    return cleaned_text == cleaned_text[::-1]


def find_palindromes_in_range(start, end):
    """
    Find all palindromic numbers in a given range.
    
    Args:
        start (int): The starting number of the range
        end (int): The ending number of the range
        
    Returns:
        list: A list of all palindromic numbers in the range
        
    Examples:
        >>> find_palindromes_in_range(10, 30)
        [11, 22]
        >>> find_palindromes_in_range(100, 200)
        [101, 111, 121, 131, 141, 151, 161, 171, 181, 191]
    """
    palindromes = []
    for num in range(start, end + 1):
        if is_palindrome_number(num):
            palindromes.append(num)
    return palindromes


def find_next_palindrome(number):
    """
    Find the next palindromic number after a given number.
    
    Args:
        number (int): The number to find the next palindrome after
        
    Returns:
        int: The next palindromic number after the given number
        
    Examples:
        >>> find_next_palindrome(123)
        131
        >>> find_next_palindrome(191)
        202
    """
    candidate = number + 1
    while not is_palindrome_number(candidate):
        candidate += 1
    return candidate


def count_palindromes_in_range(start, end):
    """
    Count the number of palindromic numbers in a given range.
    
    Args:
        start (int): The starting number of the range
        end (int): The ending number of the range
        
    Returns:
        int: The count of palindromic numbers in the range
        
    Examples:
        >>> count_palindromes_in_range(1, 100)
        18
        >>> count_palindromes_in_range(100, 200)
        10
    """
    return len(find_palindromes_in_range(start, end))


def reverse_string(text):
    """
    Reverse a given string.
    
    Args:
        text (str): The string to reverse
        
    Returns:
        str: The reversed string
        
    Examples:
        >>> reverse_string("hello")
        'olleh'
        >>> reverse_string("12345")
        '54321'
    """
    return text[::-1]


def longest_palindromic_substring(text):
    """
    Find the longest palindromic substring in a given text.
    
    Args:
        text (str): The text to search for palindromes
        
    Returns:
        str: The longest palindromic substring
        
    Examples:
        >>> longest_palindromic_substring("babad")
        'bab'
        >>> longest_palindromic_substring("cbbd")
        'bb'
    """
    if not text:
        return ""
    
    longest = ""
    
    for i in range(len(text)):
        # Check for odd-length palindromes (center at i)
        left, right = i, i
        while left >= 0 and right < len(text) and text[left] == text[right]:
            current = text[left:right + 1]
            if len(current) > len(longest):
                longest = current
            left -= 1
            right += 1
        
        # Check for even-length palindromes (center between i and i+1)
        left, right = i, i + 1
        while left >= 0 and right < len(text) and text[left] == text[right]:
            current = text[left:right + 1]
            if len(current) > len(longest):
                longest = current
            left -= 1
            right += 1
    
    return longest


def display_menu():
    """
    Display the main menu options.
    """
    print("\n" + "=" * 50)
    print("           PALINDROME CHECKER")
    print("=" * 50)
    print("Choose an option:")
    print("1. Check if a number is palindrome")
    print("2. Check if a string/phrase is palindrome")
    print("3. Find palindromes in a number range")
    print("4. Find the next palindrome after a number")
    print("5. Find longest palindromic substring")
    print("6. Run demonstration with sample data")
    print("7. Exit")
    print("-" * 50)


def validate_integer(prompt):
    """
    Validate user input to ensure it's an integer.
    
    Args:
        prompt (str): The prompt message to display
        
    Returns:
        int: A valid integer
    """
    while True:
        try:
            value = input(prompt).strip()
            number = int(value)
            return number
        except ValueError:
            print("❌ Invalid input. Please enter a valid integer.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            exit()


def validate_range(prompt_start, prompt_end):
    """
    Validate user input for a range of numbers.
    
    Args:
        prompt_start (str): Prompt for start number
        prompt_end (str): Prompt for end number
        
    Returns:
        tuple: (start, end) as valid integers with start <= end
    """
    while True:
        start = validate_integer(prompt_start)
        end = validate_integer(prompt_end)
        
        if start <= end:
            return start, end
        else:
            print("❌ Start number must be less than or equal to end number.")


def check_number_palindrome():
    """
    Handle option 1: Check if a number is palindrome.
    """
    print("\n� Number Palindrome Checker")
    print("-" * 30)
    
    number = validate_integer("Enter a number to check: ")
    
    if is_palindrome_number(number):
        print(f"✅ {number} is a PALINDROME!")
        print(f"   • It reads the same forwards and backwards")
        if number < 0:
            print(f"   • Note: We checked the absolute value {abs(number)}")
    else:
        print(f"❌ {number} is NOT a palindrome.")
        reversed_num = str(number)[::-1]
        print(f"   • Reversed: {reversed_num}")
        print(f"   • Original: {number}")


def check_string_palindrome():
    """
    Handle option 2: Check if a string/phrase is palindrome.
    """
    print("\n📝 String/Phrase Palindrome Checker")
    print("-" * 35)
    
    text = input("Enter a word or phrase to check: ").strip()
    
    if not text:
        print("❌ Please enter some text.")
        return
    
    if is_palindrome_string(text):
        print(f"✅ '{text}' is a PALINDROME!")
        print(f"   • It reads the same forwards and backwards")
        
        # Show cleaned version if different
        cleaned = ''.join(char for char in text.lower() if char.isalnum())
        if cleaned != text.lower().replace(' ', ''):
            print(f"   • Cleaned text: '{cleaned}'")
    else:
        print(f"❌ '{text}' is NOT a palindrome.")
        reversed_text = text[::-1]
        print(f"   • Reversed: '{reversed_text}'")
        print(f"   • Original: '{text}'")


def find_palindromes_interactive():
    """
    Handle option 3: Find palindromes in a number range.
    """
    print("\n🔍 Find Palindromes in Range")
    print("-" * 30)
    
    start, end = validate_range("Enter start number: ", "Enter end number: ")
    
    palindromes = find_palindromes_in_range(start, end)
    count = len(palindromes)
    
    if count == 0:
        print(f"❌ No palindromes found between {start} and {end}.")
    else:
        print(f"\n✅ Found {count} palindrome(s) between {start} and {end}:")
        
        # Display palindromes in a formatted way
        if count <= 50:  # Show all if not too many
            print("   ", end="")
            for i, palindrome in enumerate(palindromes):
                print(f"{palindrome:6d}", end="")
                if (i + 1) % 8 == 0:  # New line every 8 numbers
                    print("\n   ", end="")
            print()  # Final newline
        else:  # Show first 20 and last 10 if too many
            print("   First 20 palindromes:")
            print("   ", end="")
            for i in range(20):
                print(f"{palindromes[i]:6d}", end="")
                if (i + 1) % 8 == 0:
                    print("\n   ", end="")
            print("\n   ...")
            print("   Last 10 palindromes:")
            print("   ", end="")
            for palindrome in palindromes[-10:]:
                print(f"{palindrome:6d}", end="")
            print()
        
        # Show percentage
        total_numbers = end - start + 1
        percentage = (count / total_numbers) * 100
        print(f"   That's {percentage:.2f}% of all numbers in the range.")


def find_next_palindrome_interactive():
    """
    Handle option 4: Find the next palindrome after a number.
    """
    print("\n⏭️  Find Next Palindrome")
    print("-" * 25)
    
    number = validate_integer("Enter a number: ")
    
    next_palindrome = find_next_palindrome(number)
    
    print(f"✅ The next palindrome after {number} is {next_palindrome}.")
    
    gap = next_palindrome - number
    print(f"   Gap: {gap}")


def find_longest_palindrome_interactive():
    """
    Handle option 5: Find longest palindromic substring.
    """
    print("\n🔤 Find Longest Palindromic Substring")
    print("-" * 35)
    
    text = input("Enter text to search: ").strip()
    
    if not text:
        print("❌ Please enter some text.")
        return
    
    longest = longest_palindromic_substring(text)
    
    if longest:
        print(f"✅ Longest palindromic substring: '{longest}'")
        print(f"   Length: {len(longest)} character(s)")
        
        # Show position in original text
        pos = text.find(longest)
        if pos != -1:
            print(f"   Position: starts at index {pos}")
    else:
        print("❌ No palindromic substring found.")


def run_demonstration():
    """
    Handle option 6: Run demonstration with sample data.
    """
    print("\n🧪 Demonstration Mode")
    print("-" * 20)
    
    # Test palindromic numbers
    test_numbers = [121, 123, 1221, 12321, 111, 1001, 7337, 9009]
    print("\n📋 Testing sample numbers:")
    for num in test_numbers:
        result = is_palindrome_number(num)
        status = "✅ PALINDROME" if result else "❌ NOT PALINDROME"
        print(f"   {num:5d} → {status}")
    
    # Test palindromic strings
    test_strings = ["racecar", "hello", "madam", "A man a plan a canal Panama", "Was it a car or a cat I saw?"]
    print("\n📝 Testing sample strings:")
    for text in test_strings:
        result = is_palindrome_string(text)
        status = "✅ PALINDROME" if result else "❌ NOT PALINDROME"
        print(f"   '{text[:20]}{'...' if len(text) > 20 else ''}' → {status}")
    
    # Find palindromes in range
    start, end = 100, 200
    palindromes = find_palindromes_in_range(start, end)
    print(f"\n🔍 Palindromes between {start} and {end}:")
    print(f"   {palindromes}")
    
    # Count palindromes
    count = count_palindromes_in_range(1, 1000)
    print(f"\n🔢 Number of palindromes from 1 to 1000: {count}")
    
    # Find next palindrome
    number = 150
    next_palindrome = find_next_palindrome(number)
    print(f"\n⏭️  Next palindrome after {number}: {next_palindrome}")
    
    # Longest palindromic substring
    sample_text = "babad"
    longest = longest_palindromic_substring(sample_text)
    print(f"\n🔤 Longest palindrome in '{sample_text}': '{longest}'")


def main():
    """
    Main function with menu-driven interface.
    """
    print("🎯 Welcome to the Palindrome Checker!")
    
    while True:
        try:
            display_menu()
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == '1':
                check_number_palindrome()
            elif choice == '2':
                check_string_palindrome()
            elif choice == '3':
                find_palindromes_interactive()
            elif choice == '4':
                find_next_palindrome_interactive()
            elif choice == '5':
                find_longest_palindrome_interactive()
            elif choice == '6':
                run_demonstration()
            elif choice == '7':
                print("\n👋 Thank you for using Palindrome Checker!")
                print("   Goodbye! 🚀")
                break
            else:
                print("❌ Invalid choice. Please enter a number between 1 and 7.")
                
            # Ask if user wants to continue
            if choice in ['1', '2', '3', '4', '5', '6']:
                input("\nPress Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using Palindrome Checker! 🚀")
            break
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
