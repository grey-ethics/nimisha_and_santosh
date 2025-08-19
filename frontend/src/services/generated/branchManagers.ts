/**
 * BRANCH MANAGERS endpoints
 * - /patients (GET, POST)
 * - /patients/{user_id} (GET, PATCH)
 * - /patients/{user_id}:deactivate (POST)
 */
import type { AxiosInstance } from "axios";
import type { PatientOut } from "../../types/api";

export async function listPatients(api: AxiosInstance) {
  return api.get<PatientOut[]>("/patients");
}
export async function createPatient(api: AxiosInstance, body: any) {
  return api.post<PatientOut>("/patients", body);
}
export async function getPatient(api: AxiosInstance, user_id: string) {
  return api.get<PatientOut>(`/patients/${user_id}`);
}
export async function updatePatient(api: AxiosInstance, user_id: string, body: any) {
  return api.patch<PatientOut>(`/patients/${user_id}`, body);
}
export async function deactivatePatient(api: AxiosInstance, user_id: string) {
  return api.post(`/patients/${user_id}:deactivate`);
}
