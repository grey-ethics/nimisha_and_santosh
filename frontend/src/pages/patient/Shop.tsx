/**
 * Placeholder GET /patient/shop
 * - The backend returns {} for now.
 */
import api from "../../lib/axios";
import { useEffect, useState } from "react";

export default function Shop() {
  const [ok, setOk] = useState(false);
  useEffect(() => { (async () => { await api.get("/patient/shop"); setOk(true); })(); }, []);
  return <div className="section">{ok ? "Shop placeholder loaded." : "Loading..."}</div>;
}
