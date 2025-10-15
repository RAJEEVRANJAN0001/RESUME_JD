"use client"

import * as React from "react"
import {
  BarChart3,
  FileText,
  Home,
  Search,
  Settings,
  Upload,
  Users,
} from "lucide-react"

import { NavMain } from "@/components/nav-main"
import { NavUser } from "@/components/nav-user"
import { TeamSwitcher } from "@/components/team-switcher"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar"
import { sidebarData } from "@/lib/sidebar-data"
import { settingsApi } from "@/lib/api"
import { isAuthenticated } from "@/lib/auth"

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const [user, setUser] = React.useState(sidebarData.user)
  const [isLoading, setIsLoading] = React.useState(true)

  React.useEffect(() => {
    let mounted = true
    const load = async () => {
      try {
        if (!isAuthenticated()) {
          setIsLoading(false)
          return
        }
        const profile = await settingsApi.getProfile()
        if (!mounted) return
        setUser({
          name: profile.full_name || profile.email.split('@')[0],
          email: profile.email,
          avatar: sidebarData.user.avatar,
        })
      } catch (err) {
        // keep fallback
        console.debug('Failed to load profile for sidebar', err)
      } finally {
        if (mounted) setIsLoading(false)
      }
    }
    load()
    return () => {
      mounted = false
    }
  }, [])

  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <TeamSwitcher teams={sidebarData.teams} />
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={sidebarData.navMain} />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={user} isLoading={isLoading} />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}
