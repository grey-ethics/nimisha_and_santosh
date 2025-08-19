/**
 * Regional Manager layout:
 * - Branch Managers & Patients in region
 */
import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";

export default function RegionalManagerLayout() {
  return (
    <div className="flex">
      <Sidebar
        title="Regional Manager"
        items={[
          { label: "Branch Managers", to: "/rm/branch-managers" },
          { label: "Patients", to: "/rm/patients" }
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
