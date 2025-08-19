import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";  // ✅ import router
import App from "./App";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>   {/* ✅ Wrap App inside BrowserRouter */}
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
