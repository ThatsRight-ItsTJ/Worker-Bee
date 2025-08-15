#!/usr/bin/env python3
"""
Setup script to install Playwright browsers and dependencies
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🎭 Setting up Playwright for OpenOperator")
    print("=" * 50)
    
    # Check if playwright is installed
    try:
        from playwright import __version__ as playwright_version
        print(f"✅ Playwright {playwright_version} is installed")
    except ImportError:
        print("❌ Playwright not found. Please install requirements first:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Install browsers
    success = run_command("playwright install", "Installing Playwright browsers")
    
    if not success:
        print("\n💡 If installation failed, try:")
        print("   pip install --upgrade playwright")
        print("   playwright install")
        sys.exit(1)
    
    # Check if we're on Linux and need dependencies
    if sys.platform.startswith('linux'):
        print("\n🐧 Linux detected - checking system dependencies...")
        
        # Try to install system dependencies
        print("💡 You may need to install system dependencies:")
        print("   sudo playwright install-deps")
        print("   OR: sudo apt-get install libavif16")
        
        # Ask user if they want to try installing deps
        try:
            response = input("\nTry to install system dependencies now? (y/N): ").strip().lower()
            if response in ['y', 'yes']:
                success = run_command("python -m playwright install-deps", "Installing system dependencies")
                if not success:
                    print("⚠️  System dependency installation failed. You may need to run manually:")
                    print("   sudo apt-get install libavif16 libnss3 libatk-bridge2.0-0 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libxss1 libasound2")
        except KeyboardInterrupt:
            print("\n⏭️  Skipping system dependencies installation")
    
    print("\n🎉 Playwright setup completed!")
    print("\nNext steps:")
    print("1. Copy .env.example to .env")
    print("2. Configure your AI model settings in .env")
    print("3. Run: python test_basic_automation.py")

if __name__ == "__main__":
    main()