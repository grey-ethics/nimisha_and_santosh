import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import { AuthProvider } from "./store/authStore";   // ✅ add this
import "./index.css";                               // ✅ optional: actually load Tailwind/CSS

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>                                {/* ✅ wrap your app */}
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
