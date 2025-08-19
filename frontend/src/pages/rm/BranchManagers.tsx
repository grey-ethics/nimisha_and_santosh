/**
 * Branch Managers (Regional Manager):
 * - GET /users/branch-managers
 * - POST /users/branch-managers
 * - PATCH /users/branch-managers/{user_id}
 * - POST /users/branch-managers/{user_id}:deactivate
 */
import { useEffect, useState } from "react";
import * as RMApi from "../../services/generated/regionalManagers";
import * as AdminApi from "../../services/generated/admin";
import api from "../../lib/axios";
import DataTable from "../../components/DataTable";
import { Input, Primary, Label, Select, Button } from "../../components/Form";
import type { BranchOut, UserOut } from "../../types/api";

export default function RMBranchManagers() {
  const [branches, setBranches] = useState<BranchOut[]>([]);
  const [rows, setRows] = useState<UserOut[]>([]);
  const [form, setForm] = useState({ phone: "", password: "", full_name: "", email: "", branch_id: "" });

  const load = async () => {
    // Need branches in RM's region: backend exposes /admin/branches?region_id=...
    // We don't have the region id directly; typically RM belongs to a region.
    // For demo, we'll fetch all regions & first region's branches (you can customize).
    const regions = (await AdminApi.listRegions(api)).data;
    if (regions[0]) {
      const bs = (await AdminApi.listBranches(api, { region_id: regions[0].id })).data;
      setBranches(bs);
      if (!form.branch_id && bs[0]) setForm((f)=>({ ...f, branch_id: bs[0].id }));
    }
    setRows((await RMApi.listBms(api)).data);
  };

  useEffect(() => { load(); }, []);

  const create = async (e: React.FormEvent) => {
    e.preventDefault();
    await RMApi.createBm(api, {
      phone: form.phone,
      password: form.password,
      full_name: form.full_name || null,
      email: form.email || null,
      branch_id: form.branch_id,
      notes: null
    });
    setForm({ phone: "", password: "", full_name: "", email: "", branch_id: form.branch_id });
    await load();
  };

  const deactivate = async (id: string) => { await RMApi.deactivateBm(api, id); await load(); };

  return (
    <div className="space-y-6">
      <h2 className="text-lg font-semibold">Branch Managers</h2>

      <form onSubmit={create} className="section grid gap-3 md:grid-cols-3">
        <div><Label>Phone</Label><Input value={form.phone} onChange={e=>setForm({...form, phone:e.target.value})} required/></div>
        <div><Label>Password</Label><Input type="password" value={form.password} onChange={e=>setForm({...form, password:e.target.value})} required/></div>
        <div><Label>Full Name</Label><Input value={form.full_name} onChange={e=>setForm({...form, full_name:e.target.value})}/></div>
        <div><Label>Email</Label><Input type="email" value={form.email} onChange={e=>setForm({...form, email:e.target.value})}/></div>
        <div>
          <Label>Branch</Label>
          <Select value={form.branch_id} onChange={e=>setForm({...form, branch_id:e.target.value})}>
            {branches.map(b => <option key={b.id} value={b.id}>{b.name}</option>)}
          </Select>
        </div>
        <div className="md:col-span-3">
          <Primary type="submit">Create Branch Manager</Primary>
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
            { key: "actions", label: "Actions", render: (u) => <Button onClick={()=>deactivate(u.id)}>Deactivate</Button> }
          ]}
        />
      </div>
    </div>
  );
}
