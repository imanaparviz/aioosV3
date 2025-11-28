#!/bin/bash

# AIOOS Backend Setup Script
# This script sets up the backend server and installs all dependencies

set -e  # Exit on error

echo "================================================"
echo "🚀 AIOOS Backend Setup"
echo "================================================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.9 or higher.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python 3 found: $(python3 --version)${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
source venv/bin/activate || . venv/Scripts/activate

# Upgrade pip
echo -e "${YELLOW}📦 Upgrading pip...${NC}"
pip install --upgrade pip

# Install backend requirements
echo -e "${YELLOW}📦 Installing backend dependencies...${NC}"
pip install -r requirements.txt

# Install LiveKit agents from parent directory
echo -e "${YELLOW}📦 Installing LiveKit agents...${NC}"
cd ..
pip install -e ./livekit-agents
pip install -e ./livekit-plugins/livekit-plugins-azure
pip install -e ./livekit-plugins/livekit-plugins-openai
pip install -e ./livekit-plugins/livekit-plugins-deepgram
pip install -e ./livekit-plugins/livekit-plugins-silero
cd backend

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    echo -e "${YELLOW}📝 Copying .env.example to .env${NC}"
    cp .env.example .env
    echo -e "${RED}❗ IMPORTANT: Edit .env file and add your API keys!${NC}"
else
    echo -e "${GREEN}✅ .env file exists${NC}"
fi

echo ""
echo "================================================"
echo -e "${GREEN}✅ Backend setup complete!${NC}"
echo "================================================"
echo ""
echo "📝 Next steps:"
echo "  1. Edit backend/.env and add your API keys"
echo "  2. Run: source venv/bin/activate (or . venv/Scripts/activate on Windows)"
echo "  3. Run: python main.py"
echo ""
echo "🌐 Server will run at: http://localhost:8000"
echo "📚 API docs: http://localhost:8000/docs"
echo ""
