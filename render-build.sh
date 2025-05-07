#!/bin/bash
# render-build.sh

echo "🔧 Installing Python dependencies..."
pip install -r requirements.txt

echo "🎭 Installing Playwright browsers for Python..."
python -m playwright install chromium
