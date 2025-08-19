/**
 * Axios instance with:
 * - Base URL from env (VITE_API_BASE_URL)
 * - Bearer auth from localStorage
 * - Auto refresh on 401 via /auth/refresh
 */
import axios from "axios";
import { getTokens, setTokens, clearAuth } from "./auth";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000",
  withCredentials: false
});

let isRefreshing = false;
let pending: Array<(token: string | null) => void> = [];

function subscribeTokenRefresh(cb: (token: string | null) => void) {
  pending.push(cb);
}
function onRefreshed(token: string | null) {
  pending.forEach((cb) => cb(token));
  pending = [];
}

api.interceptors.request.use((config) => {
  const tokens = getTokens();
  if (tokens?.accessToken) {
    config.headers = config.headers || {};
    (config.headers as any)["Authorization"] = `Bearer ${tokens.accessToken}`;
  }
  return config;
});

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config;
    const status = error?.response?.status;
    if (status === 401 && !original._retry) {
      original._retry = true;
      if (!isRefreshing) {
        isRefreshing = true;
        try {
          const tokens = getTokens();
          if (!tokens?.refreshToken) throw new Error("No refresh token");
          const resp = await axios.post(
            (api.defaults.baseURL || "") + "/auth/refresh",
            { refresh_token: tokens.refreshToken }
          );
          const { access_token, refresh_token } = resp.data;
          setTokens(access_token, refresh_token);
          isRefreshing = false;
          onRefreshed(access_token);
        } catch (e) {
          isRefreshing = false;
          onRefreshed(null);
          clearAuth();
          return Promise.reject(error);
        }
      }
      return new Promise((resolve, reject) => {
        subscribeTokenRefresh((token) => {
          if (!token) {
            reject(error);
            return;
          }
          original.headers["Authorization"] = `Bearer ${token}`;
          resolve(api.request(original));
        });
      });
    }
    return Promise.reject(error);
  }
);

export default api;
