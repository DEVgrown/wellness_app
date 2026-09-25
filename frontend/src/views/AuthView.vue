<template>
  <div class="min-h-screen bg-surface dark:bg-slate-950 text-on-surface dark:text-slate-100 flex flex-col justify-between py-12 px-4 sm:px-6 lg:px-8 transition-colors duration-200">
    <!-- Header / Brand Link -->
    <div class="max-w-md w-full mx-auto flex items-center justify-between mb-8">
      <router-link to="/home" class="flex items-center gap-3 group">
        <div class="w-10 h-10 rounded-full bg-secondary-fixed flex items-center justify-center text-primary shadow-sm shrink-0 group-hover:scale-105 transition-transform">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-linecap="round" stroke-width="6" viewBox="0 0 100 100">
            <circle cx="42" cy="24" r="10"></circle>
            <path d="M26 34 C44 33, 52 42, 40 55 C34 62, 35 74, 46 80"></path>
            <circle cx="62" cy="24" r="10" stroke="#7DA2D0"></circle>
            <path d="M46 34 C64 33, 72 42, 60 55 C54 62, 55 74, 66 80" stroke="#7DA2D0"></path>
          </svg>
        </div>
        <div class="flex flex-col">
          <span class="font-eyebrow text-eyebrow text-secondary uppercase tracking-widest leading-none">YOUR TRAINER</span>
          <span class="font-headline-sm text-headline-sm text-primary-container dark:text-white font-bold leading-tight">by Karina</span>
        </div>
      </router-link>

      <!-- Theme Switcher -->
      <button 
        @click="themeStore.toggleTheme()" 
        class="w-10 h-10 rounded-full bg-surface-container-low dark:bg-slate-800 text-on-surface-variant dark:text-slate-300 hover:text-primary dark:hover:text-white flex items-center justify-center transition-colors shadow-sm"
        :title="themeStore.isDark.value ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
        type="button"
      >
        <span class="material-symbols-outlined text-xl">
          {{ themeStore.isDark.value ? 'light_mode' : 'dark_mode' }}
        </span>
      </button>
    </div>

    <!-- Auth Card -->
    <div class="max-w-md w-full mx-auto bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 sm:p-8 shadow-xl border border-outline-variant/30 dark:border-slate-800">
      <!-- Title & Subtitle -->
      <div class="text-center mb-6">
        <h2 class="font-headline-lg text-headline-lg font-bold text-primary-container dark:text-white tracking-tight">
          {{ isSignUp ? 'Begin Your Journey' : 'Welcome Back' }}
        </h2>
        <p class="font-body-sm text-body-sm text-on-surface-variant dark:text-slate-400 mt-1">
          {{ isSignUp ? 'Create an account to book and manage your private movement sessions' : 'Sign in to access your upcoming sessions, notes, and passes' }}
        </p>
      </div>

      <!-- Mode Tabs -->
      <div class="flex p-1 bg-surface-container-low dark:bg-slate-800/80 rounded-full mb-6">
        <button 
          @click="setTab(false)" 
          type="button"
          class="flex-1 py-2 text-center font-label-md text-label-md rounded-full transition-all"
          :class="!isSignUp ? 'bg-surface-container-lowest dark:bg-slate-700 text-primary-container dark:text-white font-semibold shadow-sm' : 'text-on-surface-variant dark:text-slate-400 hover:text-on-surface'"
        >
          Sign In
        </button>
        <button 
          @click="setTab(true)" 
          type="button"
          class="flex-1 py-2 text-center font-label-md text-label-md rounded-full transition-all"
          :class="isSignUp ? 'bg-surface-container-lowest dark:bg-slate-700 text-primary-container dark:text-white font-semibold shadow-sm' : 'text-on-surface-variant dark:text-slate-400 hover:text-on-surface'"
        >
          Create Account
        </button>
      </div>

      <!-- Error Alert -->
      <div v-if="errorMessage" class="mb-5 p-3.5 rounded-xl bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-800/50 flex items-start gap-2.5 text-red-700 dark:text-red-300">
        <span class="material-symbols-outlined text-lg shrink-0 mt-0.5">error</span>
        <span class="font-body-sm text-body-sm flex-1">{{ errorMessage }}</span>
      </div>

      <!-- Success Alert -->
      <div v-if="successMessage" class="mb-5 p-3.5 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/50 flex items-start gap-2.5 text-emerald-700 dark:text-emerald-300">
        <span class="material-symbols-outlined text-lg shrink-0 mt-0.5">check_circle</span>
        <span class="font-body-sm text-body-sm flex-1">{{ successMessage }}</span>
      </div>

      <!-- Sign In Form -->
      <form v-if="!isSignUp" @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block font-label-sm text-label-sm text-on-surface-variant dark:text-slate-300 mb-1.5">
            Email or Username
          </label>
          <div class="relative">
            <input 
              v-model="loginForm.username" 
              type="text" 
              required
              placeholder="e.g. elena@example.com"
              class="w-full px-4 py-3 rounded-xl bg-surface-container-low dark:bg-slate-800/60 border border-outline-variant/40 dark:border-slate-700 text-on-surface dark:text-white focus:outline-none focus:border-secondary transition-colors"
            />
            <span class="material-symbols-outlined absolute right-3.5 top-3.5 text-on-surface-variant text-lg">person</span>
          </div>
        </div>

        <div>
          <div class="flex items-center justify-between mb-1.5">
            <label class="font-label-sm text-label-sm text-on-surface-variant dark:text-slate-300">
              Password
            </label>
            <a href="#" @click.prevent="showToast('Password reset link will be sent to your email.')" class="font-label-sm text-label-sm text-secondary hover:underline">
              Forgot?
            </a>
          </div>
          <div class="relative">
            <input 
              v-model="loginForm.password" 
              :type="showPassword ? 'text' : 'password'" 
              required
              placeholder="Enter your password"
              class="w-full px-4 py-3 rounded-xl bg-surface-container-low dark:bg-slate-800/60 border border-outline-variant/40 dark:border-slate-700 text-on-surface dark:text-white focus:outline-none focus:border-secondary transition-colors pr-10"
            />
            <button 
              type="button" 
              @click="showPassword = !showPassword"
              class="absolute right-3.5 top-3 text-on-surface-variant hover:text-on-surface focus:outline-none"
            >
              <span class="material-symbols-outlined text-lg">{{ showPassword ? 'visibility_off' : 'visibility' }}</span>
            </button>
          </div>
        </div>

        <button 
          type="submit" 
          :disabled="loading"
          class="w-full py-3.5 rounded-full bg-primary-container hover:bg-primary text-on-primary font-label-md text-label-md font-semibold shadow-md active:scale-[0.99] transition-all flex items-center justify-center gap-2 mt-2 disabled:opacity-50"
        >
          <span v-if="loading" class="material-symbols-outlined animate-spin text-lg">progress_activity</span>
          <span>{{ loading ? 'Signing In...' : 'Sign In' }}</span>
        </button>
      </form>

      <!-- Sign Up Form -->
      <form v-else @submit.prevent="handleSignUp" class="space-y-3.5">
        <div>
          <label class="block font-label-sm text-label-sm text-on-surface-variant dark:text-slate-300 mb-1">
            Full Name
          </label>
          <input 
            v-model="signUpForm.name" 
            type="text" 
            required
            placeholder="e.g. Elena Rostova"
            class="w-full px-4 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800/60 border border-outline-variant/40 dark:border-slate-700 text-on-surface dark:text-white focus:outline-none focus:border-secondary transition-colors"
          />
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="block font-label-sm text-label-sm text-on-surface-variant dark:text-slate-300 mb-1">
              Username
            </label>
            <input 
              v-model="signUpForm.username" 
              type="text" 
              required
              placeholder="e.g. elena_r"
              class="w-full px-4 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800/60 border border-outline-variant/40 dark:border-slate-700 text-on-surface dark:text-white focus:outline-none focus:border-secondary transition-colors"
            />
          </div>
          <div>
            <label class="block font-label-sm text-label-sm text-on-surface-variant dark:text-slate-300 mb-1">
              Phone (M-Pesa)
            </label>
            <input 
              v-model="signUpForm.phone" 
              type="tel" 
              placeholder="+254 700 000 000"
              class="w-full px-4 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800/60 border border-outline-variant/40 dark:border-slate-700 text-on-surface dark:text-white focus:outline-none focus:border-secondary transition-colors"
            />
          </div>
        </div>

        <div>
          <label class="block font-label-sm text-label-sm text-on-surface-variant dark:text-slate-300 mb-1">
            Email Address
          </label>
          <input 
            v-model="signUpForm.email" 
            type="email" 
            required
            placeholder="e.g. elena@example.com"
            class="w-full px-4 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800/60 border border-outline-variant/40 dark:border-slate-700 text-on-surface dark:text-white focus:outline-none focus:border-secondary transition-colors"
          />
        </div>

        <div>
          <label class="block font-label-sm text-label-sm text-on-surface-variant dark:text-slate-300 mb-1">
            Password (min 6 characters)
          </label>
          <div class="relative">
            <input 
              v-model="signUpForm.password" 
              :type="showPassword ? 'text' : 'password'" 
              required
              minlength="6"
              placeholder="Create a secure password"
              class="w-full px-4 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800/60 border border-outline-variant/40 dark:border-slate-700 text-on-surface dark:text-white focus:outline-none focus:border-secondary transition-colors pr-10"
            />
            <button 
              type="button" 
              @click="showPassword = !showPassword"
              class="absolute right-3.5 top-2.5 text-on-surface-variant hover:text-on-surface focus:outline-none"
            >
              <span class="material-symbols-outlined text-lg">{{ showPassword ? 'visibility_off' : 'visibility' }}</span>
            </button>
          </div>
        </div>

        <button 
          type="submit" 
          :disabled="loading"
          class="w-full py-3.5 rounded-full bg-primary-container hover:bg-primary text-on-primary font-label-md text-label-md font-semibold shadow-md active:scale-[0.99] transition-all flex items-center justify-center gap-2 mt-4 disabled:opacity-50"
        >
          <span v-if="loading" class="material-symbols-outlined animate-spin text-lg">progress_activity</span>
          <span>{{ loading ? 'Creating Account...' : 'Create Account & Claim Pass' }}</span>
        </button>
      </form>

      <!-- Quick Demo Account helper -->
      <!-- Quick Demo Account Fillers -->
      <div class="mt-6 pt-5 border-t border-outline-variant/30 dark:border-slate-800 text-center">
        <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400 mb-2">
          Test Quick Sign In:
        </p>
        <div class="flex items-center justify-center gap-2 flex-wrap">
          <button 
            @click="fillClientAccount" 
            type="button"
            class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-surface-container-low dark:bg-slate-800 text-secondary hover:text-primary-container dark:hover:text-white font-label-sm text-xs transition-all hover:bg-surface-container"
          >
            <span class="material-symbols-outlined text-xs text-emerald-600">person</span>
            <span>Client (Sarah)</span>
          </button>

          <button 
            @click="fillAdminAccount" 
            type="button"
            class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-primary-container/10 dark:bg-sky-950/60 text-primary-container dark:text-sky-300 font-label-sm text-xs font-semibold hover:bg-primary-container/20 transition-all border border-primary-container/20 dark:border-sky-800"
          >
            <span class="material-symbols-outlined text-xs text-amber-500">admin_panel_settings</span>
            <span>Studio Admin</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Simple Footer -->
    <div class="max-w-md w-full mx-auto text-center mt-8">
      <p class="font-body-sm text-body-sm text-on-surface-variant dark:text-slate-500">
        By continuing, you agree to our 
        <a href="#" class="underline hover:text-primary-container dark:hover:text-slate-300">Studio Terms</a> and 
        <a href="#" class="underline hover:text-primary-container dark:hover:text-slate-300">Privacy Policy</a>.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import { useThemeStore } from '@/stores/themeStore';
import { useBookingStore } from '@/stores/bookingStore';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const themeStore = useThemeStore();
const bookingStore = useBookingStore();

const isSignUp = ref(false);
const showPassword = ref(false);
const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const loginForm = reactive({
  username: '',
  password: ''
});

const signUpForm = reactive({
  name: '',
  username: '',
  email: '',
  phone: '+254 ',
  password: ''
});

onMounted(() => {
  if (route.name === 'signup' || route.query.mode === 'signup') {
    isSignUp.value = true;
  }
});

function setTab(signup) {
  isSignUp.value = signup;
  errorMessage.value = '';
  successMessage.value = '';
}

function showToast(msg) {
  bookingStore.showToast(msg, 'info');
}

function fillClientAccount() {
  isSignUp.value = false;
  loginForm.username = 'sarah';
  loginForm.password = 'SecretPassword123!';
  errorMessage.value = '';
}

function fillAdminAccount() {
  isSignUp.value = false;
  loginForm.username = 'admin';
  loginForm.password = 'admin123';
  errorMessage.value = '';
}

async function handleLogin() {
  loading.value = true;
  errorMessage.value = '';
  successMessage.value = '';
  try {
    const data = await authStore.login(loginForm.username, loginForm.password);
    const user = data.user || {};
    const isAdmin = Boolean(
      user.is_staff || 
      user.is_superuser || 
      user.role === 'admin' || 
      user.username === 'admin' ||
      (user.email && user.email.toLowerCase().includes('admin'))
    );
    const roleLabel = isAdmin ? 'Studio Administrator' : 'Client';
    
    successMessage.value = `Welcome back, ${user.name || user.username}! Verified as ${roleLabel}.`;
    bookingStore.showToast(`Logged in as ${roleLabel}`, 'success');

    let targetRoute = route.query.redirect;
    if (isAdmin) {
      // For admins, default to /admin/overview unless they came specifically with an /admin destination
      if (!targetRoute || !targetRoute.startsWith('/admin')) {
        targetRoute = '/admin/overview';
      }
    } else {
      // For clients, ensure they don't land on admin routes
      if (!targetRoute || targetRoute.startsWith('/admin')) {
        targetRoute = '/home';
      }
    }

    setTimeout(() => {
      router.push(targetRoute);
    }, 250);
  } catch (err) {
    errorMessage.value = err.message || 'Login failed. Please check your credentials.';
  } finally {
    loading.value = false;
  }
}

async function handleSignUp() {
  loading.value = true;
  errorMessage.value = '';
  successMessage.value = '';
  try {
    const data = await authStore.signup({
      name: signUpForm.name,
      username: signUpForm.username,
      email: signUpForm.email,
      phone: signUpForm.phone,
      password: signUpForm.password
    });
    successMessage.value = 'Account created with 1 complimentary pass! Redirecting...';
    bookingStore.showToast('Account created successfully!', 'success');

    setTimeout(() => {
      const redirect = route.query.redirect || '/home';
      router.push(redirect);
    }, 1000);
  } catch (err) {
    errorMessage.value = err.message || 'Signup failed. Please try again.';
  } finally {
    loading.value = false;
  }
}
</script>
