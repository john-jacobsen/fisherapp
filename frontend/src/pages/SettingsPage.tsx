import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { resetPlacement, getAiConfig, saveAiConfig, deleteAiConfig, testAiConnection } from "../api/client";

type AiProvider = "anthropic" | "openai" | "gemini" | "deepseek";

export default function SettingsPage() {
  const { studentId, setNeedsPlacement, setHasAiKey } = useAuth();
  const navigate = useNavigate();

  // Placement state
  const [resetting, setResetting] = useState(false);
  const [placementError, setPlacementError] = useState("");
  const [showConfirm, setShowConfirm] = useState(false);

  // AI config state
  const [aiProvider, setAiProvider] = useState<AiProvider>("anthropic");
  const [aiApiKey, setAiApiKey] = useState("");
  const [aiConfigured, setAiConfigured] = useState(false);
  const [aiCurrentProvider, setAiCurrentProvider] = useState<string | null>(null);
  const [aiKeyHint, setAiKeyHint] = useState("");
  const [aiSaving, setAiSaving] = useState(false);
  const [aiTesting, setAiTesting] = useState(false);
  const [aiDeleting, setAiDeleting] = useState(false);
  const [aiError, setAiError] = useState("");
  const [aiSuccess, setAiSuccess] = useState("");
  const [aiLoading, setAiLoading] = useState(true);

  if (!studentId) {
    navigate("/login");
    return null;
  }

  // Load AI config on mount
  useEffect(() => {
    let mounted = true;
    getAiConfig(studentId)
      .then((config) => {
        if (!mounted) return;
        setAiConfigured(config.configured);
        setAiCurrentProvider(config.provider);
        setAiKeyHint(config.key_hint || "");
        if (config.provider) {
          setAiProvider(config.provider as AiProvider);
        }
        setHasAiKey(config.configured);
      })
      .catch(() => {})
      .finally(() => { if (mounted) setAiLoading(false); });
    return () => { mounted = false; };
  }, [studentId, setHasAiKey]);

  const handleRetakePlacement = async () => {
    setResetting(true);
    setPlacementError("");
    try {
      await resetPlacement(studentId);
      setNeedsPlacement(true);
      navigate("/placement");
    } catch (err) {
      setPlacementError(err instanceof Error ? err.message : "Failed to reset placement");
    } finally {
      setResetting(false);
      setShowConfirm(false);
    }
  };

  const handleSaveAiConfig = async () => {
    if (!aiApiKey.trim()) {
      setAiError("Please enter an API key");
      return;
    }
    setAiSaving(true);
    setAiError("");
    setAiSuccess("");
    try {
      await saveAiConfig(studentId, aiProvider, aiApiKey.trim());
      setAiConfigured(true);
      setAiCurrentProvider(aiProvider);
      setAiKeyHint("****" + aiApiKey.trim().slice(-4));
      setAiApiKey("");
      setAiSuccess("API key saved successfully");
      setHasAiKey(true);
    } catch (err) {
      setAiError(err instanceof Error ? err.message : "Failed to save AI config");
    } finally {
      setAiSaving(false);
    }
  };

  const handleTestConnection = async () => {
    setAiTesting(true);
    setAiError("");
    setAiSuccess("");
    try {
      await testAiConnection(studentId);
      setAiSuccess("Connection successful!");
    } catch (err) {
      setAiError(err instanceof Error ? err.message : "Connection test failed");
    } finally {
      setAiTesting(false);
    }
  };

  const handleDeleteAiConfig = async () => {
    setAiDeleting(true);
    setAiError("");
    setAiSuccess("");
    try {
      await deleteAiConfig(studentId);
      setAiConfigured(false);
      setAiCurrentProvider(null);
      setAiKeyHint("");
      setAiSuccess("AI configuration removed");
      setHasAiKey(false);
    } catch (err) {
      setAiError(err instanceof Error ? err.message : "Failed to remove AI config");
    } finally {
      setAiDeleting(false);
    }
  };

  const providerLabel = (p: string | null) => {
    if (p === "anthropic") return "Anthropic Claude";
    if (p === "openai") return "OpenAI";
    if (p === "gemini") return "Google Gemini";
    if (p === "deepseek") return "DeepSeek";
    return "None";
  };

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-slate-900 mb-8">Settings</h1>

      {/* AI Configuration */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 mb-6">
        <h2 className="text-lg font-semibold text-slate-900 mb-2">AI-Powered Solutions</h2>
        <p className="text-sm text-slate-500 mb-4">
          Connect your own AI API key to get AI-powered step-by-step explanations when you answer incorrectly.
        </p>

        {aiLoading ? (
          <p className="text-sm text-slate-400">Loading...</p>
        ) : (
          <>
            {aiConfigured && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
                <p className="text-sm text-blue-800">
                  Connected: <span className="font-medium">{providerLabel(aiCurrentProvider)}</span>
                  {aiKeyHint && <span className="text-blue-600 ml-2">({aiKeyHint})</span>}
                </p>
              </div>
            )}

            <div className="space-y-3 mb-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Provider</label>
                <select
                  value={aiProvider}
                  onChange={(e) => setAiProvider(e.target.value as AiProvider)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="anthropic">Anthropic Claude</option>
                  <option value="openai">OpenAI</option>
                  <option value="gemini">Google Gemini</option>
                  <option value="deepseek">DeepSeek</option>
                </select>
                <p className="mt-1 text-xs text-slate-400">
                  {aiProvider === "anthropic" && "Get your API key at console.anthropic.com under API Keys."}
                  {aiProvider === "openai" && "Get your API key at platform.openai.com under API Keys."}
                  {aiProvider === "gemini" && "Get your API key at aistudio.google.com under API Keys."}
                  {aiProvider === "deepseek" && "Get your API key at platform.deepseek.com under API Keys."}
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  API Key {aiConfigured && "(enter new key to update)"}
                </label>
                <input
                  type="password"
                  value={aiApiKey}
                  onChange={(e) => setAiApiKey(e.target.value)}
                  placeholder={aiConfigured ? "Enter new key to update" : "Paste your API key"}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            {aiError && (
              <div className="text-red-600 text-sm bg-red-50 p-3 rounded-lg mb-3">{aiError}</div>
            )}
            {aiSuccess && (
              <div className="text-green-600 text-sm bg-green-50 p-3 rounded-lg mb-3">{aiSuccess}</div>
            )}

            <div className="flex flex-wrap items-center gap-3">
              <button
                onClick={handleSaveAiConfig}
                disabled={aiSaving || !aiApiKey.trim()}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                {aiSaving ? "Saving..." : "Save Key"}
              </button>

              {aiConfigured && (
                <>
                  <button
                    onClick={handleTestConnection}
                    disabled={aiTesting}
                    className="px-4 py-2 bg-slate-100 text-slate-700 rounded-lg text-sm font-medium hover:bg-slate-200 disabled:opacity-50 transition-colors"
                  >
                    {aiTesting ? "Testing..." : "Test Connection"}
                  </button>
                  <button
                    onClick={handleDeleteAiConfig}
                    disabled={aiDeleting}
                    className="px-4 py-2 text-red-600 text-sm hover:text-red-800 disabled:opacity-50 transition-colors"
                  >
                    {aiDeleting ? "Removing..." : "Remove Key"}
                  </button>
                </>
              )}
            </div>
          </>
        )}
      </div>

      {/* Placement Test */}
      <div className="bg-white rounded-xl border border-slate-200 p-6">
        <h2 className="text-lg font-semibold text-slate-900 mb-2">Placement Test</h2>
        <p className="text-sm text-slate-500 mb-4">
          Retake the placement test to reassess your starting level across all topics.
          This will reset your topic progress and difficulty levels.
        </p>

        {placementError && (
          <div className="text-red-600 text-sm bg-red-50 p-3 rounded-lg mb-4">
            {placementError}
          </div>
        )}

        {!showConfirm ? (
          <button
            onClick={() => setShowConfirm(true)}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
          >
            Retake Placement Test
          </button>
        ) : (
          <div className="flex items-center gap-3">
            <span className="text-sm text-slate-600">
              This will reset all topic progress. Are you sure?
            </span>
            <button
              onClick={handleRetakePlacement}
              disabled={resetting}
              className="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 disabled:opacity-50 transition-colors"
            >
              {resetting ? "Resetting..." : "Yes, Reset"}
            </button>
            <button
              onClick={() => setShowConfirm(false)}
              className="px-4 py-2 text-slate-600 text-sm hover:text-slate-800 transition-colors"
            >
              Cancel
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
