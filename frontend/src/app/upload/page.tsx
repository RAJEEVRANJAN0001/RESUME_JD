"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { uploadApi } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { toast } from "sonner"
import { FileUp, Upload, CheckCircle2, TrendingUp, Briefcase, GraduationCap, Sparkles } from "lucide-react"

export default function UploadPage() {
  const router = useRouter()
  const [file, setFile] = useState<File | null>(null)
  const [jobDescription, setJobDescription] = useState("")
  const [requiredSkills, setRequiredSkills] = useState("")
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [dragActive, setDragActive] = useState(false)

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0]
      if (droppedFile.type === "application/pdf" || 
          droppedFile.type === "application/vnd.openxmlformats-officedocument.wordprocessingml.document") {
        setFile(droppedFile)
        toast.success(`File "${droppedFile.name}" selected`)
      } else {
        toast.error("Please upload only PDF or DOCX files")
      }
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      toast.success(`File "${e.target.files[0].name}" selected`)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) {
      toast.error("Please select a file")
      return
    }

    setLoading(true)
    setResult(null)

    try {
      const response = await uploadApi.uploadResume(
        file,
        jobDescription || undefined,
        requiredSkills || undefined
      )
      setResult(response)
      toast.success("Resume uploaded and parsed successfully!")
      
      // Reset form
      setFile(null)
      setJobDescription("")
      setRequiredSkills("")
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "Failed to upload resume")
    } finally {
      setLoading(false)
    }
  }

  const clearForm = () => {
    setResult(null)
    setFile(null)
    setJobDescription("")
    setRequiredSkills("")
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Upload Resume</h1>
        <p className="text-muted-foreground">
          Upload PDF or DOCX files for AI-powered parsing and analysis
        </p>
      </div>

      {!result ? (
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* File Upload Card */}
          <Card>
            <CardHeader>
              <CardTitle>Select Resume File</CardTitle>
              <CardDescription>
                Upload a PDF or DOCX file to extract candidate information
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div
                className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                  dragActive
                    ? "border-primary bg-primary/5"
                    : "border-muted-foreground/25 hover:border-muted-foreground/50"
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <Input
                  type="file"
                  accept=".pdf,.docx"
                  onChange={handleFileChange}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  required
                />
                <div className="flex flex-col items-center space-y-4">
                  <div className="p-4 bg-primary/10 rounded-full">
                    <FileUp className="h-8 w-8 text-primary" />
                  </div>
                  {file ? (
                    <div className="space-y-2">
                      <div className="flex items-center space-x-2">
                        <CheckCircle2 className="h-5 w-5 text-green-600" />
                        <span className="font-medium">{file.name}</span>
                      </div>
                      <p className="text-xs text-muted-foreground">
                        {(file.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                  ) : (
                    <div className="space-y-2">
                      <p className="text-sm font-medium">
                        Drop your resume here or click to browse
                      </p>
                      <p className="text-xs text-muted-foreground">
                        Supports PDF and DOCX files (Max 10MB)
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Optional Matching Card */}
          <Card>
            <CardHeader>
              <CardTitle>Optional: Match with Job (Get Score)</CardTitle>
              <CardDescription>
                Provide job details to calculate candidate match score
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="job-description">Job Description</Label>
                <Textarea
                  id="job-description"
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  rows={4}
                  placeholder="Paste the full job description here to calculate match score..."
                  className="resize-none"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="required-skills">Required Skills (comma-separated)</Label>
                <Input
                  id="required-skills"
                  value={requiredSkills}
                  onChange={(e) => setRequiredSkills(e.target.value)}
                  placeholder="Python, React, AWS, Node.js, TypeScript"
                />
                <p className="text-xs text-muted-foreground">
                  Separate multiple skills with commas
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Submit Button */}
          <Button type="submit" disabled={loading || !file} className="w-full" size="lg">
            {loading ? (
              <>
                <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
                Processing...
              </>
            ) : (
              <>
                <Upload className="mr-2 h-4 w-4" />
                Upload and Parse Resume
              </>
            )}
          </Button>
        </form>
      ) : (
        /* Success Result */
        <div className="space-y-6">
          <Card className="border-green-200 bg-green-50 dark:bg-green-950 dark:border-green-800">
            <CardHeader>
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="h-6 w-6 text-green-600 dark:text-green-400" />
                <CardTitle>Resume Uploaded Successfully!</CardTitle>
              </div>
              <CardDescription>
                The resume has been parsed and stored in the database
              </CardDescription>
            </CardHeader>
          </Card>

          {/* Parsed Data */}
          <Card>
            <CardHeader>
              <CardTitle>Extracted Information</CardTitle>
              <CardDescription>
                AI-powered resume parsing results
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label className="text-xs text-muted-foreground">Candidate Name</Label>
                <p className="text-lg font-semibold">{result.resume_data.name || "Not specified"}</p>
              </div>

              {result.resume_data.email && (
                <div>
                  <Label className="text-xs text-muted-foreground">Email</Label>
                  <p className="font-medium">{result.resume_data.email}</p>
                </div>
              )}

              {result.resume_data.phone && (
                <div>
                  <Label className="text-xs text-muted-foreground">Phone</Label>
                  <p className="font-medium">{result.resume_data.phone}</p>
                </div>
              )}

              <Separator />

              <div>
                <Label className="text-xs text-muted-foreground mb-2 block">Skills</Label>
                <div className="flex flex-wrap gap-2">
                  {result.resume_data.skills.length > 0 ? (
                    result.resume_data.skills.map((skill: string, idx: number) => (
                      <Badge key={idx} variant="secondary">
                        {skill}
                      </Badge>
                    ))
                  ) : (
                    <p className="text-sm text-muted-foreground">No skills extracted</p>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Match Score (if available) */}
          {result.match_score !== undefined && (
            <Card className="border-primary/20">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Match Score</CardTitle>
                    <CardDescription>
                      Candidate fit for the provided job description
                    </CardDescription>
                  </div>
                  <div className="text-right">
                    <div className="text-4xl font-bold text-primary">
                      {result.match_score}%
                    </div>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <Progress value={result.match_score} className="mb-4" />
                
                {result.match_details && (
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
                    <div className="space-y-1">
                      <div className="flex items-center space-x-1">
                        <Sparkles className="h-3 w-3 text-muted-foreground" />
                        <Label className="text-xs">Skills</Label>
                      </div>
                      <p className="text-2xl font-bold">
                        {result.match_details.breakdown.skills_score.toFixed(0)}%
                      </p>
                    </div>
                    <div className="space-y-1">
                      <div className="flex items-center space-x-1">
                        <Briefcase className="h-3 w-3 text-muted-foreground" />
                        <Label className="text-xs">Experience</Label>
                      </div>
                      <p className="text-2xl font-bold">
                        {result.match_details.breakdown.experience_score.toFixed(0)}%
                      </p>
                    </div>
                    <div className="space-y-1">
                      <div className="flex items-center space-x-1">
                        <GraduationCap className="h-3 w-3 text-muted-foreground" />
                        <Label className="text-xs">Education</Label>
                      </div>
                      <p className="text-2xl font-bold">
                        {result.match_details.breakdown.education_score.toFixed(0)}%
                      </p>
                    </div>
                    <div className="space-y-1">
                      <div className="flex items-center space-x-1">
                        <TrendingUp className="h-3 w-3 text-muted-foreground" />
                        <Label className="text-xs">Semantic</Label>
                      </div>
                      <p className="text-2xl font-bold">
                        {result.match_details.breakdown.semantic_score.toFixed(0)}%
                      </p>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          )}

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-3">
            <Button
              onClick={() => router.push(`/resumes/${result.resume_id}`)}
              className="flex-1"
              size="lg"
            >
              View Full Resume
            </Button>
            <Button
              onClick={() => router.push("/resumes")}
              variant="outline"
              className="flex-1"
              size="lg"
            >
              Go to All Resumes
            </Button>
            <Button
              onClick={clearForm}
              variant="secondary"
              className="flex-1"
              size="lg"
            >
              Upload Another
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}
