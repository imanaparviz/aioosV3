#!/bin/bash

# AIOOS Platform - Easy Startup Script
# This script runs both backend and frontend in separate terminals

set -e

echo "================================================"
echo "🚀 Starting AIOOS Voice AI Platform"
echo "================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if backend is set up
if [ ! -d "$SCRIPT_DIR/v4liveKit/backend/venv" ]; then
    echo -e "${YELLOW}⚠️  Backend not set up yet!${NC}"
    echo -e "${YELLOW}📝 Running backend setup...${NC}"
    cd "$SCRIPT_DIR/v4liveKit/backend"
    chmod +x setup.sh
    ./setup.sh
    cd "$SCRIPT_DIR"
fi

# Check if frontend deps installed
if [ ! -d "$SCRIPT_DIR/v4liveKit-frontend/node_modules" ]; then
    echo -e "${YELLOW}⚠️  Frontend not set up yet!${NC}"
    echo -e "${YELLOW}📦 Installing frontend dependencies...${NC}"
    cd "$SCRIPT_DIR/v4liveKit-frontend"
    npm install
    cd "$SCRIPT_DIR"
fi

echo -e "${GREEN}✅ All dependencies ready!${NC}"
echo ""

# Function to start backend
start_backend() {
    echo -e "${BLUE}🔧 Starting Backend Server...${NC}"
    cd "$SCRIPT_DIR/v4liveKit/backend"

    # Activate virtual environment
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    elif [ -f "venv/Scripts/activate" ]; then
        . venv/Scripts/activate
    fi

    # Start backend
    python main.py
}

# Function to start frontend
start_frontend() {
    echo -e "${BLUE}🎨 Starting Frontend Server...${NC}"
    cd "$SCRIPT_DIR/v4liveKit-frontend"
    npm run dev
}

# Check if we're on Windows (WSL)
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]] || grep -qi microsoft /proc/version 2>/dev/null; then
    echo -e "${YELLOW}🪟 Detected Windows/WSL environment${NC}"
    echo -e "${YELLOW}📝 Please run these commands in separate terminals:${NC}"
    echo ""
    echo -e "${GREEN}Terminal 1 (Backend):${NC}"
    echo "  cd v4liveKit/backend"
    echo "  source venv/bin/activate"
    echo "  python main.py"
    echo ""
    echo -e "${GREEN}Terminal 2 (Frontend):${NC}"
    echo "  cd v4liveKit-frontend"
    echo "  npm run dev"
    echo ""
    echo -e "${BLUE}Or run backend now and frontend manually:${NC}"
    read -p "Start backend? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        start_backend
    fi
else
    # On Linux/Mac, we can use tmux or gnome-terminal
    if command -v tmux &> /dev/null; then
        echo -e "${GREEN}✅ Using tmux to run both servers${NC}"

        # Create new tmux session
        tmux new-session -d -s aioos

        # Split window
        tmux split-window -h

        # Run backend in first pane
        tmux send-keys -t aioos:0.0 "cd $SCRIPT_DIR/v4liveKit/backend && source venv/bin/activate && python main.py" C-m

        # Run frontend in second pane
        tmux send-keys -t aioos:0.1 "cd $SCRIPT_DIR/v4liveKit-frontend && npm run dev" C-m

        # Attach to session
        echo -e "${GREEN}✅ Servers starting in tmux session 'aioos'${NC}"
        echo -e "${YELLOW}📝 Use Ctrl+B then D to detach${NC}"
        echo -e "${YELLOW}📝 Use 'tmux attach -t aioos' to reattach${NC}"
        echo -e "${YELLOW}📝 Use 'tmux kill-session -t aioos' to stop${NC}"
        sleep 2
        tmux attach -t aioos
    else
        echo -e "${YELLOW}📝 Please run these commands in separate terminals:${NC}"
        echo ""
        echo -e "${GREEN}Terminal 1 (Backend):${NC}"
        echo "  cd v4liveKit/backend"
        echo "  source venv/bin/activate"
        echo "  python main.py"
        echo ""
        echo -e "${GREEN}Terminal 2 (Frontend):${NC}"
        echo "  cd v4liveKit-frontend"
        echo "  npm run dev"
        echo ""
        read -p "Start backend now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            start_backend
        fi
    fi
fi
