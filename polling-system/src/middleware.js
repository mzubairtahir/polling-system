import { NextResponse } from 'next/server'

// This function can be marked `async` if using `await` inside
export async function middleware(request) {

  const sessionId = request.cookies.get("csrftoken");
  const csrf = request.cookies.get("sessionid");


  if (sessionId === undefined || csrf === undefined) {
    return NextResponse.redirect(new URL('/auth/signin', request.url))
  }
}

// See "Matching Paths" below to learn more
export const config = {
  matcher: ['/profile/:path*', '/create/:path'],
}