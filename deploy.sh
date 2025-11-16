#!/bin/bash

# OpenSpace Production Deployment Script
# This script helps deploy the application on university server

set -e

echo "========================================="
echo "🚀 OpenSpace Production Deployment"
echo "========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if .env.prod exists
if [ ! -f .env.prod ]; then
    echo -e "${RED}❌ Error: .env.prod file not found!${NC}"
    echo "Please create .env.prod file with your production settings."
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed!${NC}"
    echo "Please install Docker first:"
    echo "  curl -fsSL https://get.docker.com -o get-docker.sh"
    echo "  sudo sh get-docker.sh"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed!${NC}"
    echo "Please install Docker Compose first:"
    echo "  sudo apt install docker-compose -y"
    exit 1
fi

echo -e "${BLUE}📋 Pre-deployment checks...${NC}"
echo ""

# Make scripts executable
chmod +x entrypoint.prod.sh entrypoint.dev.sh 2>/dev/null || true

# Create necessary directories
mkdir -p nginx/conf.d nginx/ssl media staticfiles backups

echo -e "${GREEN}✅ Pre-deployment checks passed!${NC}"
echo ""

# Ask user what to do
echo "What would you like to do?"
echo "1) Fresh deployment (build and start)"
echo "2) Update existing deployment (rebuild and restart)"
echo "3) Start services"
echo "4) Stop services"
echo "5) View logs"
echo "6) Create superuser"
echo "7) Backup database"
echo "8) Check status"
echo ""
read -p "Enter your choice (1-8): " choice

case $choice in
    1)
        echo -e "${BLUE}🔨 Building production containers...${NC}"
        docker-compose -f docker-compose.prod.yml build
        
        echo -e "${BLUE}🚀 Starting services...${NC}"
        docker-compose -f docker-compose.prod.yml up -d
        
        echo ""
        echo -e "${GREEN}✅ Deployment complete!${NC}"
        echo ""
        echo "Next steps:"
        echo "1. Create superuser: docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser"
        echo "2. Access your app at: http://your-server-ip"
        echo "3. View logs: docker-compose -f docker-compose.prod.yml logs -f"
        ;;
    
    2)
        echo -e "${BLUE}🔄 Updating deployment...${NC}"
        docker-compose -f docker-compose.prod.yml down
        docker-compose -f docker-compose.prod.yml build
        docker-compose -f docker-compose.prod.yml up -d
        docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
        docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
        
        echo -e "${GREEN}✅ Update complete!${NC}"
        ;;
    
    3)
        echo -e "${BLUE}🚀 Starting services...${NC}"
        docker-compose -f docker-compose.prod.yml up -d
        echo -e "${GREEN}✅ Services started!${NC}"
        ;;
    
    4)
        echo -e "${YELLOW}⏸️  Stopping services...${NC}"
        docker-compose -f docker-compose.prod.yml down
        echo -e "${GREEN}✅ Services stopped!${NC}"
        ;;
    
    5)
        echo -e "${BLUE}📋 Viewing logs (Ctrl+C to exit)...${NC}"
        docker-compose -f docker-compose.prod.yml logs -f
        ;;
    
    6)
        echo -e "${BLUE}👤 Creating superuser...${NC}"
        docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
        ;;
    
    7)
        echo -e "${BLUE}💾 Creating database backup...${NC}"
        mkdir -p backups
        BACKUP_FILE="backups/backup_$(date +%Y%m%d_%H%M%S).sql.gz"
        docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U openspace_user openspace_prod | gzip > $BACKUP_FILE
        echo -e "${GREEN}✅ Backup created: $BACKUP_FILE${NC}"
        ;;
    
    8)
        echo -e "${BLUE}📊 Container status:${NC}"
        docker-compose -f docker-compose.prod.yml ps
        echo ""
        echo -e "${BLUE}💻 Resource usage:${NC}"
        docker stats --no-stream
        ;;
    
    *)
        echo -e "${RED}❌ Invalid choice!${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${BLUE}=========================================${NC}"
echo -e "${GREEN}Done!${NC}"
echo -e "${BLUE}=========================================${NC}"
