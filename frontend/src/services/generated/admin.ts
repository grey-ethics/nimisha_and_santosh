/**
 * ADMIN endpoints
 * - /admin/regions (GET, POST)
 * - /admin/branches (GET with region_id, POST)
 * - /admin/users/regional-managers (GET, POST)
 * - /admin/users/regional-managers/{user_id} (PATCH)
 * - /admin/users/regional-managers/{user_id}:deactivate (POST)
 */
import type { AxiosInstance } from "axios";
import type { RegionCreate, RegionOut, BranchCreate, BranchOut, UserOut } from "../../types/api";

export async function listRegions(api: AxiosInstance) {
  return api.get<RegionOut[]>("/admin/regions");
}
export async function createRegion(api: AxiosInstance, body: RegionCreate) {
  return api.post<RegionOut>("/admin/regions", body);
}

export async function listBranches(api: AxiosInstance, params: { region_id: string }) {
  return api.get<BranchOut[]>("/admin/branches", { params });
}
export async function createBranch(api: AxiosInstance, body: BranchCreate) {
  return api.post<BranchOut>("/admin/branches", body);
}

export async function listRms(api: AxiosInstance) {
  return api.get<UserOut[]>("/admin/users/regional-managers");
}
export async function createRm(api: AxiosInstance, body: {
  phone: string; password: string; full_name?: string | null; email?: string | null; region_id: string; notes?: string | null;
}) {
  return api.post<UserOut>("/admin/users/regional-managers", body);
}
export async function patchRm(api: AxiosInstance, user_id: string, body: {
  full_name?: string | null; email?: string | null; region_id?: string | null; notes?: string | null;
}) {
  return api.patch<UserOut>(`/admin/users/regional-managers/${user_id}`, body);
}
export async function deactivateRm(api: AxiosInstance, user_id: string) {
  return api.post(`/admin/users/regional-managers/${user_id}:deactivate`);
}
