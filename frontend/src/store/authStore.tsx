/**
 * Lightweight auth store using React Context.
 * - Holds tokens, current user (/me), and booting state.
 * - Exposes login, logout, refreshMe.
 */
import React, { createContext, useContext, useEffect, useMemo, useState } from "react";
import api from "../lib/axios";
import { clearAuth, getTokens, setTokens } from "../lib/auth";
import * as AuthApi from "../services/generated/auth";
import * as MeApi from "../services/generated/me";
import type { UserOut, Role } from "../types/api";
import { useNavigate } from "react-router-dom";

type State = {
  tokens: { accessToken: string; refreshToken: string } | null;
  me: UserOut | null;
};

type Ctx = {
  state: State;
  isBooting: boolean;
  login: (phone: string, password: string) => Promise<UserOut>;
  logout: () => void;
  refreshMe: () => Promise<UserOut | null>;
  routeByRole: (role: Role) => string;
};

const AuthContext = createContext<Ctx>({} as any);

// Minimal JWT payload decoder (no verification; just UI convenience)
function decodeJwt<T = any>(token: string): T {
  try {
    const [, payload] = token.split(".");
    return JSON.parse(atob(payload));
  } catch {
    return {} as T;
  }
}

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<State>({ tokens: getTokens(), me: null });
  const [isBooting, setBooting] = useState(true);
  const nav = useNavigate();

  const routeByRole = (role: Role) =>
    role === "ADMIN" ? "/admin" :
    role === "REGIONAL_MANAGER" ? "/rm" :
    role === "BRANCH_MANAGER" ? "/bm" :
    "/patient";

  const refreshMe = async () => {
    try {
      const { data } = await MeApi.getMe(api);
      setState((s) => ({ ...s, me: data }));
      return data;
    } catch {
      return null;
    }
  };

  const login = async (phone: string, password: string) => {
    const { data } = await AuthApi.login(api, { phone, password });

    // Store tokens immediately
    setTokens(data.access_token, data.refresh_token);

    // If password change is required, DON'T call /me yet (server forbids it until changed).
    if (data.must_change_password) {
      const claims = decodeJwt<{ sub?: string; role?: Role }>(data.access_token);
      const meStub: UserOut = {
        id: claims.sub ?? "unknown",
        role: (claims.role ?? "PATIENT") as Role,
        phone: phone,
        full_name: null,
        email: null,
        is_active: true,
        must_change_password: true,
      };
      setState({ tokens: { accessToken: data.access_token, refreshToken: data.refresh_token }, me: meStub });
      nav("/change-password", { replace: true });
      return meStub;
    }

    // Normal flow: fetch profile then route by role
    setState({ tokens: { accessToken: data.access_token, refreshToken: data.refresh_token }, me: null });
    const me = await refreshMe();
    if (!me) throw new Error("Failed to fetch profile after login.");
    nav(routeByRole(me.role), { replace: true });
    return me;
  };

  const logout = () => {
    clearAuth();
    setState({ tokens: null, me: null });
    nav("/login", { replace: true });
  };

  useEffect(() => {
    // Boot: if tokens exist, try to load /me; otherwise we're done.
    (async () => {
      if (state.tokens?.accessToken) {
        await refreshMe().catch(() => {});
      }
      setBooting(false);
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const value = useMemo(() => ({ state, isBooting, login, logout, refreshMe, routeByRole }), [state, isBooting]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);
