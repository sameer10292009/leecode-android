# Leecode Encoder/Decoder

## Overview

This is a multi-platform Leecode encoding/decoding system that converts text characters to two-digit numeric codes and vice versa. The system uses a predefined mapping covering 98 characters including uppercase letters, lowercase letters, numbers, punctuation marks, and whitespace characters. Multiple application formats are available:

1. **Streamlit Web Application**: Browser-based interface for online use
2. **Android APK**: Mobile application built with Kivy framework for offline use
3. **Desktop Application**: Tkinter-based standalone application for offline use

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web framework for rapid prototyping and deployment
- **Interface Design**: Single-page application with text input/output areas
- **User Interaction**: Real-time encoding/decoding with copy-to-clipboard functionality

### Core Application Logic
- **Encoding System**: Bidirectional character-to-number mapping using a comprehensive dictionary
- **Character Support**: 98 total characters including:
  - Uppercase letters (A-Z): codes 00-25
  - Lowercase letters (a-z): codes 26-51
  - Numbers (0-9): codes 52-61
  - Punctuation and symbols: codes 62-93
  - Whitespace characters (space, tab, newline, carriage return): codes 94-97
- **Input Processing**: Text cleaning with multiple space collapse functionality
- **Error Handling**: Character validation with descriptive error messages for unsupported characters

### Data Processing
- **Encoding Logic**: Character-by-character conversion to two-digit codes
- **Decoding Logic**: Pairs of digits converted back to characters (requires even-length input)
- **Validation**: Input sanitization and character support verification

## Application Versions

### 1. Streamlit Web Application (app.py)
- Browser-based interface with tabbed navigation
- Real-time encoding/decoding with copy functionality
- Character reference table
- Requires internet connection for deployment

### 2. Android APK Application (main.py)
- Kivy-based mobile application
- Touch-optimized interface for mobile devices
- Offline functionality with clipboard integration
- Built using Buildozer for Android deployment
- Minimum Android 5.0 (API 21), Target Android 13 (API 33)

### 3. Desktop Application (leecode_desktop.py)
- Tkinter-based standalone application
- Cross-platform compatibility (Windows, macOS, Linux)
- Offline functionality with system clipboard integration
- No installation required, runs directly with Python

## External Dependencies

### Python Libraries
- **streamlit**: Web application framework for the web interface
- **kivy**: Mobile application framework for Android APK
- **buildozer**: Android APK build tool
- **tkinter**: Desktop GUI framework (built-in with Python)
- **re**: Regular expression module for text cleaning and pattern matching
- **pyperclip**: Clipboard integration for copy-to-clipboard functionality

### Build Tools
- **Buildozer**: For creating Android APK files
- **Android SDK/NDK**: Required for Android development (auto-downloaded by Buildozer)
- **Java JDK 11**: Required for Android APK compilation

### Runtime Requirements
- **Web Version**: Python environment with Streamlit, web browser
- **Android Version**: Android 5.0+ device, no internet required after installation
- **Desktop Version**: Python 3.8+ with tkinter, no internet required
- No database or persistent storage requirements
- No external API integrations