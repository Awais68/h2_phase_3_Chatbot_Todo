#!/bin/bash

# Backend Management Script
# Location: backend/hf_deployment/manage_backend.sh

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BACKEND_DIR="/media/awais/6372445e-8fda-42fa-9034-61babd7dafd1/150 GB DATA TRANSFER/hackathon series/hackathon-2/phase-3 chatbot_todo/backend/hf_deployment"

case "$1" in
    start)
        echo -e "${GREEN}Starting Backend Server...${NC}"
        cd "$BACKEND_DIR"
        echo -e "${BLUE}Backend will run on http://localhost:8000${NC}"
        echo -e "${BLUE}API Docs: http://localhost:8000/docs${NC}"
        uvicorn app:app --host 0.0.0.0 --port 8000 --reload
        ;;
    
    stop)
        echo -e "${YELLOW}Stopping Backend Server...${NC}"
        # Find and kill all uvicorn processes running on port 8000
        PID=$(lsof -ti:8000)
        if [ -z "$PID" ]; then
            echo -e "${RED}No backend process found on port 8000${NC}"
        else
            kill -9 $PID
            echo -e "${GREEN}Backend stopped (PID: $PID)${NC}"
        fi
        ;;
    
    restart)
        echo -e "${YELLOW}Restarting Backend Server...${NC}"
        $0 stop
        sleep 2
        $0 start
        ;;
    
    status)
        echo -e "${BLUE}Checking Backend Status...${NC}"
        PID=$(lsof -ti:8000)
        if [ -z "$PID" ]; then
            echo -e "${RED}Backend is NOT running${NC}"
        else
            echo -e "${GREEN}Backend is running (PID: $PID)${NC}"
            echo -e "${BLUE}Port: 8000${NC}"
            echo -e "${BLUE}URL: http://localhost:8000${NC}"
            echo -e "${BLUE}Docs: http://localhost:8000/docs${NC}"
        fi
        ;;
    
    logs)
        echo -e "${BLUE}Showing Backend Logs...${NC}"
        if [ -f "$BACKEND_DIR/backend.log" ]; then
            tail -f "$BACKEND_DIR/backend.log"
        else
            echo -e "${RED}No log file found${NC}"
        fi
        ;;
    
    *)
        echo -e "${BLUE}Backend Management Script${NC}"
        echo ""
        echo "Usage: $0 {start|stop|restart|status|logs}"
        echo ""
        echo "Commands:"
        echo -e "  ${GREEN}start${NC}    - Start the backend server"
        echo -e "  ${YELLOW}stop${NC}     - Stop the backend server"
        echo -e "  ${YELLOW}restart${NC}  - Restart the backend server"
        echo -e "  ${BLUE}status${NC}   - Check if backend is running"
        echo -e "  ${BLUE}logs${NC}     - Show backend logs (tail -f)"
        echo ""
        echo "Examples:"
        echo "  $0 start"
        echo "  $0 stop"
        echo "  $0 restart"
        exit 1
        ;;
esac
