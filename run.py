import subprocess
import sys
import time
import webbrowser
import os
from pathlib import Path

def activate_venv():
    """Activate the virtual environment"""
    if sys.platform == "win32":
        activate_script = Path(".venv/Scripts/activate")
    else:
        activate_script = Path(".venv/bin/activate")
    
    if not activate_script.exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
    
    if sys.platform == "win32":
        return f"& '{activate_script.absolute()}'"
    return f"source {activate_script}"

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

def run_server():
    """Run the FastAPI server"""
    print("Starting the server...")
    return subprocess.Popen(
        f"{sys.executable} -m uvicorn frontend.app:app --host 127.0.0.1 --port 8001 --reload",
        shell=True
    )

def main():
    try:
        # Ensure we're in the correct directory
        os.chdir(Path(__file__).parent)
        
        # Install requirements
        install_requirements()
        
        # Start the server
        server_process = run_server()
        
        # Wait for server to start
        print("Waiting for server to start...")
        time.sleep(3)
        
        # Open browser
        webbrowser.open("http://127.0.0.1:8001")
        
        print("\n✅ Application is running!")
        print("🌐 Web interface: http://127.0.0.1:8001")
        print("\nPress Ctrl+C to stop the server...")
        
        # Keep the script running
        server_process.wait()
        
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup
        print("Cleanup completed")

if __name__ == "__main__":
    main()
