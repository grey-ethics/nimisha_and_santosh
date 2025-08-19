/**
 * Patient placeholders:
 * - /patient/education
 * - /patient/shop
 * - /patient/orders
 */
import type { AxiosInstance } from "axios";

export async function education(api: AxiosInstance) { return api.get("/patient/education"); }
export async function shop(api: AxiosInstance) { return api.get("/patient/shop"); }
export async function orders(api: AxiosInstance) { return api.get("/patient/orders"); }
