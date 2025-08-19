/**
 * Branches (Admin):
 * - GET /admin/branches?region_id=
 * - POST /admin/branches
 */
import { useEffect, useState } from "react";
import * as AdminApi from "../../services/generated/admin";
import api from "../../lib/axios";
import DataTable from "../../components/DataTable";
import { Input, Primary, Label, Select } from "../../components/Form";
import type { RegionOut, BranchOut } from "../../types/api";

export default function Branches() {
  const [regions, setRegions] = useState<RegionOut[]>([]);
  const [regionId, setRegionId] = useState<string>("");
  const [rows, setRows] = useState<BranchOut[]>([]);
  const [name, setName] = useState("");
  const [address, setAddress] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    (async () => {
      const { data } = await AdminApi.listRegions(api);
      setRegions(data);
      if (data[0]) setRegionId(data[0].id);
    })();
  }, []);

  const load = async () => {
    if (!regionId) return;
    const { data } = await AdminApi.listBranches(api, { region_id: regionId });
    setRows(data);
  };

  useEffect(() => { load(); }, [regionId]);

  const create = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!regionId || !name.trim()) return;
    setBusy(true);
    try {
      await AdminApi.createBranch(api, { region_id: regionId, name, address: address || null });
      setName(""); setAddress("");
      await load();
    } finally { setBusy(false); }
  };

  return (
    <div className="space-y-6">
      <h2 className="text-lg font-semibold">Branches</h2>
      <div className="section space-y-3">
        <div>
          <Label>Region</Label>
          <Select value={regionId} onChange={(e)=>setRegionId(e.target.value)}>
            {regions.map(r => <option key={r.id} value={r.id}>{r.name}</option>)}
          </Select>
        </div>
      </div>

      <form onSubmit={create} className="section grid gap-3 md:grid-cols-3">
        <div>
          <Label>Branch Name</Label>
          <Input value={name} onChange={(e)=>setName(e.target.value)} required />
        </div>
        <div className="md:col-span-2">
          <Label>Address</Label>
          <Input value={address} onChange={(e)=>setAddress(e.target.value)} placeholder="Optional"/>
        </div>
        <div className="md:col-span-3">
          <Primary disabled={busy} type="submit">{busy ? "Creating..." : "Create Branch"}</Primary>
        </div>
      </form>

      <div className="section">
        <DataTable
          rows={rows}
          columns={[
            { key: "id", label: "ID" },
            { key: "name", label: "Name" },
            { key: "address", label: "Address" },
            { key: "is_active", label: "Active" }
          ]}
        />
      </div>
    </div>
  );
}
