#!/bin/bash
# Quick start script for Role Matrix application

echo "🚀 Starting Role Matrix Application..."
echo ""

# Navigate to the app directory
cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "✅ Virtual environment found"
fi

# Run the application
echo "🌐 Launching Streamlit app..."
echo ""
echo "The app will open in your browser at http://localhost:8501"
echo "Press Ctrl+C to stop the application"
echo ""

venv/bin/streamlit run app.py
