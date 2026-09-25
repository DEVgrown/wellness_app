import { reactive, computed } from 'vue';

const TOKEN_KEY = 'karina_auth_token';
const USER_KEY = 'karina_auth_user';

const state = reactive({
  token: localStorage.getItem(TOKEN_KEY) || null,
  user: JSON.parse(localStorage.getItem(USER_KEY) || 'null'),
  loading: false,
  error: null
});

export const useAuthStore = () => {
  const token = computed(() => state.token);
  const user = computed(() => state.user || {
    name: 'Sarah',
    email: 'sarah@example.com',
    phone: '+254 712 345 678',
    avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=200&q=80'
  });
  const isAuthenticated = computed(() => !!state.token);
  const isAdmin = computed(() => {
    if (!state.user) return false;
    return !!(state.user.is_staff || state.user.is_superuser || state.user.role === 'admin' || state.user.username === 'admin' || (state.user.email && state.user.email.includes('admin')));
  });
  const loading = computed(() => state.loading);
  const error = computed(() => state.error);

  async function login(username, password) {
    state.loading = true;
    state.error = null;
    try {
      const res = await fetch('/api/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.non_field_errors?.[0] || data.detail || 'Login failed. Please check your credentials.');
      }
      state.token = data.token;
      state.user = data.user;
      localStorage.setItem(TOKEN_KEY, data.token);
      localStorage.setItem(USER_KEY, JSON.stringify(data.user));
      return data;
    } catch (err) {
      state.error = err.message;
      throw err;
    } finally {
      state.loading = false;
    }
  }

  async function signup(userData) {
    state.loading = true;
    state.error = null;
    try {
      const res = await fetch('/api/auth/signup/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      });
      const data = await res.json();
      if (!res.ok) {
        const errorMsg = data.username?.[0] || data.email?.[0] || data.password?.[0] || data.detail || 'Signup failed.';
        throw new Error(errorMsg);
      }
      state.token = data.token;
      state.user = data.user;
      localStorage.setItem(TOKEN_KEY, data.token);
      localStorage.setItem(USER_KEY, JSON.stringify(data.user));
      return data;
    } catch (err) {
      state.error = err.message;
      throw err;
    } finally {
      state.loading = false;
    }
  }

  async function logout() {
    if (state.token) {
      try {
        await fetch('/api/auth/logout/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${state.token}`
          }
        });
      } catch (e) {
        console.warn('Logout request error:', e);
      }
    }
    state.token = null;
    state.user = null;
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  }

  async function checkAuth() {
    if (!state.token) return null;
    try {
      const res = await fetch('/api/auth/me/', {
        headers: {
          'Authorization': `Token ${state.token}`
        }
      });
      if (res.ok) {
        const data = await res.json();
        state.user = data.user;
        localStorage.setItem(USER_KEY, JSON.stringify(data.user));
        return data.user;
      } else {
        // Token expired or invalid
        logout();
      }
    } catch (e) {
      console.warn('Failed to verify token:', e);
    }
    return null;
  }

  return {
    token,
    user,
    isAuthenticated,
    isAdmin,
    loading,
    error,
    login,
    signup,
    logout,
    checkAuth
  };
};
