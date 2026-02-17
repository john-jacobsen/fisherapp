import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import Navbar from "./components/Navbar";
import LoginPage from "./pages/LoginPage";
import PlacementPage from "./pages/PlacementPage";
import PracticePage from "./pages/PracticePage";
import DashboardPage from "./pages/DashboardPage";
import SettingsPage from "./pages/SettingsPage";

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { studentId } = useAuth();
  if (!studentId) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

function AppRoutes() {
  const { studentId, needsPlacement } = useAuth();

  const loggedInRedirect = needsPlacement ? "/placement" : "/dashboard";

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      <Routes>
        <Route
          path="/login"
          element={studentId ? <Navigate to={loggedInRedirect} replace /> : <LoginPage />}
        />
        <Route
          path="/placement"
          element={
            <ProtectedRoute>
              <PlacementPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/practice"
          element={
            <ProtectedRoute>
              <PracticePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/settings"
          element={
            <ProtectedRoute>
              <SettingsPage />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to={studentId ? loggedInRedirect : "/login"} replace />} />
      </Routes>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}
