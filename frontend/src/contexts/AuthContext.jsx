import { createContext, useContext, useState } from 'react'
import api from '../api/client.js'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem('fisher_user')
    return stored ? JSON.parse(stored) : null
  })

  const login = async (email, password) => {
    const res = await api.post('/auth/login', { email, password })
    localStorage.setItem('fisher_token', res.data.token)
    localStorage.setItem('fisher_user', JSON.stringify(res.data.user))
    setUser(res.data.user)
    return res.data.user
  }

  const register = async (email, name, password, courseCode) => {
    const res = await api.post('/auth/register', { email, name, password, course_code: courseCode })
    localStorage.setItem('fisher_token', res.data.token)
    localStorage.setItem('fisher_user', JSON.stringify(res.data.user))
    setUser(res.data.user)
    return res.data.user
  }

  const logout = () => {
    localStorage.removeItem('fisher_token')
    localStorage.removeItem('fisher_user')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider')
  return ctx
}
