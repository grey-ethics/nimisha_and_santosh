/**
 * Role-aware sidebar.
 * - Accepts items [{label, to}] and renders nav.
 */
import { NavLink } from "react-router-dom";

type Item = { label: string; to: string };
export default function Sidebar({ title, items }: { title: string; items: Item[] }) {
  return (
    <aside className="w-[var(--sidebar-w)] min-h-screen bg-white border-r">
      <div className="p-4 border-b">
        <h1 className="font-bold text-xl">{title}</h1>
      </div>
      <nav className="p-2 flex flex-col gap-1">
        {items.map((it) => (
          <NavLink
            key={it.to}
            to={it.to}
            className={({ isActive }) =>
              `px-3 py-2 rounded-lg hover:bg-gray-100 ${isActive ? "bg-gray-100 font-semibold" : ""}`
            }
          >
            {it.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
