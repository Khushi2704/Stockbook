"""
Build script to create standalone executable
"""
import os
import shutil
import PyInstaller.__main__
import sys


def build_executable():
    """Build standalone executable using PyInstaller"""
    
    print("Building Stockbook Medical Store Application...")
    print("=" * 60)
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # PyInstaller arguments
    args = [
        "main.py",
        "--onefile",  # Create single executable
        "--windowed",  # No console window
        "--name=Stockbook",  # Output name
        "--icon=assets/icon.ico" if os.path.exists(os.path.join(script_dir, "assets/icon.ico")) else "",
        "--clean",
        "--noupx",
    ]
    
    # Filter out empty strings
    args = [arg for arg in args if arg]
    
    # Add path
    os.chdir(script_dir)
    
    try:
        print(f"Working directory: {os.getcwd()}")
        print(f"Building with arguments: {args}")
        print("=" * 60)
        
        # Run PyInstaller
        PyInstaller.__main__.run(args)
        
        print("=" * 60)
        print("✓ Build successful!")
        print(f"✓ Executable created in: {os.path.join(script_dir, 'dist', 'Stockbook.exe')}")
        print("\nNext steps:")
        print("1. Run the executable: dist\\Stockbook.exe")
        print("2. Login with admin/admin123")
        print("3. Add medicines and start billing")
        
    except Exception as e:
        print("=" * 60)
        print(f"✗ Build failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_executable()
