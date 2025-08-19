/**
 * Route guards:
 * - <PrivateRoute>: requires auth (valid access token).
 * - <RoleRoute>: requires user role in allowed set.
 *
 * Future: add permission-level checks if backend exposes scopes.
 */
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../store/authStore";
import Loading from "../components/Loading";

export const PrivateRoute = ({ children }: { children?: JSX.Element }) => {
  const { state, isBooting } = useAuth();
  const loc = useLocation();

  if (isBooting) return <Loading label="Booting..." />;

  if (!state.tokens?.accessToken) {
    return <Navigate to="/login" replace state={{ from: loc }} />;
  }
  return children ?? <Outlet />;
};

export const RoleRoute = ({ allow }: { allow: Array<'ADMIN'|'REGIONAL_MANAGER'|'BRANCH_MANAGER'|'PATIENT'> }) => {
  const { state } = useAuth();
  const role = state.me?.role as any;
  if (!role) return <Navigate to="/login" replace />;
  if (!allow.includes(role)) return <Navigate to="/login" replace />;
  return <Outlet />;
};
