import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import { AuthProvider } from './contexts/AuthContext.jsx'
import { AIProvider } from './contexts/AIContext.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AuthProvider>
      <AIProvider>
        <App />
      </AIProvider>
    </AuthProvider>
  </React.StrictMode>
)
