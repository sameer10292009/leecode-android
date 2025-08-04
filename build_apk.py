#!/usr/bin/env python3
"""
APK Build Script for Leecode Encoder/Decoder
This script helps build the Android APK using Buildozer.
"""

import os
import sys
import subprocess
import platform

def check_requirements():
    """Check if required tools are installed."""
    print("Checking build requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Check if buildozer is installed
    try:
        result = subprocess.run(['buildozer', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Buildozer installed")
        else:
            print("❌ Buildozer not working properly")
            return False
    except FileNotFoundError:
        print("❌ Buildozer not installed. Install with: pip install buildozer")
        return False
    
    # Check if we're on a supported platform
    if platform.system() not in ['Linux', 'Darwin']:  # Linux or macOS
        print("⚠️  Warning: Buildozer works best on Linux or macOS")
    
    return True

def install_system_dependencies():
    """Install system dependencies for building Android APKs."""
    print("\nInstalling system dependencies...")
    
    system = platform.system()
    
    if system == 'Linux':
        # Check if running on Ubuntu/Debian
        try:
            subprocess.run(['which', 'apt'], check=True, capture_output=True)
            print("Installing Ubuntu/Debian dependencies...")
            deps = [
                'git', 'zip', 'unzip', 'openjdk-11-jdk', 'python3-pip',
                'autoconf', 'libtool', 'pkg-config', 'zlib1g-dev',
                'libncurses5-dev', 'libncursesw5-dev', 'libtinfo5',
                'cmake', 'libffi-dev', 'libssl-dev', 'build-essential',
                'ccache', 'libsdl2-dev', 'libsdl2-image-dev',
                'libsdl2-mixer-dev', 'libsdl2-ttf-dev'
            ]
            cmd = ['sudo', 'apt', 'update', '&&', 'sudo', 'apt', 'install', '-y'] + deps
            print(f"Run: {' '.join(cmd)}")
            
        except subprocess.CalledProcessError:
            print("⚠️  Please install dependencies manually for your Linux distribution")
            
    elif system == 'Darwin':  # macOS
        print("For macOS, ensure you have:")
        print("- Xcode Command Line Tools: xcode-select --install")
        print("- Java 11: brew install openjdk@11")
        print("- Git: brew install git")
        
    else:
        print("⚠️  Windows is not officially supported for Buildozer")
        print("Consider using WSL (Windows Subsystem for Linux)")

def build_apk(build_type='debug'):
    """Build the APK using Buildozer."""
    print(f"\nBuilding {build_type} APK...")
    
    if not os.path.exists('buildozer.spec'):
        print("❌ buildozer.spec not found in current directory")
        return False
    
    if not os.path.exists('main.py'):
        print("❌ main.py not found in current directory")
        return False
    
    try:
        # First, initialize buildozer (downloads Android SDK/NDK if needed)
        print("Initializing Buildozer (this may take a while for first build)...")
        cmd = ['buildozer', 'android', build_type]
        
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd='.', text=True)
        
        if result.returncode == 0:
            print(f"\n✅ {build_type.capitalize()} APK built successfully!")
            
            # Find the generated APK
            bin_dir = os.path.join('.', 'bin')
            if os.path.exists(bin_dir):
                apk_files = [f for f in os.listdir(bin_dir) if f.endswith('.apk')]
                if apk_files:
                    print(f"📱 APK location: {os.path.join(bin_dir, apk_files[0])}")
                    print(f"📱 APK size: {get_file_size(os.path.join(bin_dir, apk_files[0]))}")
                else:
                    print("⚠️  APK file not found in bin directory")
            
            return True
        else:
            print(f"❌ Build failed with exit code {result.returncode}")
            return False
            
    except KeyboardInterrupt:
        print("\n⚠️  Build interrupted by user")
        return False
    except Exception as e:
        print(f"❌ Build error: {str(e)}")
        return False

def get_file_size(filepath):
    """Get human-readable file size."""
    if not os.path.exists(filepath):
        return "Unknown"
    
    size = os.path.getsize(filepath)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

def clean_build():
    """Clean previous build artifacts."""
    print("Cleaning previous build artifacts...")
    
    dirs_to_clean = ['.buildozer', 'bin']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Removing {dir_name}/")
            try:
                subprocess.run(['rm', '-rf', dir_name], check=True)
                print(f"✅ Cleaned {dir_name}/")
            except subprocess.CalledProcessError:
                print(f"⚠️  Could not remove {dir_name}/")

def main():
    """Main function."""
    print("🔢 Leecode Encoder/Decoder - APK Builder")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'check':
            if check_requirements():
                print("\n✅ All requirements satisfied!")
            else:
                print("\n❌ Some requirements missing")
                sys.exit(1)
                
        elif command == 'deps':
            install_system_dependencies()
            
        elif command == 'clean':
            clean_build()
            
        elif command == 'debug':
            if check_requirements():
                build_apk('debug')
            else:
                print("❌ Requirements check failed")
                sys.exit(1)
                
        elif command == 'release':
            if check_requirements():
                build_apk('release')
            else:
                print("❌ Requirements check failed")
                sys.exit(1)
                
        else:
            print(f"Unknown command: {command}")
            print_usage()
            
    else:
        print_usage()

def print_usage():
    """Print usage instructions."""
    print("\nUsage:")
    print("  python build_apk.py check     - Check build requirements")
    print("  python build_apk.py deps      - Show system dependencies info")
    print("  python build_apk.py clean     - Clean build artifacts")
    print("  python build_apk.py debug     - Build debug APK")
    print("  python build_apk.py release   - Build release APK")
    print("\nExample workflow:")
    print("  1. python build_apk.py check")
    print("  2. python build_apk.py deps")
    print("  3. python build_apk.py debug")

if __name__ == '__main__':
    main()