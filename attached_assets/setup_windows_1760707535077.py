"""
Windows Setup Helper
Handles Windows-specific configuration and setup
"""

import sys
import subprocess
import os
import platform
from pathlib import Path


def check_windows():
    """Check if running on Windows"""
    return platform.system() == "Windows"


def install_ffmpeg_windows():
    """Helper function to install FFmpeg on Windows"""
    try:
        # Check if FFmpeg is already installed
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    print("\n" + "="*70)
    print("FFmpeg Not Found!")
    print("="*70)
    print("\nFFmpeg is required for audio processing.")
    print("\nOptions to install FFmpeg:")
    print("\n1. Using Chocolatey (if installed):")
    print("   choco install ffmpeg -y")
    print("\n2. Using Winget (Windows 10.1+):")
    print("   winget install FFmpeg.FFmpeg")
    print("\n3. Manual Download:")
    print("   https://ffmpeg.org/download.html")
    print("   Extract to C:\\ffmpeg and add to PATH")
    print("\n" + "="*70)
    
    response = input("\nInstall FFmpeg now? (requires admin privileges) [y/N]: ").lower()
    
    if response == 'y':
        try:
            # Try Chocolatey first
            subprocess.run(
                ["choco", "install", "ffmpeg", "-y"],
                check=True
            )
            print("✓ FFmpeg installed successfully!")
            return True
        except FileNotFoundError:
            try:
                # Try Winget
                subprocess.run(
                    ["winget", "install", "FFmpeg.FFmpeg"],
                    check=True
                )
                print("✓ FFmpeg installed successfully!")
                return True
            except FileNotFoundError:
                print("✗ Neither Chocolatey nor Winget found.")
                print("Please install FFmpeg manually from: https://ffmpeg.org/download.html")
                return False
    
    return False


def setup_windows_environment():
    """Setup Windows-specific environment"""
    if not check_windows():
        return True
    
    print("\n" + "="*70)
    print("🪟 Windows Setup Checker")
    print("="*70)
    
    # Check FFmpeg
    print("\n[1/3] Checking FFmpeg...")
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✓ FFmpeg found")
        else:
            print("✗ FFmpeg not found")
            install_ffmpeg_windows()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("✗ FFmpeg not found")
        install_ffmpeg_windows()
    
    # Check Python version
    print("\n[2/3] Checking Python version...")
    if sys.version_info >= (3, 8):
        print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}")
    else:
        print("✗ Python 3.8+ required")
        return False
    
    # Create required directories
    print("\n[3/3] Creating required directories...")
    base_dir = Path(__file__).parent
    
    directories = [
        base_dir / "downloads",
        base_dir / "cache",
        base_dir / "temp",
        base_dir / "logs",
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ {directory.name}/")
    
    print("\n" + "="*70)
    print("✓ Setup completed!")
    print("="*70)
    return True


if __name__ == "__main__":
    setup_windows_environment()
