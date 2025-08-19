/**
 * Placeholder GET /patient/orders
 */
import api from "../../lib/axios";
import { useEffect, useState } from "react";

export default function Orders() {
  const [ok, setOk] = useState(false);
  useEffect(() => { (async () => { await api.get("/patient/orders"); setOk(true); })(); }, []);
  return <div className="section">{ok ? "Orders placeholder loaded." : "Loading..."}</div>;
}
