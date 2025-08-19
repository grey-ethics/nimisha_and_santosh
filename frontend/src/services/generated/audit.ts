/**
 * Audit list
 * - /audit (GET)
 */
import type { AxiosInstance } from "axios";

export async function listAudit(api: AxiosInstance) {
  return api.get("/audit");
}
