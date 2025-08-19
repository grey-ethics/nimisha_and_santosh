/**
 * Manually mirrored types from OpenAPI for convenience in the UI.
 * (The generator emits fetchers; we keep small TS types here.)
 * Source: OpenAPI 3.1 (see citation in answer).
 */
export type Role = "ADMIN" | "REGIONAL_MANAGER" | "BRANCH_MANAGER" | "PATIENT";

export type UserOut = {
  id: string;
  role: Role;
  phone: string;
  full_name: string | null;
  email: string | null;
  is_active: boolean;
  must_change_password: boolean;
};

export type RegionOut = { id: string; name: string; is_active: boolean };
export type RegionCreate = { name: string };

export type BranchOut = { id: string; region_id: string; name: string; address: string | null; is_active: boolean };
export type BranchCreate = { region_id: string; name: string; address?: string | null };

export type PatientStatus = "ACTIVE" | "INACTIVE";
export type Gender = "MALE" | "FEMALE" | "OTHER" | "UNKNOWN";
export type DonorType = "LIVING" | "DECEASED" | "UNKNOWN";

export type PatientOut = {
  user_id: string;
  branch_id: string;
  assigned_bm_user_id: string;
  rm_approval: boolean;
  enrollment_date: string | null;
  transplant_date: string | null;
  notes: string | null;
  mrn: string | null;
  blood_group: string | null;
  donor_type: DonorType | null;
  primary_center: string | null;
  treating_physician: string | null;
  date_of_birth: string | null;
  gender: Gender | null;
  emergency_contact_name: string | null;
  emergency_contact_phone: string | null;
  status: PatientStatus;
  is_active: boolean;
};
