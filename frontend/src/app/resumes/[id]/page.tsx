"use client"

import { useState, useEffect } from "react"
import { useRouter, useParams } from "next/navigation"
import { isAuthenticated } from "@/lib/auth"
import { resumeApi } from "@/lib/api"
import type { Resume } from "@/types"
import { 
  Save, 
  ArrowLeft, 
  Briefcase, 
  GraduationCap, 
  Award, 
  Mail,
  Phone,
  Linkedin,
  Globe,
  User,
  Calendar,
  MapPin,
  Edit2,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  Download,
  Trash2
} from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { toast } from "sonner"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"

export default function ResumeDetailPage() {
  const router = useRouter()
  const params = useParams()
  const [resume, setResume] = useState<Resume | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [isEditing, setIsEditing] = useState(false)
  const [showDeleteDialog, setShowDeleteDialog] = useState(false)
  const [deleting, setDeleting] = useState(false)

  useEffect(() => {
    // Ensure params is available before proceeding
    if (!params?.id) {
      setLoading(false)
      return
    }

    if (!isAuthenticated()) {
      toast.error("Please login to access resume details")
      router.push("/login")
      return
    }

    loadResume(params.id as string)
  }, [router, params?.id])

  const loadResume = async (id: string) => {
    try {
      const data = await resumeApi.get(id)
      setResume(data)
      toast.success("Resume loaded successfully")
    } catch (error: any) {
      console.error("Failed to load resume:", error)
      const errorMessage = error.response?.data?.detail || "Failed to load resume"
      toast.error(errorMessage)
      setTimeout(() => router.push("/resumes"), 2000)
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    if (!resume) return
    
    setSaving(true)
    try {
      await resumeApi.update(resume.id, resume)
      toast.success("Resume updated successfully!", {
        description: "All changes have been saved",
        icon: <CheckCircle2 className="h-5 w-5" />,
      })
      setIsEditing(false)
    } catch (error: any) {
      console.error("Failed to save resume:", error)
      const errorMessage = error.response?.data?.detail || "Failed to save changes"
      toast.error(errorMessage, {
        description: "Please try again",
        icon: <AlertCircle className="h-5 w-5" />,
      })
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async () => {
    if (!resume) return
    
    setDeleting(true)
    try {
      await resumeApi.delete(resume.id)
      toast.success("Resume deleted successfully")
      router.push("/resumes")
    } catch (error: any) {
      console.error("Failed to delete resume:", error)
      const errorMessage = error.response?.data?.detail || "Failed to delete resume"
      toast.error(errorMessage)
      setDeleting(false)
      setShowDeleteDialog(false)
    }
  }

  const formatDate = (dateString?: string | null) => {
    if (!dateString) return "Present"
    try {
      return new Date(dateString).toLocaleDateString("en-US", {
        month: "short",
        year: "numeric",
      })
    } catch {
      return dateString
    }
  }

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
              <p className="text-lg font-medium">Loading resume...</p>
              <p className="text-sm text-muted-foreground">Please wait</p>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (!resume) {
    return (
      <div className="container mx-auto p-6">
        <Card className="max-w-md mx-auto mt-20">
          <CardHeader>
            <div className="flex justify-center mb-4">
              <div className="p-3 bg-destructive/10 rounded-full">
                <AlertCircle className="h-12 w-12 text-destructive" />
              </div>
            </div>
            <CardTitle className="text-center">Resume Not Found</CardTitle>
            <CardDescription className="text-center">
              The resume you're looking for doesn't exist or has been deleted
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={() => router.push("/resumes")} className="w-full gap-2">
              <ArrowLeft className="h-4 w-4" />
              Back to Resumes
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="container mx-auto p-6 max-w-6xl space-y-6 animate-in fade-in duration-500">
      {/* Header Actions */}
      <div className="flex items-center justify-between">
          <Button onClick={() => router.push("/resumes")} variant="outline" className="gap-2">
            <ArrowLeft className="h-4 w-4" />
            Back to List
          </Button>
          <div className="flex gap-2">
            <Button
              onClick={() => setShowDeleteDialog(true)}
              variant="outline"
              className="gap-2 text-destructive hover:text-destructive"
            >
              <Trash2 className="h-4 w-4" />
              Delete
            </Button>
            {!isEditing ? (
              <Button onClick={() => setIsEditing(true)} variant="outline" className="gap-2">
                <Edit2 className="h-4 w-4" />
                Edit
              </Button>
            ) : (
              <>
                <Button onClick={() => setIsEditing(false)} variant="outline">
                  Cancel
                </Button>
                <Button onClick={handleSave} disabled={saving} className="gap-2">
                  <Save className="h-4 w-4" />
                  {saving ? "Saving..." : "Save Changes"}
                </Button>
              </>
            )}
          </div>
        </div>

        {/* Resume Header */}
        <Card className="border-2">
          <CardHeader>
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-primary/10 rounded-full">
                  <User className="h-8 w-8 text-primary" />
                </div>
                <div>
                  <CardTitle className="text-3xl">{resume.name}</CardTitle>
                  <CardDescription className="text-base mt-1">
                    Parsed on {formatDate(resume.parsed_at)}
                  </CardDescription>
                </div>
              </div>
              {resume.source && (
                <Badge variant="secondary" className="gap-1">
                  <Sparkles className="h-3 w-3" />
                  {resume.source}
                </Badge>
              )}
            </div>
          </CardHeader>
        </Card>

        {/* Personal Information */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <User className="h-5 w-5" />
              Personal Information
            </CardTitle>
            <CardDescription>Contact details and professional summary</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="name">Full Name</Label>
                {isEditing ? (
                  <Input
                    id="name"
                    value={resume.name}
                    onChange={(e) => setResume({ ...resume, name: e.target.value })}
                  />
                ) : (
                  <div className="p-2 border rounded-md bg-muted/50">{resume.name}</div>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="email" className="flex items-center gap-2">
                  <Mail className="h-4 w-4" />
                  Email
                </Label>
                {isEditing ? (
                  <Input
                    id="email"
                    type="email"
                    value={resume.contact?.email || ""}
                    onChange={(e) =>
                      setResume({
                        ...resume,
                        contact: { ...resume.contact, email: e.target.value },
                      })
                    }
                  />
                ) : (
                  <div className="p-2 border rounded-md bg-muted/50">
                    {resume.contact?.email || "Not provided"}
                  </div>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="phone" className="flex items-center gap-2">
                  <Phone className="h-4 w-4" />
                  Phone
                </Label>
                {isEditing ? (
                  <Input
                    id="phone"
                    value={resume.contact?.phone || ""}
                    onChange={(e) =>
                      setResume({
                        ...resume,
                        contact: { ...resume.contact, phone: e.target.value },
                      })
                    }
                  />
                ) : (
                  <div className="p-2 border rounded-md bg-muted/50">
                    {resume.contact?.phone || "Not provided"}
                  </div>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="linkedin" className="flex items-center gap-2">
                  <Linkedin className="h-4 w-4" />
                  LinkedIn
                </Label>
                {isEditing ? (
                  <Input
                    id="linkedin"
                    value={resume.contact?.linkedin || ""}
                    onChange={(e) =>
                      setResume({
                        ...resume,
                        contact: { ...resume.contact, linkedin: e.target.value },
                      })
                    }
                  />
                ) : (
                  <div className="p-2 border rounded-md bg-muted/50">
                    {resume.contact?.linkedin || "Not provided"}
                  </div>
                )}
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="summary">Professional Summary</Label>
              {isEditing ? (
                <Textarea
                  id="summary"
                  value={resume.summary || ""}
                  onChange={(e) => setResume({ ...resume, summary: e.target.value })}
                  rows={4}
                  placeholder="Enter professional summary..."
                />
              ) : (
                <div className="p-3 border rounded-md bg-muted/50 min-h-[100px]">
                  {resume.summary || "No summary provided"}
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Skills */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="h-5 w-5" />
              Skills & Expertise
            </CardTitle>
            <CardDescription>
              {resume.skills.length} skills identified
            </CardDescription>
          </CardHeader>
          <CardContent>
            {resume.skills.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {resume.skills.map((skill, idx) => (
                  <Badge key={idx} variant="secondary" className="text-sm py-1 px-3">
                    {skill}
                  </Badge>
                ))}
              </div>
            ) : (
              <p className="text-muted-foreground text-sm">No skills listed</p>
            )}
          </CardContent>
        </Card>

        {/* Experience */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Briefcase className="h-5 w-5" />
              Work Experience
            </CardTitle>
            <CardDescription>
              {resume.experiences.length} position{resume.experiences.length !== 1 ? "s" : ""}
            </CardDescription>
          </CardHeader>
          <CardContent>
            {resume.experiences.length > 0 ? (
              <div className="space-y-6">
                {resume.experiences.map((exp, idx) => (
                  <div key={idx} className="space-y-3">
                    <div>
                      <h3 className="text-lg font-semibold">{exp.title}</h3>
                      <p className="text-muted-foreground font-medium">{exp.company}</p>
                      <div className="flex items-center gap-4 text-sm text-muted-foreground mt-1">
                        <span className="flex items-center gap-1">
                          <Calendar className="h-3 w-3" />
                          {formatDate(exp.start_date)} - {formatDate(exp.end_date)}
                        </span>
                        {exp.location && (
                          <span className="flex items-center gap-1">
                            <MapPin className="h-3 w-3" />
                            {exp.location}
                          </span>
                        )}
                      </div>
                    </div>
                    {exp.responsibilities.length > 0 && (
                      <ul className="list-disc list-inside space-y-1 text-sm">
                        {exp.responsibilities.map((resp, ridx) => (
                          <li key={ridx} className="text-muted-foreground leading-relaxed">
                            {resp}
                          </li>
                        ))}
                      </ul>
                    )}
                    {idx < resume.experiences.length - 1 && <Separator className="mt-6" />}
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-muted-foreground text-sm">No work experience listed</p>
            )}
          </CardContent>
        </Card>

        {/* Education */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <GraduationCap className="h-5 w-5" />
              Education
            </CardTitle>
            <CardDescription>
              {resume.education.length} qualification{resume.education.length !== 1 ? "s" : ""}
            </CardDescription>
          </CardHeader>
          <CardContent>
            {resume.education.length > 0 ? (
              <div className="space-y-4">
                {resume.education.map((edu, idx) => (
                  <div key={idx} className="space-y-1">
                    <h3 className="text-lg font-semibold">{edu.degree}</h3>
                    <p className="text-muted-foreground font-medium">{edu.institution}</p>
                    <p className="text-sm text-muted-foreground flex items-center gap-1">
                      <Calendar className="h-3 w-3" />
                      {formatDate(edu.start_date)} - {formatDate(edu.end_date)}
                    </p>
                    {idx < resume.education.length - 1 && <Separator className="mt-4" />}
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-muted-foreground text-sm">No education listed</p>
            )}
          </CardContent>
        </Card>

        {/* Certifications */}
        {resume.certifications.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Award className="h-5 w-5" />
                Certifications
              </CardTitle>
              <CardDescription>
                {resume.certifications.length} certification{resume.certifications.length !== 1 ? "s" : ""}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {resume.certifications.map((cert, idx) => {
                  const certData = typeof cert === 'string' ? { name: cert } : cert;
                  return (
                    <div key={idx} className="flex items-start gap-3 border-l-2 border-primary pl-4">
                      <CheckCircle2 className="h-5 w-5 text-primary mt-0.5 flex-shrink-0" />
                      <div className="flex-1 space-y-1">
                        <p className="font-semibold">{certData.name}</p>
                        {certData.issuing_organization && (
                          <p className="text-sm text-muted-foreground">
                            {certData.issuing_organization}
                          </p>
                        )}
                        {(certData.issue_date || certData.expiration_date) && (
                          <div className="flex items-center gap-2 text-xs text-muted-foreground">
                            <Calendar className="h-3 w-3" />
                            {certData.issue_date && (
                              <span>Issued: {formatDate(certData.issue_date)}</span>
                            )}
                            {certData.expiration_date && (
                              <span>• Expires: {formatDate(certData.expiration_date)}</span>
                            )}
                          </div>
                        )}
                        {certData.credential_url && (
                          <a 
                            href={certData.credential_url} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="text-xs text-primary hover:underline flex items-center gap-1"
                          >
                            <Globe className="h-3 w-3" />
                            View Credential
                          </a>
                        )}
                        {certData.credential_id && (
                          <p className="text-xs text-muted-foreground">
                            ID: {certData.credential_id}
                          </p>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Delete Confirmation Dialog */}
      <AlertDialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Are you sure?</AlertDialogTitle>
            <AlertDialogDescription>
              This will permanently delete the resume for <strong>{resume?.name || 'Unknown'}</strong>. This action cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel disabled={deleting}>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleDelete}
              disabled={deleting}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              {deleting ? "Deleting..." : "Delete Resume"}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}
