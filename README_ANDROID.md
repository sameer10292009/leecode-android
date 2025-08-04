# Leecode Encoder/Decoder Android App

This is the Android APK version of the Leecode Encoder/Decoder application built with Kivy and packaged using Buildozer.

## Features

- **Text Encoding**: Convert text to Leecode numeric format
- **Text Decoding**: Convert Leecode numbers back to readable text
- **Character Reference**: Complete mapping table of all supported characters
- **Clipboard Support**: Copy results directly to your device clipboard
- **Offline Operation**: Works completely offline without internet connection
- **Mobile Optimized**: Touch-friendly interface designed for mobile devices

## Supported Characters

The app supports 98 characters including:
- Uppercase letters (A-Z): codes 00-25
- Lowercase letters (a-z): codes 26-51
- Numbers (0-9): codes 52-61
- Punctuation and symbols: codes 62-93
- Whitespace characters: codes 94-97

## Building the APK

### Prerequisites

1. **Install Python 3.8+**
2. **Install Buildozer**:
   ```bash
   pip install buildozer
   ```

3. **Install Java Development Kit (JDK 11)**
4. **Install Android SDK and NDK** (Buildozer can auto-download these)

### Build Instructions

1. **Clone or download this project**

2. **Navigate to the project directory**:
   ```bash
   cd leecode-android
   ```

3. **Initialize Buildozer** (first time only):
   ```bash
   buildozer android debug
   ```

4. **Build the APK**:
   ```bash
   buildozer android debug
   ```

   The APK will be created in the `bin/` directory.

5. **For release build** (signed APK):
   ```bash
   buildozer android release
   ```

### Installation

1. **Enable Unknown Sources** on your Android device:
   - Go to Settings > Security
   - Enable "Unknown sources" or "Install unknown apps"

2. **Transfer the APK** to your device

3. **Install the APK** by tapping on it

## Usage

### Encoding Text
1. Open the app and go to the "Encoder" tab
2. Type or paste your text in the input field
3. Tap "Encode Text"
4. The encoded result appears below
5. Tap "Copy Result" to copy to clipboard

### Decoding Leecode
1. Go to the "Decoder" tab
2. Enter the numeric Leecode in the input field
3. Tap "Decode Leecode"
4. The decoded text appears below
5. Tap "Copy Result" to copy to clipboard

### Character Reference
- Go to the "Reference" tab to see the complete character-to-code mapping

## App Structure

```
leecode-android/
├── main.py              # Main Kivy application
├── buildozer.spec       # Buildozer configuration
├── README_ANDROID.md    # This file
└── bin/                 # Generated APK files (after build)
```

## Technical Details

- **Framework**: Kivy (Python-based mobile framework)
- **Minimum Android Version**: Android 5.0 (API 21)
- **Target Android Version**: Android 13 (API 33)
- **Architecture Support**: ARM64-v8a, ARMv7a
- **Package Size**: ~10-15 MB
- **Permissions**: None required (runs completely offline)

## Troubleshooting

### Build Issues

1. **Java/SDK Issues**:
   - Ensure JDK 11 is installed and in PATH
   - Let Buildozer auto-download Android SDK/NDK

2. **Permission Errors**:
   - Run with proper permissions
   - On Linux/Mac: `sudo buildozer android debug`

3. **Dependencies**:
   - Install system dependencies:
     ```bash
     # Ubuntu/Debian
     sudo apt update
     sudo apt install -y git zip unzip openjdk-11-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
     
     # Arch Linux
     sudo pacman -S jdk11-openjdk python-pip autoconf automake
     ```

### Runtime Issues

1. **App Crashes**:
   - Check Android logs: `adb logcat`
   - Ensure all characters are supported in Leecode mapping

2. **Clipboard Not Working**:
   - App will show popup messages
   - Manually select and copy text if needed

## Development

To modify the app:

1. **Edit main.py** for application logic
2. **Edit buildozer.spec** for build configuration
3. **Rebuild**: `buildozer android debug`

## Version History

- **v1.0**: Initial release with encoding/decoding functionality

## License

This project is part of the Leecode Encoder/Decoder suite.