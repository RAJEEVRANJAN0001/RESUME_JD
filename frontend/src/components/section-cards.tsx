import { FileText, TrendingUp, Users, Clock } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export function SectionCards() {
  const cards = [
    {
      title: "Total Resumes",
      value: "1,234",
      description: "All parsed resumes in database",
      icon: FileText,
      color: "text-blue-600 dark:text-blue-400",
      bgColor: "bg-blue-50 dark:bg-blue-950",
      trend: "+12% from last month",
      trendColor: "text-green-600",
    },
    {
      title: "Recent Uploads",
      value: "89",
      description: "Uploaded in the last 7 days",
      icon: Clock,
      color: "text-green-600 dark:text-green-400",
      bgColor: "bg-green-50 dark:bg-green-950",
      trend: "Active",
      trendColor: "text-green-600",
    },
    {
      title: "Avg Match Score",
      value: "78%",
      description: "Average candidate matching",
      icon: TrendingUp,
      color: "text-purple-600 dark:text-purple-400",
      bgColor: "bg-purple-50 dark:bg-purple-950",
      trend: "Excellent",
      trendColor: "text-green-600",
    },
    {
      title: "Total Candidates",
      value: "1,234",
      description: "Unique candidates in pool",
      icon: Users,
      color: "text-orange-600 dark:text-orange-400",
      bgColor: "bg-orange-50 dark:bg-orange-950",
      trend: "Growing",
      trendColor: "text-green-600",
    },
  ]

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {cards.map((card, index) => {
        const Icon = card.icon
        return (
          <Card
            key={card.title}
            className="hover:shadow-lg transition-all duration-300 hover:scale-105"
          >
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                {card.title}
              </CardTitle>
              <div className={`p-2 rounded-lg ${card.bgColor}`}>
                <Icon className={`h-4 w-4 ${card.color}`} />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold mb-1">{card.value}</div>
              <p className="text-xs text-muted-foreground mb-2">
                {card.description}
              </p>
              <div className={`text-xs ${card.trendColor}`}>
                {card.trend}
              </div>
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}