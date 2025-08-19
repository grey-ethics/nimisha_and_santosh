/**
 * Local auth helpers.
 * - Stores tokens in localStorage.
 * - Simple encode/decode helpers for safety.
 */
const KEY = "kidneytx.auth";

export type Tokens = {
  accessToken: string;
  refreshToken: string;
};

export function getTokens(): Tokens | null {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return null;
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function setTokens(access: string, refresh: string) {
  localStorage.setItem(KEY, JSON.stringify({ accessToken: access, refreshToken: refresh }));
}

export function clearAuth() {
  localStorage.removeItem(KEY);
}
