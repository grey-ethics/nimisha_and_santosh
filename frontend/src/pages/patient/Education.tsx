/**
 * Placeholder GET /patient/education
 */
import api from "../../lib/axios";
import { useEffect, useState } from "react";

export default function Education() {
  const [ok, setOk] = useState(false);
  useEffect(() => { (async () => { await api.get("/patient/education"); setOk(true); })(); }, []);
  return <div className="section">{ok ? "Education placeholder loaded." : "Loading..."}</div>;
}
