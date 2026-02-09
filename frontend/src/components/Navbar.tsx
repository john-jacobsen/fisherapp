import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { studentId, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  if (!studentId) return null;

  return (
    <nav className="bg-white border-b border-slate-200 px-4 py-3">
      <div className="max-w-5xl mx-auto flex items-center justify-between">
        <Link to="/dashboard" className="text-lg font-bold text-slate-900 hover:text-blue-600 transition-colors">
          BerkeleyStats Tutor
        </Link>

        <div className="flex items-center gap-4">
          <Link
            to="/dashboard"
            className="text-sm text-slate-600 hover:text-blue-600 transition-colors"
          >
            Dashboard
          </Link>
          <Link
            to="/practice"
            className="text-sm text-slate-600 hover:text-blue-600 transition-colors"
          >
            Practice
          </Link>
          <button
            onClick={handleLogout}
            className="text-sm text-slate-500 hover:text-red-600 transition-colors"
          >
            Sign Out
          </button>
        </div>
      </div>
    </nav>
  );
}
