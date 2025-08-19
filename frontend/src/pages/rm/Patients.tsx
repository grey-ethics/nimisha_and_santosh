/**
 * RM Patients (read-only list in region):
 * - GET /users/patients
 */
import { useEffect, useState } from "react";
import * as RMApi from "../../services/generated/regionalManagers";
import api from "../../lib/axios";
import DataTable from "../../components/DataTable";
import type { PatientOut } from "../../types/api";

export default function RMPatients() {
  const [rows, setRows] = useState<PatientOut[]>([]);
  useEffect(() => { (async () => setRows((await RMApi.listPatientsRegion(api)).data))(); }, []);
  return (
    <div className="space-y-6">
      <h2 className="text-lg font-semibold">Patients (Region)</h2>
      <div className="section">
        <DataTable
          rows={rows}
          columns={[
            { key: "user_id", label: "User ID" },
            { key: "status", label: "Status" },
            { key: "rm_approval", label: "RM Approved" },
            { key: "mrn", label: "MRN" },
            { key: "blood_group", label: "Blood Group" }
          ]}
        />
      </div>
    </div>
  );
}
