"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ThemeToggle } from "@/components/theme-toggle"
import { ClientOnly } from "@/components/client-only"
import {
  FileText,
  Zap,
  Shield,
  TrendingUp,
  Users,
  Brain,
  Sparkles,
  CheckCircle2,
  ArrowRight,
  Upload,
  Search,
  BarChart3,
  Lock,
  Clock,
  Target,
  ChevronRight,
  Star,
} from "lucide-react"

export default function LandingPage() {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  const features = [
    {
      icon: Brain,
      title: "AI-Powered Parsing",
      description: "Advanced AI extracts skills, experience, and education from any resume format",
      color: "text-blue-600 dark:text-blue-400",
      bg: "bg-blue-50 dark:bg-blue-950",
    },
    {
      icon: Zap,
      title: "Lightning Fast",
      description: "Process hundreds of resumes in seconds with our optimized pipeline",
      color: "text-yellow-600 dark:text-yellow-400",
      bg: "bg-yellow-50 dark:bg-yellow-950",
    },
    {
      icon: Target,
      title: "Smart Matching",
      description: "Intelligent algorithms match candidates to job descriptions with 90%+ accuracy",
      color: "text-green-600 dark:text-green-400",
      bg: "bg-green-50 dark:bg-green-950",
    },
    {
      icon: Shield,
      title: "Secure & Private",
      description: "Enterprise-grade security with encrypted storage and GDPR compliance",
      color: "text-purple-600 dark:text-purple-400",
      bg: "bg-purple-50 dark:bg-purple-950",
    },
    {
      icon: BarChart3,
      title: "Analytics Dashboard",
      description: "Real-time insights and metrics to optimize your recruitment process",
      color: "text-orange-600 dark:text-orange-400",
      bg: "bg-orange-50 dark:bg-orange-950",
    },
    {
      icon: Users,
      title: "Team Collaboration",
      description: "Share candidates, add notes, and collaborate seamlessly with your team",
      color: "text-pink-600 dark:text-pink-400",
      bg: "bg-pink-50 dark:bg-pink-950",
    },
  ]

  const benefits = [
    { text: "Reduce screening time by 90%" },
    { text: "Improve candidate quality by 75%" },
    { text: "Save $50K+ annually on recruiting costs" },
    { text: "Process unlimited resumes" },
    { text: "24/7 support and updates" },
    { text: "No credit card required to start" },
  ]

  const stats = [
    { number: "10K+", label: "Resumes Processed" },
    { number: "95%", label: "Accuracy Rate" },
    { number: "50+", label: "Companies Trust Us" },
    { number: "4.9/5", label: "Customer Rating" },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-b from-background via-background to-muted/20">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 backdrop-blur-lg bg-background/80 border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="flex items-center space-x-2">
              <div className="bg-primary text-primary-foreground p-2 rounded-lg">
                <FileText className="h-6 w-6" />
              </div>
              <span className="font-bold text-xl">Resume Screener</span>
            </Link>
            
            <div className="flex items-center space-x-4">
              <ClientOnly fallback={<div className="w-[120px] h-[24px]" />}>
                <ThemeToggle />
              </ClientOnly>
              <Link href="/login">
                <Button variant="ghost">Sign In</Button>
              </Link>
              <Link href="/register">
                <Button>Get Started</Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 md:py-32">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          <Badge variant="secondary" className="text-sm">
            <Sparkles className="h-3 w-3 mr-1" />
            Powered by Azure AI & Google Gemini
          </Badge>
          
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-primary to-primary/60">
            Screen Resumes in Seconds,
            <br />
            Not Hours
          </h1>
          
          <p className="text-xl md:text-2xl text-muted-foreground max-w-2xl mx-auto">
            AI-powered resume parsing and intelligent candidate screening. 
            Find the perfect hire faster with our automated recruitment platform.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
            <Link href="/register">
              <Button size="lg" className="text-lg h-14 px-8">
                Start Free Trial
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link href="#features">
              <Button size="lg" variant="outline" className="text-lg h-14 px-8">
                See How It Works
              </Button>
            </Link>
          </div>
          
          <p className="text-sm text-muted-foreground">
            No credit card required • Free 14-day trial • Cancel anytime
          </p>
        </div>
      </section>

      {/* Stats Section */}
      <section className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto">
          {stats.map((stat, idx) => (
            <div key={idx} className="text-center space-y-2">
              <div className="text-4xl md:text-5xl font-bold text-primary">
                {stat.number}
              </div>
              <div className="text-sm text-muted-foreground">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="container mx-auto px-4 py-20">
        <div className="text-center space-y-4 mb-16">
          <Badge variant="outline">Features</Badge>
          <h2 className="text-4xl md:text-5xl font-bold">
            Everything You Need to Hire Smarter
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Powerful features designed to streamline your recruitment process
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {features.map((feature, idx) => {
            const Icon = feature.icon
            return (
              <Card key={idx} className="hover:shadow-lg transition-all duration-300 border-2 hover:border-primary/50">
                <CardHeader>
                  <div className={`${feature.bg} ${feature.color} p-3 rounded-lg w-fit mb-3`}>
                    <Icon className="h-6 w-6" />
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                  <CardDescription className="text-base">
                    {feature.description}
                  </CardDescription>
                </CardHeader>
              </Card>
            )
          })}
        </div>
      </section>

      {/* How It Works Section */}
      <section className="container mx-auto px-4 py-20 bg-muted/30 rounded-3xl my-20">
        <div className="text-center space-y-4 mb-16">
          <Badge variant="outline">Process</Badge>
          <h2 className="text-4xl md:text-5xl font-bold">
            How It Works
          </h2>
          <p className="text-xl text-muted-foreground">
            Get started in 3 simple steps
          </p>
        </div>
        
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {[
            {
              step: "1",
              icon: Upload,
              title: "Upload Resumes",
              description: "Drag and drop PDF or DOCX files. Our AI instantly extracts all relevant information.",
            },
            {
              step: "2",
              icon: Search,
              title: "Define Requirements",
              description: "Enter job description and required skills. Our algorithm understands context.",
            },
            {
              step: "3",
              icon: Target,
              title: "Get Matched Results",
              description: "Receive ranked candidates with match scores. Hire the perfect fit faster.",
            },
          ].map((item, idx) => {
            const Icon = item.icon
            return (
              <div key={idx} className="relative">
                <Card className="text-center h-full hover:shadow-xl transition-all">
                  <CardHeader>
                    <div className="mx-auto mb-4">
                      <div className="relative">
                        <div className="absolute -top-4 -left-4 w-12 h-12 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-2xl font-bold">
                          {item.step}
                        </div>
                        <div className="bg-primary/10 p-4 rounded-2xl">
                          <Icon className="h-12 w-12 text-primary" />
                        </div>
                      </div>
                    </div>
                    <CardTitle className="text-2xl mb-2">{item.title}</CardTitle>
                    <CardDescription className="text-base">
                      {item.description}
                    </CardDescription>
                  </CardHeader>
                </Card>
                {idx < 2 && (
                  <ChevronRight className="hidden md:block absolute top-1/2 -right-8 transform -translate-y-1/2 h-8 w-8 text-primary" />
                )}
              </div>
            )
          })}
        </div>
      </section>

      {/* Benefits Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="grid md:grid-cols-2 gap-12 max-w-6xl mx-auto items-center">
          <div className="space-y-6">
            <Badge variant="outline">Benefits</Badge>
            <h2 className="text-4xl md:text-5xl font-bold">
              Why Choose Resume Screener?
            </h2>
            <p className="text-lg text-muted-foreground">
              Join hundreds of companies that have transformed their hiring process with our AI-powered platform.
            </p>
            <div className="space-y-3">
              {benefits.map((benefit, idx) => (
                <div key={idx} className="flex items-center space-x-3">
                  <CheckCircle2 className="h-5 w-5 text-green-600 dark:text-green-400 flex-shrink-0" />
                  <span className="text-lg">{benefit.text}</span>
                </div>
              ))}
            </div>
            <Link href="/auth">
              <Button size="lg" className="mt-4">
                Start Your Free Trial
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
          </div>
          
          <Card className="p-8 bg-gradient-to-br from-primary/5 to-primary/10 border-2">
            <CardContent className="space-y-6 p-0">
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <Clock className="h-8 w-8 text-primary" />
                  <div>
                    <h3 className="font-bold text-xl">Save Time</h3>
                    <p className="text-muted-foreground">Automated screening frees up your HR team</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-3">
                  <TrendingUp className="h-8 w-8 text-primary" />
                  <div>
                    <h3 className="font-bold text-xl">Improve Quality</h3>
                    <p className="text-muted-foreground">Find better candidates with AI matching</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-3">
                  <Lock className="h-8 w-8 text-primary" />
                  <div>
                    <h3 className="font-bold text-xl">Stay Secure</h3>
                    <p className="text-muted-foreground">Enterprise-grade data protection</p>
                  </div>
                </div>
              </div>
              
              
            </CardContent>
          </Card>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-20">
        <Card className="bg-gradient-to-r from-primary to-primary/80 text-primary-foreground border-0 max-w-4xl mx-auto">
          <CardContent className="p-12 text-center space-y-6">
            <h2 className="text-4xl md:text-5xl font-bold">
              Ready to Transform Your Hiring?
            </h2>
            <p className="text-xl opacity-90 max-w-2xl mx-auto">
              Join thousands of companies using AI to find better candidates faster. 
              Start your free trial today - no credit card required.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
              <Link href="/auth">
                <Button size="lg" variant="secondary" className="text-lg h-14 px-8">
                  Start Free Trial
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Footer */}
      <footer className="border-t mt-20">
        <div className="container mx-auto px-4 py-12">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="space-y-4">
              <Link href="/" className="flex items-center space-x-2">
                <div className="bg-primary text-primary-foreground p-2 rounded-lg">
                  <FileText className="h-6 w-6" />
                </div>
                <span className="font-bold text-xl">Resume Screener</span>
              </Link>
              <p className="text-sm text-muted-foreground">
                AI-powered resume screening for modern recruiters
              </p>
            </div>
            
            <div>
              <h3 className="font-bold mb-4">Product</h3>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link href="#features" className="hover:text-foreground">Features</Link></li>
                <li><Link href="/auth" className="hover:text-foreground">Pricing</Link></li>
              
              </ul>
            </div>
            
            <div>
              <h3 className="font-bold mb-4">Company</h3>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link href="/auth" className="hover:text-foreground">About</Link></li>
            
                <li><Link href="/auth" className="hover:text-foreground">Careers</Link></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-bold mb-4">Support</h3>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link href="/auth" className="hover:text-foreground">Help Center</Link></li>
                <li><Link href="/auth" className="hover:text-foreground">Contact</Link></li>
                <li><Link href="/auth" className="hover:text-foreground">Privacy</Link></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t mt-12 pt-8 text-center text-sm text-muted-foreground">
            <p>© 2024 Smart Resume Screener. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
