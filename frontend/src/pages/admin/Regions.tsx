/**
 * Regions management (Admin):
 * - GET /admin/regions
 * - POST /admin/regions
 */
import { useEffect, useState } from "react";
import * as AdminApi from "../../services/generated/admin";
import api from "../../lib/axios";
import DataTable from "../../components/DataTable";
import { Input, Primary, Label, Button } from "../../components/Form";
import type { RegionOut } from "../../types/api";

export default function Regions() {
  const [rows, setRows] = useState<RegionOut[]>([]);
  const [name, setName] = useState("");
  const [busy, setBusy] = useState(false);

  const load = async () => {
    const { data } = await AdminApi.listRegions(api);
    setRows(data);
  };

  useEffect(() => { load(); }, []);

  const create = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;
    setBusy(true);
    try {
      await AdminApi.createRegion(api, { name });
      setName("");
      await load();
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="space-y-6">
      <h2 className="text-lg font-semibold">Regions</h2>
      <form onSubmit={create} className="section flex items-end gap-3">
        <div className="flex-1">
          <Label>Name</Label>
          <Input value={name} onChange={(e)=>setName(e.target.value)} placeholder="e.g., North Zone" required />
        </div>
        <Primary type="submit" disabled={busy}>{busy ? "Creating..." : "Create"}</Primary>
      </form>

      <div className="section">
        <DataTable
          rows={rows}
          columns={[
            { key: "id", label: "ID" },
            { key: "name", label: "Name" },
            { key: "is_active", label: "Active" }
          ]}
        />
        <div className="mt-3 text-xs text-gray-500">To deactivate a region, use server-side admin operations if added later.</div>
      </div>
    </div>
  );
}
