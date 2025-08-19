/**
 * BM Patients (full CRUD):
 * - GET /patients
 * - POST /patients
 * - GET /patients/{user_id}
 * - PATCH /patients/{user_id}
 * - POST /patients/{user_id}:deactivate
 */
import { useEffect, useState } from "react";
import * as BmApi from "../../services/generated/branchManagers";
import api from "../../lib/axios";
import DataTable from "../../components/DataTable";
import { Input, Primary, Label, Select, Textarea, Button } from "../../components/Form";
import type { PatientOut, PatientStatus, Gender, DonorType } from "../../types/api";

export default function BMPatients() {
  const [rows, setRows] = useState<PatientOut[]>([]);

  // Minimal create form; the backend requires: branch_id, assigned_bm_user_id, phone, password
  const [form, setForm] = useState({
    branch_id: "",
    assigned_bm_user_id: "",
    phone: "",
    password: "",
    full_name: "",
    email: "",
    notes: ""
  });

  useEffect(() => { load(); }, []);
  const load = async () => setRows((await BmApi.listPatients(api)).data);

  const create = async (e: React.FormEvent) => {
    e.preventDefault();
    await BmApi.createPatient(api, {
      branch_id: form.branch_id,
      assigned_bm_user_id: form.assigned_bm_user_id,
      phone: form.phone,
      password: form.password,
      full_name: form.full_name || null,
      email: form.email || null,
      rm_approval: false,
      notes: form.notes || null
    } as any);
    setForm({ ...form, phone: "", password: "", full_name: "", email: "", notes: "" });
    await load();
  };

  const deactivate = async (userId: string) => {
    await BmApi.deactivatePatient(api, userId);
    await load();
  };

  return (
    <div className="space-y-6">
      <h2 className="text-lg font-semibold">Patients</h2>

      <form onSubmit={create} className="section grid md:grid-cols-3 gap-3">
        <div><Label>Branch ID</Label><Input value={form.branch_id} onChange={e=>setForm({...form, branch_id:e.target.value})} required/></div>
        <div><Label>Assigned BM User ID</Label><Input value={form.assigned_bm_user_id} onChange={e=>setForm({...form, assigned_bm_user_id:e.target.value})} required/></div>
        <div><Label>Phone</Label><Input value={form.phone} onChange={e=>setForm({...form, phone:e.target.value})} required/></div>
        <div><Label>Password</Label><Input type="password" value={form.password} onChange={e=>setForm({...form, password:e.target.value})} required/></div>
        <div><Label>Full Name</Label><Input value={form.full_name} onChange={e=>setForm({...form, full_name:e.target.value})}/></div>
        <div><Label>Email</Label><Input type="email" value={form.email} onChange={e=>setForm({...form, email:e.target.value})}/></div>
        <div className="md:col-span-3"><Label>Notes</Label><Textarea value={form.notes} onChange={e=>setForm({...form, notes:e.target.value})}/></div>
        <div className="md:col-span-3"><Primary type="submit">Create Patient</Primary></div>
      </form>

      <div className="section">
        <DataTable
          rows={rows}
          columns={[
            { key: "user_id", label: "User ID" },
            { key: "status", label: "Status" },
            { key: "rm_approval", label: "RM Approved" },
            { key: "blood_group", label: "Blood Group" },
            {
              key: "actions", label: "Actions",
              render: (p) => <Button onClick={()=>deactivate(p.user_id)}>Deactivate</Button>
            }
          ]}
        />
      </div>
    </div>
  );
}
