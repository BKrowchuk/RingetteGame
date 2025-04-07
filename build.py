import os
import subprocess
import sys

def build_executable():
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    print("Building executable...")
    # Get the absolute path to the assets directory
    assets_path = os.path.abspath("assets")
    
    subprocess.check_call([
        sys.executable,
        "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "RingetteGame",
        "--add-data", f"{assets_path};assets",  # Use absolute path for assets
        "--collect-all", "assets",  # Ensure all assets are collected
        "main.py"
    ])
    
    print("\nBuild complete! Executable is in the 'dist' directory.")

if __name__ == "__main__":
    build_executable() 