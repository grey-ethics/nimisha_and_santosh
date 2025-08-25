/**
 * Simple header with user info and logout.
 */
import { useAuth } from "../store/authStore";
import RoleBadge from "./RoleBadge";

export default function Header() {
  const { state, logout } = useAuth();
  const me = state.me;
  return (
    <header className="sticky top-0 z-10 bg-white border-b">
      <div className="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between">
        <div className="font-semibold">KidneyTx Pharma Portal</div>
        <div className="flex items-center gap-3">
          {me && <RoleBadge role={me.role} />}
          <span className="text-sm text-gray-600">{me?.full_name ?? me?.phone}</span>
          <button onClick={logout} className="text-sm px-3 py-1.5 border rounded-lg hover:bg-gray-50">Logout</button>
        </div>
      </div>
    </header>
  );
}
