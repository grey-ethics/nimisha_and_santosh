/**
 * Small role badge.
 */
export default function RoleBadge({ role }: { role: string }) {
  const color =
    role === "ADMIN" ? "bg-office-blue-100 text-office-blue-700" :
    role === "REGIONAL_MANAGER" ? "bg-office-red-100 text-office-red-700" :
    role === "BRANCH_MANAGER" ? "bg-office-red-50 text-office-red-700" :
    "bg-office-blue-50 text-office-blue-700";
  return <span className={`text-xs px-2 py-1 rounded ${color}`}>{role}</span>;
}
