"use client"

import * as React from "react"
import { Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"
import { Switch } from "@/components/ui/switch"

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = React.useState(false)

  // useEffect only runs on the client, so now we can safely show the UI
  React.useEffect(() => {
    setMounted(true)
  }, [])

  return (
    <div className={`flex items-center space-x-2 transition-opacity duration-200 ${mounted ? 'opacity-100' : 'opacity-0'}`}>
      <Sun className="h-4 w-4 text-muted-foreground" />
      <Switch
        id="theme-toggle"
        checked={theme === "dark"}
        onCheckedChange={(checked) => setTheme(checked ? "dark" : "light")}
        disabled={!mounted}
      />
      <Moon className="h-4 w-4 text-muted-foreground" />
    </div>
  )
}
