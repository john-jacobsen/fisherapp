import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { saveAiConfig } from "../api/client";

type AiProvider = "anthropic" | "openai";

export default function LoginPage() {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login, register, setHasAiKey } = useAuth();

  // AI config during registration
  const [showAiSection, setShowAiSection] = useState(false);
  const [aiProvider, setAiProvider] = useState<AiProvider>("anthropic");
  const [aiApiKey, setAiApiKey] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      if (isRegister) {
        const result = await register(email, password, name);
        // If user provided an AI key during registration, save it
        if (aiApiKey.trim()) {
          try {
            // Get the student_id from localStorage (set by register)
            const studentId = localStorage.getItem("studentId");
            if (studentId) {
              await saveAiConfig(studentId, aiProvider, aiApiKey.trim());
              setHasAiKey(true);
            }
          } catch {
            // Don't block registration if AI config fails
          }
        }
        return result;
      } else {
        await login(email, password);
      }
      // Redirect is handled by App.tsx route (Navigate based on auth state)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-slate-900">BerkeleyStats Tutor</h1>
          <p className="text-slate-500 mt-2">
            Adaptive algebra practice for statistics students
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <div className="flex mb-6 border-b border-slate-200">
            <button
              className={`flex-1 pb-3 text-sm font-medium ${
                !isRegister
                  ? "text-blue-600 border-b-2 border-blue-600"
                  : "text-slate-500"
              }`}
              onClick={() => setIsRegister(false)}
            >
              Sign In
            </button>
            <button
              className={`flex-1 pb-3 text-sm font-medium ${
                isRegister
                  ? "text-blue-600 border-b-2 border-blue-600"
                  : "text-slate-500"
              }`}
              onClick={() => setIsRegister(true)}
            >
              Register
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {isRegister && (
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Name
                </label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Your name"
                  required
                />
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="you@berkeley.edu"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Password"
                required
              />
            </div>

            {/* AI-Powered Solutions — only on registration */}
            {isRegister && (
              <div className="border border-slate-200 rounded-lg">
                <button
                  type="button"
                  onClick={() => setShowAiSection(!showAiSection)}
                  className="w-full flex items-center justify-between px-3 py-2.5 text-sm text-slate-600 hover:text-slate-800"
                >
                  <span>AI-Powered Solutions (optional)</span>
                  <span className="text-slate-400">{showAiSection ? "−" : "+"}</span>
                </button>
                {showAiSection && (
                  <div className="px-3 pb-3 space-y-3 border-t border-slate-100 pt-3">
                    <p className="text-xs text-slate-400">
                      Add your own AI API key for AI-powered explanations. You can also do this later in Settings.
                    </p>
                    <div>
                      <label className="block text-xs font-medium text-slate-600 mb-1">Provider</label>
                      <select
                        value={aiProvider}
                        onChange={(e) => setAiProvider(e.target.value as AiProvider)}
                        className="w-full px-2 py-1.5 border border-slate-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="anthropic">Anthropic Claude</option>
                        <option value="openai">OpenAI</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-xs font-medium text-slate-600 mb-1">API Key</label>
                      <input
                        type="password"
                        value={aiApiKey}
                        onChange={(e) => setAiApiKey(e.target.value)}
                        placeholder="Paste your API key"
                        className="w-full px-2 py-1.5 border border-slate-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                  </div>
                )}
              </div>
            )}

            {error && (
              <div className="text-red-600 text-sm bg-red-50 p-3 rounded-lg">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-2.5 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? "Please wait..." : isRegister ? "Create Account" : "Sign In"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
