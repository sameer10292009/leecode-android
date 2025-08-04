#!/usr/bin/env python3
"""
Test script for Leecode encoding/decoding functionality
This tests the core logic that will be used in the Android app.
"""

import re

# Mapping dictionary from number strings to characters
number_to_char = {
    '00': 'A', '01': 'B', '02': 'C', '03': 'D', '04': 'E', '05': 'F',
    '06': 'G', '07': 'H', '08': 'I', '09': 'J', '10': 'K', '11': 'L',
    '12': 'M', '13': 'N', '14': 'O', '15': 'P', '16': 'Q', '17': 'R',
    '18': 'S', '19': 'T', '20': 'U', '21': 'V', '22': 'W', '23': 'X',
    '24': 'Y', '25': 'Z', '26': 'a', '27': 'b', '28': 'c', '29': 'd',
    '30': 'e', '31': 'f', '32': 'g', '33': 'h', '34': 'i', '35': 'j',
    '36': 'k', '37': 'l', '38': 'm', '39': 'n', '40': 'o', '41': 'p',
    '42': 'q', '43': 'r', '44': 's', '45': 't', '46': 'u', '47': 'v',
    '48': 'w', '49': 'x', '50': 'y', '51': 'z', '52': '0', '53': '1',
    '54': '2', '55': '3', '56': '4', '57': '5', '58': '6', '59': '7',
    '60': '8', '61': '9', '62': '.', '63': ',', '64': '?', '65': '!',
    '66': ';', '67': ':', '68': "'", '69': '"', '70': '-', '71': '—',
    '72': '(', '73': ')', '74': '[', '75': ']', '76': '{', '77': '}',
    '78': '/', '79': '\\', '80': '|', '81': '@', '82': '#', '83': '$',
    '84': '%', '85': '^', '86': '&', '87': '*', '88': '_', '89': '~',
    '90': '`', '91': '<', '92': '>', '93': '=', '94': ' ', '95': '\t',
    '96': '\n', '97': '\r'
}

# Reverse the dictionary for encoding
char_to_number = {v: k for k, v in number_to_char.items()}

def clean_input(text):
    """Clean input: collapse multiple spaces."""
    text = re.sub(r' +', ' ', text)
    return text

def encode(text):
    """Encode a string using Leecode format."""
    if not text:
        return ""
    
    text = clean_input(text)
    encoded = ''
    for char in text:
        if char in char_to_number:
            encoded += char_to_number[char]
        else:
            raise ValueError(f"Character '{char}' (Unicode: {ord(char)}) not supported in Leecode mapping.")
    return encoded

def decode(code):
    """Decode a Leecode string (must be even-length)."""
    if not code:
        return ""
    
    # Remove any whitespace or non-digit characters
    code = re.sub(r'[^0-9]', '', code)
    
    if len(code) % 2 != 0:
        raise ValueError("Encoded string length must be even (pairs of digits).")
    
    decoded = ''
    for i in range(0, len(code), 2):
        part = code[i:i+2]
        if part in number_to_char:
            decoded += number_to_char[part]
        else:
            raise ValueError(f"Code '{part}' not found in Leecode mapping.")
    return decoded

def test_leecode():
    """Test the Leecode encoding/decoding functionality."""
    print("🔢 Testing Leecode Encoder/Decoder")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        "Hello World!",
        "Python 3.11",
        "Test@123",
        "Special chars: !@#$%^&*()",
        "Numbers: 0123456789",
        "Mixed: ABC123xyz!?.",
        "Single space",
        "Multiple   spaces   here"
    ]
    
    print("Testing encoding and decoding:")
    print()
    
    for i, original in enumerate(test_cases, 1):
        try:
            # Encode
            encoded = encode(original)
            # Decode back
            decoded = decode(encoded)
            
            # Check if round-trip is successful
            success = "✓" if decoded == clean_input(original) else "✗"
            
            print(f"Test {i}: {success}")
            print(f"  Original : '{original}'")
            print(f"  Cleaned  : '{clean_input(original)}'")
            print(f"  Encoded  : {encoded}")
            print(f"  Decoded  : '{decoded}'")
            print(f"  Length   : {len(original)} → {len(encoded)} → {len(decoded)}")
            print()
            
        except Exception as e:
            print(f"Test {i}: ✗ ERROR")
            print(f"  Original: '{original}'")
            print(f"  Error   : {str(e)}")
            print()
    
    # Test edge cases
    print("Testing edge cases:")
    print()
    
    edge_cases = [
        ("", "Empty string"),
        ("A", "Single character"),
        ("  ", "Only spaces"),
        ("\n\t", "Whitespace characters"),
        ("00", "Numbers that look like codes")
    ]
    
    for original, description in edge_cases:
        try:
            encoded = encode(original)
            decoded = decode(encoded)
            success = "✓" if decoded == clean_input(original) else "✗"
            
            print(f"{description}: {success}")
            print(f"  Original: '{repr(original)}'")
            print(f"  Encoded : {encoded}")
            print(f"  Decoded : '{repr(decoded)}'")
            print()
            
        except Exception as e:
            print(f"{description}: ✗ ERROR - {str(e)}")
            print()
    
    # Test character coverage
    print("Character coverage test:")
    print(f"Total supported characters: {len(char_to_number)}")
    print(f"Code range: 00-{max(char_to_number.values())}")
    print()
    
    # Test some manual decode cases
    print("Manual decode tests:")
    manual_tests = [
        ("071430374115408", "Should decode to 'Hello!'"),
        ("0730373340154015940845", "Should decode to 'Hi there'"),
    ]
    
    for code, expected_desc in manual_tests:
        try:
            decoded = decode(code)
            print(f"  Code: {code}")
            print(f"  {expected_desc}")
            print(f"  Result: '{decoded}'")
            print()
        except Exception as e:
            print(f"  Code: {code} - ERROR: {str(e)}")
            print()

if __name__ == "__main__":
    test_leecode()