import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json({
    status: 'ok',
    env: {
      hasDatabase: !!process.env.DATABASE_URL,
      databaseType: process.env.DATABASE_URL?.includes('postgres') ? 'postgresql' : 
                   process.env.DATABASE_URL?.includes('file:') ? 'sqlite' : 'none',
      hasAuthSecret: !!process.env.BETTER_AUTH_SECRET,
      hasApiUrl: !!process.env.NEXT_PUBLIC_API_URL,
      hasAppUrl: !!process.env.NEXT_PUBLIC_APP_URL,
      nodeEnv: process.env.NODE_ENV,
      vercelUrl: process.env.VERCEL_URL || 'not set'
    },
    message: 'Check if all required environment variables are set'
  })
}
