/**
 * Login page:
 * - POST /auth/login { phone, password }
 * - On success, redirect by role; if must_change_password, go to change-password.
 */
import { useState } from "react";
import { Input, Primary, Label } from "../components/Form";
import { useAuth } from "../store/authStore";

export default function Login() {
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const { login } = useAuth();

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    try {
      await login(phone, password);
    } catch (err: any) {
      alert(err?.response?.data?.detail ?? "Login failed");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="min-h-screen grid place-items-center p-4">
      <form onSubmit={submit} className="section w-full max-w-md space-y-4">
        <div className="text-center">
          <h2 className="text-xl font-semibold">Sign in</h2>
          <p className="text-gray-600 text-sm">Use your phone and password</p>
        </div>
        <div>
          <Label>Phone</Label>
          <Input placeholder="+91..." value={phone} onChange={(e)=>setPhone(e.target.value)} required />
        </div>
        <div>
          <Label>Password</Label>
          <Input type="password" value={password} onChange={(e)=>setPassword(e.target.value)} required />
        </div>
        <Primary disabled={busy} type="submit" className="w-full">{busy ? "Signing in..." : "Sign in"}</Primary>
      </form>
    </div>
  );
}
