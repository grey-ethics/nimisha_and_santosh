/// <reference types="vitest" />
/**
 * Vite config
 * - React + TS
 * - Server proxy (optional) if you want to avoid CORS during dev.
 */
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: true,
    // Uncomment to proxy API in dev instead of setting CORS on backend:
    // proxy: { "/auth": "http://localhost:8000", "/admin": "http://localhost:8000", "/users": "http://localhost:8000", "/patients": "http://localhost:8000", "/audit": "http://localhost:8000", "/me": "http://localhost:8000", "/patient": "http://localhost:8000" }
  }
});
