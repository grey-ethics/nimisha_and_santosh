/**
 * Top-level App
 * - Renders all routes
 * - Could host global toasts etc.
 */
import { AppRouter } from "./router";
import Toast from "./components/Toast";

export default function App() {
  return (
    <>
      <AppRouter />
      <Toast />
    </>
  );
}
