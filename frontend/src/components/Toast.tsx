/**
 * Minimal toast:
 * - Uses a global event to emit messages: window.dispatchEvent(new CustomEvent('toast',{detail:'Saved!'}))
 * - Keeps code simple without extra deps.
 */
import { useEffect, useState } from "react";

export default function Toast() {
  const [msg, setMsg] = useState<string | null>(null);
  useEffect(() => {
    const onToast = (e: Event) => setMsg((e as CustomEvent<string>).detail);
    window.addEventListener("toast", onToast as any);
    const t = setInterval(() => { /* no-op: keep component alive */ }, 60000);
    return () => { window.removeEventListener("toast", onToast as any); clearInterval(t); };
  }, []);
  useEffect(() => { if (msg) setTimeout(() => setMsg(null), 2500); }, [msg]);
  if (!msg) return null;
  return (
    <div className="fixed bottom-6 inset-x-0 grid place-items-center pointer-events-none">
      <div className="pointer-events-auto bg-office-blue-dark text-white px-4 py-2 rounded-xl shadow">{msg}</div>
    </div>
  );
}

export function toast(text: string) {
  window.dispatchEvent(new CustomEvent("toast", { detail: text }));
}
