import {
  BarChart3,
  FileText,
  Home,
  Search,
  Settings,
  Upload,
  Users,
} from "lucide-react"

export const sidebarData = {
  user: {
    name: "Your Name",
    email: "your@email.com",
    avatar: "/avatars/default.png",
  },
  teams: [
    {
      name: "Resume Screener",
      logo: FileText,
      plan: "Enterprise",
    },
  ],
  navMain: [
    {
      title: "Dashboard",
      url: "/dashboard",
      icon: Home,
      isActive: true,
    },
    {
      title: "Upload",
      url: "/upload",
      icon: Upload,
    },
    {
      title: "Search",
      url: "/search",
      icon: Search,
    },
    {
      title: "All Resumes",
      url: "/resumes",
      icon: Users,
    },
    {
      title: "Analytics",
      url: "/analytics",
      icon: BarChart3,
    },
    {
      title: "Settings",
      url: "/settings",
      icon: Settings,
    },
  ],
}