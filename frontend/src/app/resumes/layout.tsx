import DashboardLayout from "../dashboard/layout"

export default function ResumesLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return <DashboardLayout>{children}</DashboardLayout>
}
