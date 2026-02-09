import { createContext, useContext, useState, useCallback, type ReactNode } from "react";
import { loginStudent, registerStudent } from "../api/client";

interface AuthContextType {
  studentId: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [studentId, setStudentId] = useState<string | null>(
    () => localStorage.getItem("studentId")
  );

  const login = useCallback(async (email: string, password: string) => {
    const res = await loginStudent(email, password);
    localStorage.setItem("studentId", res.student_id);
    setStudentId(res.student_id);
  }, []);

  const register = useCallback(async (email: string, password: string, name: string) => {
    const res = await registerStudent(email, password, name);
    localStorage.setItem("studentId", res.student_id);
    setStudentId(res.student_id);
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem("studentId");
    setStudentId(null);
  }, []);

  return (
    <AuthContext.Provider value={{ studentId, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
