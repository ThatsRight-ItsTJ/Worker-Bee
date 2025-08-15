#!/usr/bin/env python3
"""
Startup script for OpenOperator UI
Starts both the backend API server and frontend development server
"""

import subprocess
import sys
import os
import time
import signal
from threading import Thread

def start_backend():
    """Start the Flask backend server"""
    print("🚀 Starting OpenOperator API server...")
    try:
        subprocess.run([sys.executable, "backend_server.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
    except Exception as e:
        print(f"❌ Backend server error: {e}")

def start_frontend():
    """Start the Vite frontend development server"""
    print("🎨 Starting OpenOperator UI...")
    try:
        os.chdir("openoperator-ui")
        subprocess.run(["npm", "run", "dev"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except Exception as e:
        print(f"❌ Frontend server error: {e}")

def main():
    """Start both servers"""
    print("🐝 OpenOperator UI Startup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("backend_server.py"):
        print("❌ Please run this script from the Worker-Bee root directory")
        sys.exit(1)
    
    # Check if frontend directory exists
    if not os.path.exists("openoperator-ui"):
        print("❌ Frontend directory not found. Please run the setup first.")
        sys.exit(1)
    
    try:
        # Start backend in a separate thread
        backend_thread = Thread(target=start_backend, daemon=True)
        backend_thread.start()
        
        # Give backend time to start
        time.sleep(3)
        
        # Start frontend (this will block)
        start_frontend()
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down OpenOperator UI...")
        sys.exit(0)

if __name__ == "__main__":
    main()