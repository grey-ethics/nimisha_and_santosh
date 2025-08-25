/**
 * Role-aware sidebar.
 * - Accepts items [{label, to}] and renders nav.
 */
import { NavLink } from "react-router-dom";

type Item = { label: string; to: string };
export default function Sidebar({ title, items }: { title: string; items: Item[] }) {
  return (
    <aside className="w-[var(--sidebar-w)] min-h-screen bg-office-blue text-white border-r border-red-500">
      <div className="p-4 border-b border-red-500">
        <h1 className="font-bold text-xl text-red-200">{title}</h1>
      </div>
      <nav className="p-2 flex flex-col gap-1">
        {items.map((it) => (
          <NavLink
            key={it.to}
            to={it.to}
            className={({ isActive }) =>
              `px-3 py-2 rounded-lg hover:bg-office-blue-dark ${isActive ? "bg-office-blue-dark font-semibold text-red-200" : ""}`
            }
          >
            {it.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
