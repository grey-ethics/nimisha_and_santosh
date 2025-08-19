/**
 * REGIONAL MANAGERS endpoints
 * - /users/branch-managers (GET, POST)
 * - /users/branch-managers/{user_id} (PATCH)
 * - /users/branch-managers/{user_id}:deactivate (POST)
 * - /users/patients (GET)
 */
import type { AxiosInstance } from "axios";
import type { UserOut, PatientOut } from "../../types/api";

export async function listBms(api: AxiosInstance) {
  return api.get<UserOut[]>("/users/branch-managers");
}
export async function createBm(api: AxiosInstance, body: {
  phone: string; password: string; full_name?: string | null; email?: string | null; branch_id: string; notes?: string | null;
}) {
  return api.post<UserOut>("/users/branch-managers", body);
}
export async function patchBm(api: AxiosInstance, user_id: string, body: {
  full_name?: string | null; email?: string | null; branch_id?: string | null; notes?: string | null;
}) {
  return api.patch<UserOut>(`/users/branch-managers/${user_id}`, body);
}
export async function deactivateBm(api: AxiosInstance, user_id: string) {
  return api.post(`/users/branch-managers/${user_id}:deactivate`);
}
export async function listPatientsRegion(api: AxiosInstance) {
  return api.get<PatientOut[]>("/users/patients");
}
