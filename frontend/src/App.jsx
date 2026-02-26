import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './contexts/AuthContext.jsx'
import { theme } from './theme.js'
import LoginPage from './pages/LoginPage.jsx'
import RegisterPage from './pages/RegisterPage.jsx'
import Dashboard from './pages/Dashboard.jsx'
import PlacementIntro from './pages/PlacementIntro.jsx'
import PlacementQuestion from './pages/PlacementQuestion.jsx'
import PlacementResults from './pages/PlacementResults.jsx'
import LessonPage from './pages/LessonPage.jsx'
import WorkedExamplesPage from './pages/WorkedExamplesPage.jsx'
import PracticePage from './pages/PracticePage.jsx'
import ScoreReport from './pages/ScoreReport.jsx'
import AISetupPage from './pages/AISetupPage.jsx'
import ReviewQueue from './pages/ReviewQueue.jsx'

function ProtectedRoute({ children }) {
  const { user } = useAuth()
  return user ? children : <Navigate to="/login" replace />
}

function App() {
  return (
    <BrowserRouter>
      <div style={{ fontFamily: theme.fonts.sans, background: theme.colors.bg, minHeight: '100vh' }}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route
            path="/dashboard"
            element={<ProtectedRoute><Dashboard /></ProtectedRoute>}
          />
          <Route
            path="/placement/intro"
            element={<ProtectedRoute><PlacementIntro /></ProtectedRoute>}
          />
          <Route
            path="/placement/start"
            element={<ProtectedRoute><PlacementQuestion /></ProtectedRoute>}
          />
          <Route
            path="/placement/results"
            element={<ProtectedRoute><PlacementResults /></ProtectedRoute>}
          />
          <Route
            path="/lesson/:nodeId"
            element={<ProtectedRoute><LessonPage /></ProtectedRoute>}
          />
          <Route
            path="/lesson/:nodeId/examples"
            element={<ProtectedRoute><WorkedExamplesPage /></ProtectedRoute>}
          />
          <Route
            path="/practice/:nodeId"
            element={<ProtectedRoute><PracticePage /></ProtectedRoute>}
          />
          <Route
            path="/score/:nodeId"
            element={<ProtectedRoute><ScoreReport /></ProtectedRoute>}
          />
          <Route
            path="/ai-setup"
            element={<ProtectedRoute><AISetupPage /></ProtectedRoute>}
          />
          <Route
            path="/reviews"
            element={<ProtectedRoute><ReviewQueue /></ProtectedRoute>}
          />
          <Route path="/" element={<Navigate to="/login" replace />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
