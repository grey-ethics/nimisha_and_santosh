/**
 * Audit log (Admin):
 * - GET /audit
 */
import { useEffect, useState } from "react";
import * as AuditApi from "../../services/generated/audit";
import api from "../../lib/axios";
import DataTable from "../../components/DataTable";

type Audit = {
  id: string;
  actor_user_id: string | null;
  action: string;
  entity_type: string;
  entity_id: string | null;
  timestamp: string;
  ip: string | null;
};

export default function Audit() {
  const [rows, setRows] = useState<Audit[]>([]);
  useEffect(() => {
    (async () => {
      const { data } = await AuditApi.listAudit(api);
      setRows(data);
    })();
  }, []);
  return (
    <div className="space-y-6">
      <h2 className="text-lg font-semibold">Audit</h2>
      <div className="section">
        <DataTable
          rows={rows}
          columns={[
            { key: "timestamp", label: "Time" },
            { key: "actor_user_id", label: "Actor" },
            { key: "action", label: "Action" },
            { key: "entity_type", label: "Entity" },
            { key: "entity_id", label: "Entity ID" },
            { key: "ip", label: "IP" }
          ]}
        />
      </div>
    </div>
  );
}
