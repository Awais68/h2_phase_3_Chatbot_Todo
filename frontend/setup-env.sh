#!/bin/bash

# Setup script for switching between local and production environments

echo "🚀 Environment Setup Script"
echo ""
echo "Choose your setup:"
echo "1) Local Development (SQLite + Local Backend)"
echo "2) Production Testing (PostgreSQL + Render Backend)"
echo ""
read -p "Enter choice (1 or 2): " choice

case $choice in
  1)
    echo "📝 Setting up LOCAL development environment..."
    cat > .env.local << EOF
# Local Development Configuration
NEXT_PUBLIC_APP_URL=http://localhost:3005
NEXT_PUBLIC_API_URL=http://localhost:8000
DATABASE_URL="file:./prisma/dev.db"
BETTER_AUTH_SECRET="Ikns5R4zC2bdlj+83nblBOMlL+jKa9wXdVkfviQDRuQ="
EOF
    
    # Update Prisma schema for SQLite
    sed -i 's/provider = "postgresql"/provider = "sqlite"/' prisma/schema.prisma
    
    echo "✅ Local environment configured!"
    echo "Run: npm run dev"
    ;;
    
  2)
    echo "📝 Setting up PRODUCTION testing environment..."
    read -p "Enter your PostgreSQL DATABASE_URL: " db_url
    
    cat > .env.local << EOF
# Production Testing Configuration
NEXT_PUBLIC_APP_URL=http://localhost:3005
NEXT_PUBLIC_API_URL=https://hackathon-2-phase-ii-full-stack-web-app-1.onrender.com
DATABASE_URL="${db_url}"
BETTER_AUTH_SECRET="Ikns5R4zC2bdlj+83nblBOMlL+jKa9wXdVkfviQDRuQ="
EOF
    
    # Update Prisma schema for PostgreSQL
    sed -i 's/provider = "sqlite"/provider = "postgresql"/' prisma/schema.prisma
    
    echo "🔄 Running Prisma migrations..."
    npx prisma generate
    npx prisma db push
    
    echo "✅ Production environment configured!"
    echo "Run: npm run dev"
    ;;
    
  *)
    echo "❌ Invalid choice. Exiting."
    exit 1
    ;;
esac
