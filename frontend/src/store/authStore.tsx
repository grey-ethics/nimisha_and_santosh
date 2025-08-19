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
    setTokens(data.access_token, data.refresh_token);
    setState({ tokens: { accessToken: data.access_token, refreshToken: data.refresh_token }, me: null });
    const me = await refreshMe();
    if (!me) throw new Error("Failed to fetch profile after login.");
    if (data.must_change_password || me.must_change_password) {
      nav("/change-password", { replace: true });
    } else {
      nav(routeByRole(me.role), { replace: true });
    }
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
        await refreshMe();
      }
      setBooting(false);
    })();
  }, []);

  const value = useMemo(() => ({ state, isBooting, login, logout, refreshMe, routeByRole }), [state, isBooting]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);
