/**
 * AUTH endpoints
 * - /auth/login
 * - /auth/refresh
 * - /auth/change-password
 * - /auth/logout
 */
import type { AxiosInstance } from "axios";

export type LoginRequest = { phone: string; password: string };
export type TokenPair = {
  access_token: string;
  refresh_token: string;
  token_type?: string;
  must_change_password?: boolean;
};
export type RefreshRequest = { refresh_token: string };
export type ChangePasswordRequest = { current_password?: string | null; new_password: string };

export async function login(api: AxiosInstance, body: LoginRequest) {
  return api.post<TokenPair>("/auth/login", body);
}
export async function refresh(api: AxiosInstance, body: RefreshRequest) {
  return api.post<TokenPair>("/auth/refresh", body);
}
export async function changePassword(api: AxiosInstance, body: ChangePasswordRequest) {
  return api.post("/auth/change-password", body);
}
export async function logout(api: AxiosInstance) {
  return api.post("/auth/logout");
}
