/**
 * Admin layout with sidebar:
 * - Regions, Branches, Regional Managers, Audit
 */
import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";

export default function AdminLayout() {
  return (
    <div className="flex">
      <Sidebar
        title="Admin"
        items={[
          { label: "Regions", to: "/admin/regions" },
          { label: "Branches", to: "/admin/branches" },
          { label: "Regional Managers", to: "/admin/regional-managers" },
          { label: "Audit", to: "/admin/audit" },
        ]}
      />
      <div className="flex-1 min-h-screen">
        <Header />
        <main className="max-w-7xl mx-auto p-4">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
