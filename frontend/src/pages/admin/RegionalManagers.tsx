/**
 * Regional Managers (Admin):
 * - GET /admin/users/regional-managers
 * - POST /admin/users/regional-managers
 * - PATCH /admin/users/regional-managers/{user_id}
 * - POST /admin/users/regional-managers/{user_id}:deactivate
 */
import { useEffect, useState } from "react";
import * as AdminApi from "../../services/generated/admin";
import api from "../../lib/axios";
import DataTable from "../../components/DataTable";
import { Input, Primary, Label, Select, Button } from "../../components/Form";
import type { RegionOut, UserOut } from "../../types/api";

export default function RegionalManagers() {
  const [regions, setRegions] = useState<RegionOut[]>([]);
  const [rows, setRows] = useState<UserOut[]>([]);
  const [form, setForm] = useState({ phone: "", password: "", full_name: "", email: "", region_id: "" });
  const [busy, setBusy] = useState(false);

  const load = async () => {
    const [r1, r2] = await Promise.all([AdminApi.listRegions(api), AdminApi.listRms(api)]);
    setRegions(r1.data);
    setRows(r2.data);
    if (!form.region_id && r1.data[0]) setForm((f) => ({ ...f, region_id: r1.data[0].id }));
  };

  useEffect(() => { load(); }, []);

  const create = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    try {
      await AdminApi.createRm(api, {
        phone: form.phone,
        password: form.password,
        full_name: form.full_name || null,
        email: form.email || null,
        region_id: form.region_id,
        notes: null
      });
      setForm({ phone: "", password: "", full_name: "", email: "", region_id: form.region_id });
      await load();
    } finally { setBusy(false); }
  };

  const deactivate = async (id: string) => {
    await AdminApi.deactivateRm(api, id);
    await load();
  };

  return (
    <div className="space-y-6">
      <h2 className="text-lg font-semibold">Regional Managers</h2>
      <form onSubmit={create} className="section grid gap-3 md:grid-cols-3">
        <div><Label>Phone</Label><Input value={form.phone} onChange={e=>setForm({...form, phone:e.target.value})} required/></div>
        <div><Label>Password</Label><Input type="password" value={form.password} onChange={e=>setForm({...form, password:e.target.value})} required/></div>
        <div><Label>Full Name</Label><Input value={form.full_name} onChange={e=>setForm({...form, full_name:e.target.value})}/></div>
        <div><Label>Email</Label><Input type="email" value={form.email} onChange={e=>setForm({...form, email:e.target.value})}/></div>
        <div>
          <Label>Region</Label>
          <Select value={form.region_id} onChange={e=>setForm({...form, region_id:e.target.value})}>
            {regions.map(r => <option value={r.id} key={r.id}>{r.name}</option>)}
          </Select>
        </div>
        <div className="md:col-span-3">
          <Primary disabled={busy} type="submit">{busy ? "Creating..." : "Create RM"}</Primary>
        </div>
      </form>

      <div className="section">
        <DataTable
          rows={rows}
          columns={[
            { key: "id", label: "ID" },
            { key: "full_name", label: "Name" },
            { key: "phone", label: "Phone" },
            { key: "email", label: "Email" },
            { key: "is_active", label: "Active" },
            {
              key: "actions",
              label: "Actions",
              render: (u) => (
                <div className="flex gap-2">
                  <Button onClick={() => deactivate(u.id)}>Deactivate</Button>
                </div>
              )
            }
          ]}
        />
      </div>
    </div>
  );
}
