/**
 * Patient layout:
 * - Profile, Shop, Orders, Education
 */
import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";

export default function PatientLayout() {
  return (
    <div className="flex">
      <Sidebar
        title="Patient"
        items={[
          { label: "Profile", to: "/patient/profile" },
          { label: "Shop", to: "/patient/shop" },
          { label: "Orders", to: "/patient/orders" },
          { label: "Education", to: "/patient/education" }
        ]}
      />
      <div className="flex-1 min-h-screen">
        <Header />
        <main className="max-w-5xl mx-auto p-4">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
