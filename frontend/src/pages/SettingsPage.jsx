import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import NavBar from '../components/NavBar';
import api from '../api/client';
import { useAuth } from '../contexts/AuthContext';
import { useAI } from '../contexts/AIContext';
import { theme } from '../theme';

function Section({ title, children }) {
  return (
    <div style={{
      background: theme.colors.surface, borderRadius: theme.radius.lg,
      padding: '24px 28px', boxShadow: theme.shadow.sm,
      border: `1px solid ${theme.colors.border}`, marginBottom: 24,
    }}>
      <h2 style={{ margin: '0 0 20px', fontSize: 17, fontWeight: 600, color: theme.colors.text }}>{title}</h2>
      {children}
    </div>
  );
}

function Field({ label, children }) {
  return (
    <div style={{ marginBottom: 16 }}>
      <label style={{ display: 'block', marginBottom: 6, fontSize: 13, fontWeight: 500, color: theme.colors.textSecondary }}>
        {label}
      </label>
      {children}
    </div>
  );
}

const inputStyle = {
  width: '100%', padding: '10px 13px', fontSize: 14,
  border: `1px solid ${theme.colors.border}`, borderRadius: theme.radius.md,
  background: theme.colors.surface, color: theme.colors.text,
  fontFamily: theme.fonts.sans, boxSizing: 'border-box', outline: 'none',
};

export default function SettingsPage() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const { aiConfig, clearConfig } = useAI();

  // Profile
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [profileMsg, setProfileMsg] = useState(null);
  const [savingProfile, setSavingProfile] = useState(false);

  // Password
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordMsg, setPasswordMsg] = useState(null);
  const [savingPassword, setSavingPassword] = useState(false);

  // Danger zone
  const [resetConfirm, setResetConfirm] = useState('');
  const [resetting, setResetting] = useState(false);
  const [resetMsg, setResetMsg] = useState(null);

  useEffect(() => {
    api.get('/settings/profile').then(r => {
      setName(r.data.name || '');
      setEmail(r.data.email || '');
    }).catch(() => {});
  }, []);

  const saveProfile = async () => {
    setSavingProfile(true);
    setProfileMsg(null);
    try {
      await api.patch('/settings/profile', { name, email });
      setProfileMsg({ ok: true, text: 'Profile updated.' });
    } catch (e) {
      setProfileMsg({ ok: false, text: e.response?.data?.detail || 'Update failed.' });
    } finally {
      setSavingProfile(false);
    }
  };

  const savePassword = async () => {
    if (newPassword !== confirmPassword) {
      setPasswordMsg({ ok: false, text: 'New passwords do not match.' });
      return;
    }
    if (newPassword.length < 8) {
      setPasswordMsg({ ok: false, text: 'Password must be at least 8 characters.' });
      return;
    }
    setSavingPassword(true);
    setPasswordMsg(null);
    try {
      await api.post('/settings/change-password', { current_password: currentPassword, new_password: newPassword });
      setPasswordMsg({ ok: true, text: 'Password updated.' });
      setCurrentPassword(''); setNewPassword(''); setConfirmPassword('');
    } catch (e) {
      setPasswordMsg({ ok: false, text: e.response?.data?.detail || 'Password change failed.' });
    } finally {
      setSavingPassword(false);
    }
  };

  const resetProgress = async () => {
    if (resetConfirm !== 'RESET') return;
    setResetting(true);
    setResetMsg(null);
    try {
      await api.post('/settings/reset-progress');
      setResetMsg({ ok: true, text: 'Progress reset. You will be redirected to placement.' });
      setTimeout(() => navigate('/placement/intro'), 2000);
    } catch {
      setResetMsg({ ok: false, text: 'Reset failed.' });
    } finally {
      setResetting(false);
    }
  };

  const Msg = ({ msg }) => msg ? (
    <div style={{
      padding: '10px 14px', borderRadius: theme.radius.sm, marginTop: 12, fontSize: 13,
      background: msg.ok ? theme.colors.successLight : theme.colors.errorLight,
      color: msg.ok ? theme.colors.success : theme.colors.error,
      border: `1px solid ${msg.ok ? theme.colors.success : theme.colors.error}`,
    }}>
      {msg.text}
    </div>
  ) : null;

  const Btn = ({ onClick, disabled, danger, loading, children }) => (
    <button
      onClick={onClick}
      disabled={disabled || loading}
      style={{
        padding: '10px 22px',
        background: danger ? theme.colors.errorLight : theme.colors.primary,
        color: danger ? theme.colors.error : '#fff',
        border: danger ? `1px solid ${theme.colors.error}` : 'none',
        borderRadius: theme.radius.md, cursor: disabled || loading ? 'not-allowed' : 'pointer',
        fontSize: 14, fontWeight: 600, fontFamily: theme.fonts.sans,
        opacity: disabled || loading ? 0.6 : 1,
      }}
    >
      {loading ? 'Saving\u2026' : children}
    </button>
  );

  return (
    <>
      <NavBar />
      <div style={{ maxWidth: 600, margin: '0 auto', padding: '32px 24px', fontFamily: theme.fonts.sans }}>
        <h1 style={{ margin: '0 0 28px', fontSize: 26, fontWeight: 700, color: theme.colors.text }}>Settings</h1>

        {/* Profile */}
        <Section title="Profile">
          <Field label="Name">
            <input style={inputStyle} value={name} onChange={e => setName(e.target.value)} />
          </Field>
          <Field label="Email">
            <input style={inputStyle} type="email" value={email} onChange={e => setEmail(e.target.value)} />
          </Field>
          <Btn onClick={saveProfile} loading={savingProfile}>Save Profile</Btn>
          <Msg msg={profileMsg} />
        </Section>

        {/* Password */}
        <Section title="Change Password">
          <Field label="Current Password">
            <input style={inputStyle} type="password" value={currentPassword} onChange={e => setCurrentPassword(e.target.value)} />
          </Field>
          <Field label="New Password">
            <input style={inputStyle} type="password" value={newPassword} onChange={e => setNewPassword(e.target.value)} />
          </Field>
          <Field label="Confirm New Password">
            <input style={inputStyle} type="password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} />
          </Field>
          <Btn onClick={savePassword} loading={savingPassword} disabled={!currentPassword || !newPassword || !confirmPassword}>
            Update Password
          </Btn>
          <Msg msg={passwordMsg} />
        </Section>

        {/* AI Hints */}
        <Section title="AI Hints">
          {aiConfig ? (
            <div>
              <div style={{ padding: '12px 14px', background: theme.colors.successLight, borderRadius: theme.radius.md, marginBottom: 16, border: `1px solid ${theme.colors.success}`, fontSize: 13, color: theme.colors.success }}>
                ✓ AI hints enabled — {aiConfig.provider} ({aiConfig.model})
              </div>
              <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
                <Link
                  to="/ai-setup"
                  style={{
                    padding: '10px 20px', background: theme.colors.surfaceAlt,
                    border: `1px solid ${theme.colors.border}`, borderRadius: theme.radius.md,
                    cursor: 'pointer', fontSize: 14, fontFamily: theme.fonts.sans,
                    color: theme.colors.text, textDecoration: 'none', display: 'inline-block',
                  }}
                >
                  Change AI Settings
                </Link>
                <button
                  onClick={() => clearConfig()}
                  style={{
                    padding: '10px 20px', background: theme.colors.errorLight,
                    border: `1px solid ${theme.colors.error}`, borderRadius: theme.radius.md,
                    cursor: 'pointer', fontSize: 14, fontFamily: theme.fonts.sans, color: theme.colors.error,
                  }}
                >
                  Remove Key
                </button>
              </div>
            </div>
          ) : (
            <div>
              <p style={{ margin: '0 0 14px', fontSize: 14, color: theme.colors.textSecondary, lineHeight: 1.6 }}>
                Add an AI API key to get personalized hints when you're stuck. Your key is stored only in your browser — never sent to our servers.
              </p>
              <Link
                to="/ai-setup"
                style={{
                  display: 'inline-block', padding: '10px 22px',
                  background: theme.colors.primary, color: '#fff',
                  borderRadius: theme.radius.md, textDecoration: 'none',
                  fontSize: 14, fontWeight: 600, fontFamily: theme.fonts.sans,
                }}
              >
                Set Up AI Hints →
              </Link>
            </div>
          )}
        </Section>

        {/* Danger zone */}
        <Section title="Danger Zone">
          <p style={{ margin: '0 0 16px', fontSize: 14, color: theme.colors.textSecondary, lineHeight: 1.6 }}>
            Resetting your progress will delete all mastery data, practice sessions, review schedules, and placement results. This cannot be undone.
          </p>
          <Field label="Type RESET to confirm">
            <input
              style={{ ...inputStyle, borderColor: resetConfirm === 'RESET' ? theme.colors.error : theme.colors.border }}
              value={resetConfirm}
              onChange={e => setResetConfirm(e.target.value)}
              placeholder="RESET"
            />
          </Field>
          <Btn onClick={resetProgress} loading={resetting} disabled={resetConfirm !== 'RESET'} danger>
            Reset All Progress
          </Btn>
          <Msg msg={resetMsg} />
        </Section>
      </div>
    </>
  );
}
