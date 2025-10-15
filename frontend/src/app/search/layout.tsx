import DashboardLayout from "../dashboard/layout"

export default function SearchLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return <DashboardLayout>{children}</DashboardLayout>
}
