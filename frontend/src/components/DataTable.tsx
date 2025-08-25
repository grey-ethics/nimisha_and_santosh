/**
 * Minimal data table for lists.
 * - columns: [{key,label,render?}]
 */
import React from "react";

export type Column<T> = {
  key: keyof T | string;
  label: string;
  render?: (row: T) => React.ReactNode;
};

export default function DataTable<T extends object>({
  rows, columns, empty = "No data"
}: { rows: T[]; columns: Column<T>[]; empty?: string }) {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full text-sm">
        <thead>
          <tr className="text-left bg-office-blue text-white">
            {columns.map((c) => <th key={String(c.key)} className="px-3 py-2 font-medium">{c.label}</th>)}
          </tr>
        </thead>
        <tbody>
          {rows.length === 0 && (
            <tr><td className="px-3 py-6 text-office-blue-dark" colSpan={columns.length}>{empty}</td></tr>
          )}
          {rows.map((r, i) => (
            <tr key={i} className="border-t">
              {columns.map((c) => (
                <td key={String(c.key)} className="px-3 py-2">
                  {c.render ? c.render(r) : (r as any)[c.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
