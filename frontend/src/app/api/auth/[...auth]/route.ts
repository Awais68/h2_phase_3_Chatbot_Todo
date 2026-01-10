import { auth } from "@/lib/auth"
import { NextResponse } from "next/server"

// Create handlers based on auth initialization status
const createHandlers = () => {
  if (!auth || !auth.handler) {
    console.error("❌ Auth not initialized - DATABASE_URL missing?")
    
    // Provide fallback handlers
    const errorHandler = () => {
      return NextResponse.json(
        { 
          error: "Auth service not configured",
          message: "DATABASE_URL environment variable is required",
          hasDatabase: !!process.env.DATABASE_URL 
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

