/**
 * Patient self profile:
 * - GET /me
 */
import { useEffect, useState } from "react";
import * as MeApi from "../../services/generated/me";
import api from "../../lib/axios";
import { Input, Label } from "../../components/Form";
import type { UserOut } from "../../types/api";

export default function Profile() {
  const [me, setMe] = useState<UserOut | null>(null);
  useEffect(() => { (async () => setMe((await MeApi.getMe(api)).data))(); }, []);
  if (!me) return null;
  return (
    <div className="section grid gap-3 md:grid-cols-2">
      <div><Label>ID</Label><Input readOnly value={me.id} /></div>
      <div><Label>Role</Label><Input readOnly value={me.role} /></div>
      <div><Label>Phone</Label><Input readOnly value={me.phone} /></div>
      <div><Label>Full Name</Label><Input readOnly value={me.full_name ?? ""} /></div>
      <div><Label>Email</Label><Input readOnly value={me.email ?? ""} /></div>
      <div><Label>Active</Label><Input readOnly value={me.is_active ? "Yes" : "No"} /></div>
    </div>
  );
}
