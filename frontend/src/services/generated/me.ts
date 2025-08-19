/**
 * GET /me -> UserOut
 */
import type { AxiosInstance } from "axios";
import type { UserOut } from "../../types/api";

export async function getMe(api: AxiosInstance) {
  return api.get<UserOut>("/me");
}
