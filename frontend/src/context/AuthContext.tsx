import { createContext, useContext, useState, useCallback, type ReactNode } from "react";
import { loginStudent, registerStudent } from "../api/client";

interface AuthContextType {
  studentId: string | null;
  needsPlacement: boolean;
  hasAiKey: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  logout: () => void;
  setNeedsPlacement: (value: boolean) => void;
  setHasAiKey: (value: boolean) => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [studentId, setStudentId] = useState<string | null>(
    () => localStorage.getItem("studentId")
  );
  const [needsPlacement, setNeedsPlacement] = useState<boolean>(
    () => localStorage.getItem("needsPlacement") === "true"
  );
  const [hasAiKey, setHasAiKey] = useState<boolean>(
    () => localStorage.getItem("hasAiKey") === "true"
  );

  const login = useCallback(async (email: string, password: string) => {
    const res = await loginStudent(email, password);
    localStorage.setItem("studentId", res.student_id);
    localStorage.setItem("needsPlacement", String(res.needs_placement));
    setStudentId(res.student_id);
    setNeedsPlacement(res.needs_placement);
  }, []);

  const register = useCallback(async (email: string, password: string, name: string) => {
    const res = await registerStudent(email, password, name);
    localStorage.setItem("studentId", res.student_id);
    localStorage.setItem("needsPlacement", "true");
    setStudentId(res.student_id);
    setNeedsPlacement(true);
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem("studentId");
    localStorage.removeItem("needsPlacement");
    localStorage.removeItem("hasAiKey");
    setStudentId(null);
    setNeedsPlacement(false);
    setHasAiKey(false);
  }, []);

  const updateNeedsPlacement = useCallback((value: boolean) => {
    localStorage.setItem("needsPlacement", String(value));
    setNeedsPlacement(value);
  }, []);

  const updateHasAiKey = useCallback((value: boolean) => {
    localStorage.setItem("hasAiKey", String(value));
    setHasAiKey(value);
  }, []);

  return (
    <AuthContext.Provider value={{
      studentId, needsPlacement, hasAiKey, login, register, logout,
      setNeedsPlacement: updateNeedsPlacement,
      setHasAiKey: updateHasAiKey
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
