import { auth } from "@/lib/auth"
import { NextResponse } from "next/server"

// Create handlers based on auth initialization status
const createHandlers = () => {
  if (!auth || !auth.handler) {
    console.error("❌ Auth not initialized - DATABASE_URL or BETTER_AUTH_SECRET missing?", {
      hasDatabase: !!process.env.DATABASE_URL,
      hasAuthSecret: !!process.env.BETTER_AUTH_SECRET,
      isBuilding: process.env.NEXT_PHASE === 'phase-production-build'
    })

    // Provide fallback handlers
    const errorHandler = () => {
      return NextResponse.json(
        {
          error: "Auth service not configured",
          message: "DATABASE_URL and BETTER_AUTH_SECRET environment variables are required",
          hasDatabase: !!process.env.DATABASE_URL,
          hasAuthSecret: !!process.env.BETTER_AUTH_SECRET,
          isBuilding: process.env.NEXT_PHASE === 'phase-production-build'
        },
        { status: 503 }
      )
    }

    return { GET: errorHandler, POST: errorHandler }
  }

  return { GET: auth.handler, POST: auth.handler }
}

const handlers = createHandlers()

export const GET = handlers.GET
export const POST = handlers.POST

