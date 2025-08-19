/**
 * Defines all routes with role-specific layouts.
 * - After login, users are redirected based on role.
 * - Use <PrivateRoute> to protect segments.
 */
import { Routes, Route, Navigate } from "react-router-dom";
import Login from "../pages/Login";
import ChangePassword from "../pages/ChangePassword";
import NotFound from "../pages/NotFound";
import { PrivateRoute, RoleRoute } from "./guards";
import AdminLayout from "../layouts/AdminLayout";
import RegionalManagerLayout from "../layouts/RegionalManagerLayout";
import BranchManagerLayout from "../layouts/BranchManagerLayout";
import PatientLayout from "../layouts/PatientLayout";

// Admin pages
import Regions from "../pages/admin/Regions";
import Branches from "../pages/admin/Branches";
import RegionalManagers from "../pages/admin/RegionalManagers";
import Audit from "../pages/admin/Audit";

// RM pages
import RMBranchManagers from "../pages/rm/BranchManagers";
import RMPatients from "../pages/rm/Patients";

// BM pages
import BMPatients from "../pages/bm/Patients";

// Patient pages
import Profile from "../pages/patient/Profile";
import Shop from "../pages/patient/Shop";
import Orders from "../pages/patient/Orders";
import Education from "../pages/patient/Education";

export const AppRouter = () => {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<Login />} />
      <Route path="/change-password" element={<PrivateRoute><ChangePassword /></PrivateRoute>} />

      {/* Admin */}
      <Route element={<PrivateRoute/>}>
        <Route element={<RoleRoute allow={['ADMIN']} />}>
          <Route path="/admin" element={<AdminLayout />}>
            <Route index element={<Navigate to="regions" replace />} />
            <Route path="regions" element={<Regions />} />
            <Route path="branches" element={<Branches />} />
            <Route path="regional-managers" element={<RegionalManagers />} />
            <Route path="audit" element={<Audit />} />
          </Route>
        </Route>

        {/* Regional Manager */}
        <Route element={<RoleRoute allow={['REGIONAL_MANAGER']} />}>
          <Route path="/rm" element={<RegionalManagerLayout />}>
            <Route index element={<Navigate to="branch-managers" replace />} />
            <Route path="branch-managers" element={<RMBranchManagers />} />
            <Route path="patients" element={<RMPatients />} />
          </Route>
        </Route>

        {/* Branch Manager */}
        <Route element={<RoleRoute allow={['BRANCH_MANAGER']} />}>
          <Route path="/bm" element={<BranchManagerLayout />}>
            <Route index element={<Navigate to="patients" replace />} />
            <Route path="patients" element={<BMPatients />} />
          </Route>
        </Route>

        {/* Patient */}
        <Route element={<RoleRoute allow={['PATIENT']} />}>
          <Route path="/patient" element={<PatientLayout />}>
            <Route index element={<Navigate to="profile" replace />} />
            <Route path="profile" element={<Profile />} />
            <Route path="shop" element={<Shop />} />
            <Route path="orders" element={<Orders />} />
            <Route path="education" element={<Education />} />
          </Route>
        </Route>
      </Route>

      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};
