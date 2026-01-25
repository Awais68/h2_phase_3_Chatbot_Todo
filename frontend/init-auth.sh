#!/bin/bash

echo "🚀 Initializing authentication system..."

# Navigate to the frontend directory
cd "$(dirname "$0")"

echo "📦 Installing dependencies..."
npm install

echo "🔄 Generating Prisma client..."
npx prisma generate

echo "🗄️  Pushing database schema..."
npx prisma db push

echo "✅ Authentication system initialized!"
echo ""
echo "To start the development server:"
echo "npm run dev"
echo ""
echo "For production builds:"
echo "npm run build"