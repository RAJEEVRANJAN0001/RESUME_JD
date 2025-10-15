"use client"

import { ReactNode } from "react"

interface AppWrapperProps {
  children: ReactNode
}

export function AppWrapper({ children }: AppWrapperProps) {
  return (
    <div className="min-h-screen bg-background">
      {children}
    </div>
  )
}