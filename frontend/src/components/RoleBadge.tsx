/**
 * Small role badge.
 */
export default function RoleBadge({ role }: { role: string }) {
  const color =
    role === "ADMIN" ? "bg-purple-100 text-purple-700" :
    role === "REGIONAL_MANAGER" ? "bg-emerald-100 text-emerald-700" :
    role === "BRANCH_MANAGER" ? "bg-amber-100 text-amber-700" :
    "bg-sky-100 text-sky-700";
  return <span className={`text-xs px-2 py-1 rounded ${color}`}>{role}</span>;
}
