#!/bin/bash

# Quick Start Script for Smart Resume Screener
# This script sets up and runs both backend and frontend

set -e  # Exit on error

echo "[▶] Smart Resume Screener - Quick Start"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo -e "${RED}[✗] Error: Please run this script from the project root directory${NC}"
    exit 1
fi

echo "[📦] Step 1: Setting up Backend..."
echo "--------------------------------"

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${RED}[✗] Error: .env file not found in backend/${NC}"
    echo "Please create backend/.env with your credentials"
    exit 1
fi

# Seed user if needed
echo "Setting up demo user..."
python scripts/seed_user.py 2>&1 | grep -E "\[✓\]|\[!\]" || true

echo -e "${GREEN}[✓] Backend setup complete!${NC}"
echo ""

cd ..

echo "[📦] Step 2: Setting up Frontend..."
echo "--------------------------------"

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies (this may take a few minutes)..."
    npm install > /dev/null 2>&1
fi

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo -e "${RED}[✗] Error: .env.local file not found in frontend/${NC}"
    echo "Please create frontend/.env.local with NEXT_PUBLIC_API_URL"
    exit 1
fi

echo -e "${GREEN}[✓] Frontend setup complete!${NC}"
echo ""

cd ..

echo "[🎉] Setup Complete!"
echo "=================="
echo ""
echo -e "${YELLOW}To start the application:${NC}"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo -e "${GREEN}Then visit: http://localhost:3000${NC}"
echo ""
echo "Demo credentials:"
echo "  Email: admin@resumescreener.com"
echo "  Password: admin123"
echo ""
echo "[📚] For detailed documentation, see PROJECT_SETUP.md"
