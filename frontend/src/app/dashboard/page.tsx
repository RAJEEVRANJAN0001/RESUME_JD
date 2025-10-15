"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { isAuthenticated } from "@/lib/auth"
import { resumeApi } from "@/lib/api"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { 
  FileText, 
  Upload, 
  Search, 
  Users, 
  TrendingUp, 
  Clock,
  CheckCircle2,
  AlertCircle,
  Activity,
  Sparkles,
  ArrowRight,
  RefreshCw
} from "lucide-react"
import Link from "next/link"
import { toast } from "sonner"

interface Resume {
  id: string
  name: string
  parsed_at: string
  match_score?: number
  skills: string[]
}

export default function DashboardPage() {
  const router = useRouter()
  const [stats, setStats] = useState({
    totalResumes: 0,
    recentResumes: 0,
    avgMatchScore: 0,
    todayResumes: 0,
  })
  const [recentResumes, setRecentResumes] = useState<Resume[]>([])
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)

  useEffect(() => {
    // Check authentication
    if (!isAuthenticated()) {
      toast.error("Please login to access the dashboard")
      router.push("/login")
      return
    }
    
    fetchDashboardData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const fetchDashboardData = async (isRefresh = false) => {
    if (isRefresh) {
      setRefreshing(true)
    }
    
    try {
      const resumes = await resumeApi.list({ limit: 100 })
      
      const now = new Date()
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
      const weekAgo = new Date()
      weekAgo.setDate(weekAgo.getDate() - 7)
      
      const recentResumesList = resumes.filter((r: Resume) => {
        const parsedDate = new Date(r.parsed_at)
        return parsedDate > weekAgo
      })
      
      const todayResumesList = resumes.filter((r: Resume) => {
        const parsedDate = new Date(r.parsed_at)
        return parsedDate >= today
      })
      
      setStats({
        totalResumes: resumes.length,
        recentResumes: recentResumesList.length,
        todayResumes: todayResumesList.length,
        avgMatchScore: resumes.length > 0 
          ? Math.round(resumes.reduce((acc: number, r: Resume) => acc + (r.match_score || 0), 0) / resumes.length)
          : 0,
      })
      
      // Set recent resumes for the activity feed
      setRecentResumes(recentResumesList.slice(0, 5))
      
      if (isRefresh) {
        toast.success("Dashboard refreshed successfully")
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || "Failed to load dashboard data"
      toast.error(errorMessage)
      console.error("Dashboard fetch error:", error)
    } finally {
      setLoading(false)
      setRefreshing(false)
    }
  }
  
  const handleRefresh = () => {
    fetchDashboardData(true)
  }

  const statCards = [
    {
      title: "Total Resumes",
      value: stats.totalResumes,
      description: "All parsed resumes in database",
      icon: FileText,
      color: "text-blue-600 dark:text-blue-400",
      bgColor: "bg-blue-50 dark:bg-blue-950",
      trend: stats.todayResumes > 0 ? `+${stats.todayResumes} today` : "No uploads today",
      trendColor: stats.todayResumes > 0 ? "text-green-600" : "text-muted-foreground",
    },
    {
      title: "Recent Uploads",
      value: stats.recentResumes,
      description: "Uploaded in the last 7 days",
      icon: Clock,
      color: "text-green-600 dark:text-green-400",
      bgColor: "bg-green-50 dark:bg-green-950",
      trend: stats.recentResumes > 0 ? "Active" : "Inactive",
      trendColor: stats.recentResumes > 0 ? "text-green-600" : "text-orange-600",
    },
    {
      title: "Avg Match Score",
      value: `${stats.avgMatchScore}%`,
      description: "Average candidate matching",
      icon: TrendingUp,
      color: "text-purple-600 dark:text-purple-400",
      bgColor: "bg-purple-50 dark:bg-purple-950",
      trend: stats.avgMatchScore >= 70 ? "Excellent" : stats.avgMatchScore >= 50 ? "Good" : "Fair",
      trendColor: stats.avgMatchScore >= 70 ? "text-green-600" : stats.avgMatchScore >= 50 ? "text-blue-600" : "text-orange-600",
    },
    {
      title: "Total Candidates",
      value: stats.totalResumes,
      description: "Unique candidates in pool",
      icon: Users,
      color: "text-orange-600 dark:text-orange-400",
      bgColor: "bg-orange-50 dark:bg-orange-950",
      trend: "Growing",
      trendColor: "text-green-600",
    },
  ]

  const quickActions = [
    {
      title: "Upload Resume",
      description: "Parse and analyze a new resume",
      icon: Upload,
      href: "/upload",
      color: "text-primary",
    },
    {
      title: "Search Resumes",
      description: "Find candidates by skills and criteria",
      icon: Search,
      href: "/search",
      color: "text-primary",
    },
    {
      title: "View All Resumes",
      description: "Browse all parsed resumes",
      icon: Users,
      href: "/resumes",
      color: "text-primary",
    },
  ]

  if (loading) {
    return (
      <div className="container mx-auto p-6">
        <div className="flex items-center justify-center h-[calc(100vh-200px)]">
          <div className="flex flex-col items-center space-y-4">
            <div className="relative">
              <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-primary"></div>
              <Sparkles className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 h-6 w-6 text-primary animate-pulse" />
            </div>
            <div className="text-center">
              <p className="text-lg font-medium">Loading dashboard...</p>
              <p className="text-sm text-muted-foreground">Fetching your data</p>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto p-6 space-y-8 animate-in fade-in duration-500">
      {/* Header */}
      <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
              <Badge variant="secondary" className="gap-1">
                <Activity className="h-3 w-3" />
                Live
              </Badge>
            </div>
            <p className="text-muted-foreground mt-1">
              Welcome to your Smart Resume Screener dashboard
            </p>
          </div>
          <Button 
            onClick={handleRefresh} 
            disabled={refreshing}
            variant="outline"
            className="gap-2"
          >
            <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
        </div>

        {/* Stats Grid */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {statCards.map((stat, index) => {
            const Icon = stat.icon
            return (
              <Card 
                key={stat.title} 
                className="hover:shadow-lg transition-all duration-300 hover:scale-105 animate-in slide-in-from-bottom"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    {stat.title}
                  </CardTitle>
                  <div className={`p-2 rounded-lg ${stat.bgColor} transition-all duration-300 hover:scale-110`}>
                    <Icon className={`h-4 w-4 ${stat.color}`} />
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold mb-1">{stat.value}</div>
                  <p className="text-xs text-muted-foreground mb-2">
                    {stat.description}
                  </p>
                  <Badge variant="outline" className={`text-xs ${stat.trendColor}`}>
                    {stat.trend}
                  </Badge>
                </CardContent>
              </Card>
            )
          })}
        </div>

        {/* Quick Actions & Recent Activity */}
        <div className="grid gap-6 lg:grid-cols-3">
          {/* Quick Actions */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold tracking-tight">Quick Actions</h2>
              <Badge variant="secondary">3 Actions</Badge>
            </div>
            <div className="grid gap-4 md:grid-cols-3">
              {quickActions.map((action, index) => {
                const Icon = action.icon
                return (
                  <Link key={action.title} href={action.href}>
                    <Card className="hover:shadow-xl transition-all duration-300 cursor-pointer h-full hover:scale-105 hover:border-primary group animate-in slide-in-from-bottom"
                      style={{ animationDelay: `${(index + 4) * 100}ms` }}
                    >
                      <CardHeader>
                        <div className="flex items-center space-x-3">
                          <div className={`p-2 rounded-lg ${action.color === 'text-primary' ? 'bg-primary/10' : 'bg-secondary'} group-hover:scale-110 transition-transform`}>
                            <Icon className={`h-5 w-5 ${action.color}`} />
                          </div>
                          <CardTitle className="text-base">{action.title}</CardTitle>
                        </div>
                        <CardDescription className="text-xs">{action.description}</CardDescription>
                      </CardHeader>
                      <CardContent>
                        <Button variant="ghost" size="sm" className="w-full group-hover:bg-primary group-hover:text-primary-foreground transition-colors gap-2">
                          Open
                          <ArrowRight className="h-3 w-3" />
                        </Button>
                      </CardContent>
                    </Card>
                  </Link>
                )
              })}
            </div>
          </div>

          {/* Recent Activity */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold tracking-tight">Recent Activity</h2>
              {recentResumes.length > 0 && (
                <Badge variant="outline">{recentResumes.length} Recent</Badge>
              )}
            </div>
            <Card className="animate-in slide-in-from-right">
              <CardHeader>
                <CardTitle className="text-base flex items-center gap-2">
                  <Clock className="h-4 w-4" />
                  Latest Uploads
                </CardTitle>
                <CardDescription>Recently processed resumes</CardDescription>
              </CardHeader>
              <CardContent>
                {recentResumes.length === 0 ? (
                  <div className="text-center py-8">
                    <AlertCircle className="h-12 w-12 mx-auto text-muted-foreground mb-3" />
                    <p className="text-sm text-muted-foreground">No recent activity</p>
                    <p className="text-xs text-muted-foreground mt-1">Upload a resume to get started</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {recentResumes.map((resume) => (
                      <div 
                        key={resume.id}
                        className="flex items-start justify-between p-3 rounded-lg border hover:bg-accent transition-colors cursor-pointer group"
                        onClick={() => router.push(`/resumes/${resume.id}`)}
                      >
                        <div className="flex items-start gap-3 flex-1 min-w-0">
                          <CheckCircle2 className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium truncate group-hover:text-primary transition-colors">
                              {resume.name}
                            </p>
                            <p className="text-xs text-muted-foreground">
                              {new Date(resume.parsed_at).toLocaleDateString('en-US', { 
                                month: 'short', 
                                day: 'numeric',
                                hour: '2-digit',
                                minute: '2-digit'
                              })}
                            </p>
                          </div>
                        </div>
                        {resume.match_score && (
                          <Badge variant="secondary" className="ml-2 flex-shrink-0">
                            {resume.match_score}%
                          </Badge>
                        )}
                      </div>
                    ))}
                    {recentResumes.length >= 5 && (
                      <Link href="/resumes">
                        <Button variant="ghost" size="sm" className="w-full gap-2">
                          View All Resumes
                          <ArrowRight className="h-3 w-3" />
                        </Button>
                      </Link>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Getting Started */}
        <Card className="border-2 border-dashed animate-in slide-in-from-bottom" style={{ animationDelay: '700ms' }}>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-primary" />
              <CardTitle>Getting Started</CardTitle>
            </div>
            <CardDescription>
              Follow these steps to start screening resumes efficiently
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-start space-x-4 p-4 rounded-lg bg-muted/50 hover:bg-muted transition-colors">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm font-bold">
                  1
                </div>
                <div className="flex-1">
                  <p className="font-semibold mb-1">Upload Resumes</p>
                  <p className="text-sm text-muted-foreground mb-2">
                    Upload PDF or DOCX resumes to parse with AI. Our system extracts skills, experience, and education automatically.
                  </p>
                  <Link href="/upload">
                    <Button size="sm" variant="outline" className="gap-2">
                      <Upload className="h-3 w-3" />
                      Start Uploading
                    </Button>
                  </Link>
                </div>
              </div>
              
              <Separator />
              
              <div className="flex items-start space-x-4 p-4 rounded-lg bg-muted/50 hover:bg-muted transition-colors">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm font-bold">
                  2
                </div>
                <div className="flex-1">
                  <p className="font-semibold mb-1">Review Parsed Data</p>
                  <p className="text-sm text-muted-foreground mb-2">
                    Check and verify the extracted information. Edit details if needed for accuracy.
                  </p>
                  <Link href="/resumes">
                    <Button size="sm" variant="outline" className="gap-2">
                      <FileText className="h-3 w-3" />
                      View Resumes
                    </Button>
                  </Link>
                </div>
              </div>
              
              <Separator />
              
              <div className="flex items-start space-x-4 p-4 rounded-lg bg-muted/50 hover:bg-muted transition-colors">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm font-bold">
                  3
                </div>
                <div className="flex-1">
                  <p className="font-semibold mb-1">Search & Match Candidates</p>
                  <p className="text-sm text-muted-foreground mb-2">
                    Use job descriptions to find the best candidates. Get AI-powered matching scores.
                  </p>
                  <Link href="/search">
                    <Button size="sm" variant="outline" className="gap-2">
                      <Search className="h-3 w-3" />
                      Start Searching
                    </Button>
                  </Link>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
  )
}

