/**
 * Change password page:
 * - POST /auth/change-password { current_password?, new_password }
 */
import { useState } from "react";
import { Input, Primary, Label } from "../components/Form";
import api from "../lib/axios";
import { useAuth } from "../store/authStore";
import * as MeApi from "../services/generated/me";

export default function ChangePassword() {
  const [current, setCurrent] = useState("");
  const [next, setNext] = useState("");
  const [busy, setBusy] = useState(false);
  const { routeByRole } = useAuth();

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    try {
      await api.post("/auth/change-password", { current_password: current || null, new_password: next });
      alert("Password changed!");

      // After change, server clears must_change_password; now /me works.
      const { data: me } = await MeApi.getMe(api);
      location.href = routeByRole(me.role);
    } catch (err: any) {
      alert(err?.response?.data?.detail ?? "Change password failed");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="min-h-screen grid place-items-center p-4">
      <form onSubmit={submit} className="section w-full max-w-md space-y-4">
        <div className="text-center">
          <h2 className="text-xl font-semibold">Change password</h2>
        </div>
        <div>
          <Label>Current password (may be optional)</Label>
          <Input type="password" value={current} onChange={(e)=>setCurrent(e.target.value)} />
        </div>
        <div>
          <Label>New password (min 8 chars)</Label>
          <Input type="password" value={next} onChange={(e)=>setNext(e.target.value)} required minLength={8}/>
        </div>
        <Primary disabled={busy} type="submit" className="w-full">{busy ? "Saving..." : "Save"}</Primary>
      </form>
    </div>
  );
}
