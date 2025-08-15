#!/bin/bash
# Quick setup script for Linux systems

echo "🐧 Worker-Bee Linux Setup"
echo "========================="

# Install Python dependencies
echo "📦 Installing Python dependencies..."
python -m pip install -r requirements.txt

# Install Playwright browsers
echo "🎭 Installing Playwright browsers..."
python -m playwright install

# Install system dependencies for Linux
echo "🔧 Installing system dependencies..."
echo "This requires sudo access to install system packages."
read -p "Install system dependencies? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo apt-get update
    sudo apt-get install -y libavif16 libnss3 libatk-bridge2.0-0 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libxss1 libasound2
    echo "✅ System dependencies installed"
else
    echo "⏭️  Skipped system dependencies"
    echo "💡 If you get browser errors, run:"
    echo "   sudo apt-get install libavif16 libnss3 libatk-bridge2.0-0 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libxss1 libasound2"
fi

echo ""
echo "🎉 Setup completed!"
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env"
echo "2. Configure your AI model settings in .env"
echo "3. Run: python test_basic_automation.py"