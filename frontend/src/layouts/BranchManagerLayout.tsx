/**
 * Branch Manager layout:
 * - Patients in branch
 */
import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";

export default function BranchManagerLayout() {
  return (
    <div className="flex">
      <Sidebar
        title="Branch Manager"
        items={[{ label: "Patients", to: "/bm/patients" }]}
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
