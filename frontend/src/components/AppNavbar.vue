<template>
  <header class="fixed top-0 left-0 right-0 z-50 bg-surface-container-lowest/90 dark:bg-slate-900/90 backdrop-blur-xl shadow-[0_1px_8px_rgba(10,42,94,0.06)] border-b border-outline-variant/20 dark:border-slate-800 transition-colors duration-200">
    <div class="max-w-7xl mx-auto h-20 px-4 sm:px-6 lg:px-8 flex items-center justify-between gap-4">
      <!-- Left: Logo & Brand Anchor -->
      <router-link to="/" class="flex items-center gap-3 shrink-0 group">
        <div class="w-10 h-10 rounded-full bg-secondary-fixed flex items-center justify-center text-primary shadow-xs shrink-0 group-hover:scale-105 transition-transform">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-linecap="round" stroke-width="6" viewBox="0 0 100 100">
            <circle cx="42" cy="24" r="10"></circle>
            <path d="M26 34 C44 33, 52 42, 40 55 C34 62, 35 74, 46 80"></path>
            <circle cx="62" cy="24" r="10" stroke="#7DA2D0"></circle>
            <path d="M46 34 C64 33, 72 42, 60 55 C54 62, 55 74, 66 80" stroke="#7DA2D0"></path>
          </svg>
        </div>
        <div class="flex flex-col">
          <span class="font-headline-sm text-headline-sm font-semibold tracking-tight text-primary-container dark:text-white leading-tight">YOUR TRAINER</span>
          <span class="font-eyebrow text-eyebrow uppercase tracking-widest text-secondary font-medium -mt-space-xs">by Karina</span>
        </div>
      </router-link>

      <!-- Center: Decluttered 4 Primary Destinations (Desktop only) -->
      <nav class="hidden md:flex items-center gap-6 lg:gap-8 shrink-0">
        <router-link 
          to="/" 
          class="font-label-md text-label-md transition-colors py-1 hover:text-primary-container dark:hover:text-white"
          :class="$route.path === '/' ? 'text-primary-container dark:text-white font-semibold' : 'text-on-surface-variant dark:text-slate-400'"
        >
          Home
        </router-link>

        <router-link 
          to="/services" 
          class="font-label-md text-label-md transition-colors py-1 hover:text-primary-container dark:hover:text-white"
          :class="$route.path.startsWith('/services') ? 'text-primary-container dark:text-white font-semibold' : 'text-on-surface-variant dark:text-slate-400'"
        >
          Services
        </router-link>

        <router-link 
          to="/book" 
          class="font-label-md text-label-md transition-colors py-1 hover:text-primary-container dark:hover:text-white"
          :class="$route.path.startsWith('/book') ? 'text-primary-container dark:text-white font-semibold' : 'text-on-surface-variant dark:text-slate-400'"
        >
          Schedule &amp; Book
        </router-link>

        <router-link 
          to="/bookings" 
          class="font-label-md text-label-md transition-colors py-1 hover:text-primary-container dark:hover:text-white"
          :class="$route.path === '/bookings' ? 'text-primary-container dark:text-white font-semibold' : 'text-on-surface-variant dark:text-slate-400'"
        >
          My Passes
        </router-link>
      </nav>

      <!-- Right: Streamlined Controls (Desktop & Mobile) -->
      <div class="flex items-center gap-2 sm:gap-3 shrink-0">
        <!-- Compact Currency Switcher -->
        <div class="flex items-center bg-surface-container-low dark:bg-slate-800 p-0.5 rounded-full border border-outline-variant/30 dark:border-slate-700">
          <button 
            @click="bookingStore.setCurrency('KES')"
            :class="bookingStore.currency.value === 'KES' ? 'bg-surface-container-lowest dark:bg-slate-700 text-primary-container dark:text-white font-semibold shadow-xs' : 'text-on-surface-variant dark:text-slate-400 hover:text-on-surface'"
            class="px-2 py-0.5 rounded-full font-label-sm text-xs transition-all"
            type="button"
          >
            KES
          </button>
          <button 
            @click="bookingStore.setCurrency('EUR')"
            :class="bookingStore.currency.value === 'EUR' ? 'bg-surface-container-lowest dark:bg-slate-700 text-primary-container dark:text-white font-semibold shadow-xs' : 'text-on-surface-variant dark:text-slate-400 hover:text-on-surface'"
            class="px-2 py-0.5 rounded-full font-label-sm text-xs transition-all"
            type="button"
          >
            EUR
          </button>
        </div>

        <!-- Dark / Light Mode Toggle Button -->
        <button 
          @click="themeStore.toggleTheme()" 
          class="w-9 h-9 rounded-full bg-surface-container-low dark:bg-slate-800 flex items-center justify-center text-on-surface-variant dark:text-slate-300 hover:text-primary-container dark:hover:text-white transition-colors" 
          :title="themeStore.isDark.value ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
          type="button"
        >
          <span class="material-symbols-outlined text-lg">{{ themeStore.isDark.value ? 'light_mode' : 'dark_mode' }}</span>
        </button>

        <!-- User Profile Dropdown or Sign In -->
        <div v-if="authStore.isAuthenticated.value" class="relative">
          <button 
            @click="showUserMenu = !showUserMenu" 
            class="flex items-center gap-2 focus:outline-none"
            type="button"
          >
            <img 
              alt="Profile" 
              class="w-9 h-9 rounded-full object-cover shadow-sm ring-2 ring-secondary/30" 
              :src="authStore.user.value.avatar || 'https://lh3.googleusercontent.com/aida/AEtjO1UwxvO7_3GTbgWd4EMPt4rt_w381oAezID3bV9-NdwIdn55FZ_9EuUxkek0b1g_CCD7OREkS7yHj5Cgb747yd7hji3o7wMsF5yMWX7Y-9WXeuNJSV87pRW9T6yotkdPzul6-kYjIysNWHJ6rcSRnoCnngzil7rsid2c6iewLxqYX2u5vPcQFLY7r3ZEkPxwmhnE8RfShmfVHjQTEbYJSi9MwKlsQzRFBydQI4ftgATXc7O0xLaTmJmS44Z2gA8121FAes4FrKhN'" 
            />
          </button>

          <!-- Dropdown Popover -->
          <div 
            v-if="showUserMenu" 
            @click="showUserMenu = false"
            class="absolute right-0 mt-2 w-56 bg-surface-container-lowest dark:bg-slate-900 rounded-2xl shadow-xl border border-outline-variant/30 dark:border-slate-800 py-2 z-50 animate-fadeIn"
          >
            <div class="px-4 py-2 border-b border-outline-variant/20 dark:border-slate-800">
              <p class="font-label-md text-label-md text-primary-container dark:text-white font-semibold truncate">
                {{ authStore.user.value.name || authStore.user.value.username }}
              </p>
              <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400 truncate">
                {{ authStore.user.value.email }}
              </p>
            </div>
            <router-link to="/bookings" class="flex items-center gap-2 px-4 py-2.5 text-on-surface dark:text-slate-200 hover:bg-surface-container-low dark:hover:bg-slate-800 text-sm">
              <span class="material-symbols-outlined text-lg text-secondary">event_available</span>
              <span>My Passes &amp; Bookings</span>
            </router-link>
            <button 
              @click="handleLogout" 
              class="w-full flex items-center gap-2 px-4 py-2.5 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/30 text-sm text-left"
            >
              <span class="material-symbols-outlined text-lg">logout</span>
              <span>Sign Out</span>
            </button>
          </div>
        </div>

        <!-- Guest Links: Sign In + Book Session -->
        <div v-else class="flex items-center gap-2">
          <router-link 
            to="/login" 
            class="hidden sm:inline-flex font-label-sm text-label-sm text-secondary hover:text-primary-container dark:hover:text-white transition-colors px-2 font-medium"
          >
            Sign In
          </router-link>

          <router-link 
            to="/book" 
            class="inline-flex items-center justify-center bg-primary-container hover:bg-primary text-on-primary font-label-md text-xs sm:text-label-md px-3.5 sm:px-5 py-2 rounded-full shadow-sm transition-all active:scale-[0.98] font-semibold"
          >
            Book Now
          </router-link>
        </div>

        <!-- Mobile Hamburger Button (<768px) -->
        <button 
          @click="mobileMenuOpen = !mobileMenuOpen" 
          class="md:hidden w-9 h-9 rounded-full bg-surface-container-low dark:bg-slate-800 flex items-center justify-center text-on-surface dark:text-slate-200"
          type="button"
          aria-label="Toggle mobile menu"
        >
          <span class="material-symbols-outlined text-2xl">
            {{ mobileMenuOpen ? 'close' : 'menu' }}
          </span>
        </button>
      </div>
    </div>

    <!-- Mobile Slide-out Drawer Menu -->
    <div 
      v-if="mobileMenuOpen" 
      class="md:hidden bg-surface-container-lowest dark:bg-slate-900 border-b border-outline-variant/30 dark:border-slate-800 px-6 py-6 flex flex-col gap-4 shadow-xl"
    >
      <router-link 
        @click="mobileMenuOpen = false" 
        to="/" 
        class="font-headline-sm text-headline-sm text-primary-container dark:text-white py-1 flex items-center justify-between"
      >
        <span>Home</span>
        <span class="material-symbols-outlined text-sm text-secondary">chevron_right</span>
      </router-link>

      <router-link 
        @click="mobileMenuOpen = false" 
        to="/services" 
        class="font-headline-sm text-headline-sm text-primary-container dark:text-white py-1 flex items-center justify-between"
      >
        <span>Services &amp; Workshops</span>
        <span class="material-symbols-outlined text-sm text-secondary">chevron_right</span>
      </router-link>

      <router-link 
        @click="mobileMenuOpen = false" 
        to="/book" 
        class="font-headline-sm text-headline-sm text-primary-container dark:text-white py-1 flex items-center justify-between"
      >
        <span>Schedule &amp; Book</span>
        <span class="material-symbols-outlined text-sm text-secondary">chevron_right</span>
      </router-link>

      <router-link 
        @click="mobileMenuOpen = false" 
        to="/bookings" 
        class="font-headline-sm text-headline-sm text-primary-container dark:text-white py-1 flex items-center justify-between"
      >
        <span>My Passes &amp; Bookings</span>
        <span class="material-symbols-outlined text-sm text-secondary">chevron_right</span>
      </router-link>

      <div class="pt-4 border-t border-outline-variant/20 dark:border-slate-800 flex items-center justify-between">
        <span class="font-label-sm text-label-sm text-on-surface-variant dark:text-slate-400">Account</span>
        <router-link 
          v-if="!authStore.isAuthenticated.value"
          @click="mobileMenuOpen = false" 
          to="/login" 
          class="font-label-md text-label-md font-semibold text-secondary hover:text-primary-container dark:hover:text-white"
        >
          Sign In / Register
        </router-link>
        <button 
          v-else 
          @click="handleLogout" 
          class="font-label-md text-label-md font-semibold text-red-600 dark:text-red-400"
        >
          Sign Out
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useBookingStore } from '@/stores/bookingStore';
import { useThemeStore } from '@/stores/themeStore';
import { useAuthStore } from '@/stores/authStore';

const router = useRouter();
const bookingStore = useBookingStore();
const themeStore = useThemeStore();
const authStore = useAuthStore();

const showUserMenu = ref(false);
const mobileMenuOpen = ref(false);

function handleLogout() {
  showUserMenu.value = false;
  mobileMenuOpen.value = false;
  authStore.logout();
  bookingStore.showToast('You have been signed out.', 'info');
  router.push('/');
}
</script>
