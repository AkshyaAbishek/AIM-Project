<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Palindrome Checker Project

This project contains Python functions for checking palindromes in numbers and strings.

## Code Style Guidelines
- Use clear, descriptive function and variable names
- Include comprehensive docstrings with examples
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write efficient string and number manipulation algorithms

## Palindrome Context
- When working with palindrome algorithms, consider both number and string palindromes
- For strings, handle case-insensitivity and ignore spaces/punctuation when appropriate
- Use string slicing ([::-1]) for efficient reversal operations
- Handle edge cases like empty strings, single characters, and negative numbers

## Testing
- Include doctest examples in function docstrings
- Test edge cases like empty strings, single digits, negative numbers
- Verify correctness of palindrome detection algorithms
- Test both number palindromes (121, 1221) and string palindromes ("racecar", "A man a plan a canal Panama")
