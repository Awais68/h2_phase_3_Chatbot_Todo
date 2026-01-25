#!/bin/bash

echo "🔧 Setting up better-auth with Prisma..."

# Navigate to current directory (where the script is located)
cd "$(dirname "$0")"

# Install correct Prisma versions
echo "📦 Installing Prisma 5..."
npm uninstall prisma @prisma/client
npm install prisma@5.22.0 @prisma/client@5.22.0

# Generate Prisma Client
echo "🎯 Generating Prisma Client..."
npx prisma generate

# Push database schema
echo "🗄️  Creating database..."
npx prisma db push --accept-data-loss

echo "✅ Setup complete! You can now:"
echo "   1. Start the frontend: npm run dev"
echo "   2. Login/Signup will use better-auth"
