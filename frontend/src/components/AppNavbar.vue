<template>
  <header class="fixed top-0 left-0 right-0 z-50 bg-surface-container-lowest/85 dark:bg-slate-900/85 backdrop-blur-xl shadow-[0_1px_8px_rgba(10,42,94,0.05)] border-b border-outline-variant/20 dark:border-slate-800/80 transition-colors duration-200">
    <div class="max-w-7xl mx-auto h-16 sm:h-[72px] px-3.5 sm:px-6 lg:px-8 flex items-center justify-between gap-3 sm:gap-4">
      <!-- Left: Logo & Brand Anchor -->
      <router-link to="/" class="flex items-center gap-2.5 sm:gap-3 shrink-0 group">
        <div class="w-9 h-9 sm:w-10 sm:h-10 rounded-full bg-secondary-fixed flex items-center justify-center text-primary shadow-xs shrink-0 group-hover:scale-105 transition-transform">
          <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" stroke-linecap="round" stroke-width="6" viewBox="0 0 100 100">
            <circle cx="42" cy="24" r="10"></circle>
            <path d="M26 34 C44 33, 52 42, 40 55 C34 62, 35 74, 46 80"></path>
            <circle cx="62" cy="24" r="10" stroke="#7DA2D0"></circle>
            <path d="M46 34 C64 33, 72 42, 60 55 C54 62, 55 74, 66 80" stroke="#7DA2D0"></path>
          </svg>
        </div>
        <div class="flex flex-col">
          <span class="font-headline-sm text-sm sm:text-base font-bold tracking-tight text-primary-container dark:text-white leading-tight">YOUR TRAINER</span>
          <span class="font-eyebrow text-[10px] sm:text-eyebrow uppercase tracking-widest text-secondary font-medium -mt-0.5 sm:-mt-space-xs">by Karina</span>
        </div>
      </router-link>

      <!-- Center: Decluttered Primary Consumer Destinations (Desktop only) -->
      <nav class="hidden md:flex items-center gap-7 lg:gap-9 shrink-0">
        <router-link 
          to="/" 
          class="font-label-md text-sm transition-colors py-1 hover:text-primary-container dark:hover:text-white"
          :class="$route.path === '/' ? 'text-primary-container dark:text-white font-bold' : 'text-on-surface-variant dark:text-slate-400 font-medium'"
        >
          Home
        </router-link>

        <router-link 
          to="/services" 
          class="font-label-md text-sm transition-colors py-1 hover:text-primary-container dark:hover:text-white"
          :class="$route.path.startsWith('/services') ? 'text-primary-container dark:text-white font-bold' : 'text-on-surface-variant dark:text-slate-400 font-medium'"
        >
          Services
        </router-link>

        <router-link 
          to="/book" 
          class="font-label-md text-sm transition-colors py-1 hover:text-primary-container dark:hover:text-white"
          :class="$route.path.startsWith('/book') ? 'text-primary-container dark:text-white font-bold' : 'text-on-surface-variant dark:text-slate-400 font-medium'"
        >
          Schedule &amp; Book
        </router-link>

        <router-link 
          to="/bookings" 
          class="font-label-md text-sm transition-colors py-1 hover:text-primary-container dark:hover:text-white"
          :class="$route.path === '/bookings' ? 'text-primary-container dark:text-white font-bold' : 'text-on-surface-variant dark:text-slate-400 font-medium'"
        >
          My Passes
        </router-link>
      </nav>

      <!-- Right: Streamlined Controls (Desktop & Mobile) -->
      <div class="flex items-center gap-2 sm:gap-3 shrink-0">
        <!-- Compact Currency Switcher (Hidden on narrow mobile, available in drawer) -->
        <div class="hidden sm:flex items-center bg-surface-container-low dark:bg-slate-800 p-0.5 rounded-full border border-outline-variant/30 dark:border-slate-700 shadow-2xs">
          <button 
            @click="bookingStore.setCurrency('KES')"
            :class="bookingStore.currency.value === 'KES' ? 'bg-surface-container-lowest dark:bg-slate-700 text-primary-container dark:text-white font-bold shadow-xs' : 'text-on-surface-variant dark:text-slate-400 hover:text-on-surface'"
            class="px-2.5 py-0.5 rounded-full font-label-sm text-[11px] transition-all"
            type="button"
          >
            KES
          </button>
          <button 
            @click="bookingStore.setCurrency('EUR')"
            :class="bookingStore.currency.value === 'EUR' ? 'bg-surface-container-lowest dark:bg-slate-700 text-primary-container dark:text-white font-bold shadow-xs' : 'text-on-surface-variant dark:text-slate-400 hover:text-on-surface'"
            class="px-2.5 py-0.5 rounded-full font-label-sm text-[11px] transition-all"
            type="button"
          >
            EUR
          </button>
        </div>

        <!-- Dark / Light Mode Toggle Button -->
        <button 
          @click="themeStore.toggleTheme()" 
          class="w-9 h-9 rounded-full bg-surface-container-low dark:bg-slate-800 flex items-center justify-center text-on-surface-variant dark:text-slate-300 hover:text-primary-container dark:hover:text-white transition-colors shrink-0" 
          :title="themeStore.isDark.value ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
          type="button"
        >
          <span class="material-symbols-outlined text-lg">{{ themeStore.isDark.value ? 'light_mode' : 'dark_mode' }}</span>
        </button>

        <!-- User Profile Dropdown or Guest Actions -->
        <div v-if="authStore.isAuthenticated.value" class="relative shrink-0">
          <button 
            @click="showUserMenu = !showUserMenu" 
            :class="[
              avatarShapeClass,
              'w-9 h-9 overflow-hidden flex items-center justify-center ring-2 ring-secondary/30 hover:ring-secondary/70 focus:outline-none transition-all shrink-0 bg-surface-container-low dark:bg-slate-800'
            ]"
            type="button"
            aria-label="User account menu"
          >
            <img 
              v-if="userAvatarUrl && !avatarFailed" 
              alt="Profile" 
              :class="[avatarPositionClass, 'w-full h-full object-cover']" 
              :src="userAvatarUrl" 
              @error="avatarFailed = true"
            />
            <div 
              v-else 
              class="w-full h-full bg-secondary-container dark:bg-sky-950 text-primary-container dark:text-sky-200 font-bold flex items-center justify-center text-xs shadow-inner"
            >
              {{ userInitial }}
            </div>
          </button>

          <!-- Dropdown Popover -->
          <div 
            v-if="showUserMenu" 
            @click="showUserMenu = false"
            class="absolute right-0 mt-2 w-56 sm:w-60 max-w-[calc(100vw-1.5rem)] bg-surface-container-lowest dark:bg-slate-900 rounded-3xl shadow-2xl border border-outline-variant/30 dark:border-slate-800 py-2.5 z-50 animate-fadeIn"
          >
            <div class="px-4 py-2 border-b border-outline-variant/20 dark:border-slate-800">
              <p class="font-label-md text-sm text-primary-container dark:text-white font-bold truncate">
                {{ authStore.user.value.name || authStore.user.value.username }}
              </p>
              <p class="font-body-sm text-[11px] text-on-surface-variant dark:text-slate-400 truncate">
                {{ authStore.user.value.email }}
              </p>
              <div v-if="authStore.isAdmin.value" class="mt-1">
                <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 font-label-sm text-[10px] font-semibold border border-emerald-200 dark:border-emerald-800">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> Verified Admin
                </span>
              </div>
            </div>

            <!-- Profile & Personal Data Link (Accessible to both clients and admins) -->
            <router-link 
              to="/profile" 
              class="flex items-center gap-2.5 px-4 py-2.5 text-on-surface dark:text-slate-200 hover:bg-surface-container-low dark:hover:bg-slate-800 text-xs transition-colors font-medium"
            >
              <span class="material-symbols-outlined text-base text-secondary">person</span>
              <span>My Profile &amp; Settings</span>
            </router-link>

            <!-- Discrete Admin Portal Link (ONLY visible if verified admin) -->
            <router-link 
              v-if="authStore.isAdmin.value" 
              to="/admin/overview" 
              class="flex items-center gap-2.5 px-4 py-2.5 text-primary-container dark:text-sky-300 font-semibold hover:bg-surface-container-low dark:hover:bg-slate-800 text-xs transition-colors"
            >
              <span class="material-symbols-outlined text-base text-secondary">admin_panel_settings</span>
              <span>Admin Portal</span>
            </router-link>

            <router-link 
              to="/bookings" 
              class="flex items-center gap-2.5 px-4 py-2.5 text-on-surface dark:text-slate-200 hover:bg-surface-container-low dark:hover:bg-slate-800 text-xs transition-colors"
            >
              <span class="material-symbols-outlined text-base text-secondary">confirmation_number</span>
              <span>My Passes &amp; Bookings</span>
            </router-link>

            <div class="pt-1.5 mt-1 border-t border-outline-variant/20 dark:border-slate-800">
              <button 
                @click="handleLogout" 
                class="w-full flex items-center gap-2.5 px-4 py-2 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/30 text-xs text-left transition-colors"
              >
                <span class="material-symbols-outlined text-base">logout</span>
                <span>Sign Out</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Guest Actions: Sign In + Book Now -->
        <div v-else class="flex items-center gap-2">
          <router-link 
            to="/login" 
            class="hidden sm:inline-flex font-label-sm text-xs font-semibold text-secondary hover:text-primary-container dark:hover:text-white transition-colors px-2 py-1"
          >
            Sign In
          </router-link>

          <router-link 
            to="/book" 
            class="inline-flex items-center justify-center bg-primary-container hover:bg-primary text-white font-label-sm text-xs px-3.5 sm:px-4 py-1.5 sm:py-2 rounded-full shadow-xs transition-all active:scale-95 font-bold"
          >
            Book Now
          </router-link>
        </div>

        <!-- Mobile Hamburger Button (<768px) -->
        <button 
          @click="mobileMenuOpen = !mobileMenuOpen" 
          class="md:hidden w-9 h-9 rounded-full bg-surface-container-low dark:bg-slate-800 flex items-center justify-center text-on-surface dark:text-slate-200 hover:bg-surface-container transition-colors shrink-0"
          type="button"
          aria-label="Toggle mobile menu"
        >
          <span class="material-symbols-outlined text-xl">
            {{ mobileMenuOpen ? 'close' : 'menu' }}
          </span>
        </button>
      </div>
    </div>

    <!-- Mobile Slide-out Drawer Menu -->
    <div 
      v-if="mobileMenuOpen" 
      class="md:hidden bg-surface-container-lowest/95 dark:bg-slate-900/95 backdrop-blur-xl border-b border-outline-variant/30 dark:border-slate-800 px-5 py-5 flex flex-col gap-3 shadow-2xl animate-fadeIn"
    >
      <router-link 
        @click="mobileMenuOpen = false" 
        to="/" 
        class="font-headline-sm text-base text-primary-container dark:text-white py-1.5 flex items-center justify-between"
      >
        <span>Home</span>
        <span class="material-symbols-outlined text-sm text-secondary">chevron_right</span>
      </router-link>

      <router-link 
        @click="mobileMenuOpen = false" 
        to="/services" 
        class="font-headline-sm text-base text-primary-container dark:text-white py-1.5 flex items-center justify-between"
      >
        <span>Services &amp; Offerings</span>
        <span class="material-symbols-outlined text-sm text-secondary">chevron_right</span>
      </router-link>

      <router-link 
        @click="mobileMenuOpen = false" 
        to="/book" 
        class="font-headline-sm text-base text-primary-container dark:text-white py-1.5 flex items-center justify-between"
      >
        <span>Schedule &amp; Book</span>
        <span class="material-symbols-outlined text-sm text-secondary">chevron_right</span>
      </router-link>

      <router-link 
        @click="mobileMenuOpen = false" 
        to="/bookings" 
        class="font-headline-sm text-base text-primary-container dark:text-white py-1.5 flex items-center justify-between"
      >
        <span>My Passes &amp; Bookings</span>
        <span class="material-symbols-outlined text-sm text-secondary">chevron_right</span>
      </router-link>

      <!-- Profile View / Edit (Accessible when logged in) -->
      <router-link 
        v-if="authStore.isAuthenticated.value"
        @click="mobileMenuOpen = false" 
        to="/profile" 
        class="font-headline-sm text-base text-primary-container dark:text-white py-1.5 flex items-center justify-between"
      >
        <span class="flex items-center gap-2">
          <span class="material-symbols-outlined text-secondary text-base">person</span>
          My Profile &amp; Settings
        </span>
        <span class="material-symbols-outlined text-sm text-secondary">chevron_right</span>
      </router-link>

      <!-- Admin Portal (ONLY visible to verified admin in drawer) -->
      <router-link 
        v-if="authStore.isAdmin.value"
        @click="mobileMenuOpen = false" 
        to="/admin/overview" 
        class="font-headline-sm text-base text-primary-container dark:text-sky-300 py-1.5 flex items-center justify-between font-semibold"
      >
        <span class="flex items-center gap-2">
          <span class="material-symbols-outlined text-secondary text-base">admin_panel_settings</span>
          Admin Portal
        </span>
        <span class="material-symbols-outlined text-sm text-secondary">chevron_right</span>
      </router-link>

      <!-- Mobile Settings Bar: Currency + Theme -->
      <div class="pt-3 border-t border-outline-variant/20 dark:border-slate-800 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="font-label-sm text-xs text-on-surface-variant dark:text-slate-400">Currency</span>
          <div class="flex items-center bg-surface-container-low dark:bg-slate-800 p-0.5 rounded-full border border-outline-variant/30 dark:border-slate-700">
            <button 
              @click="bookingStore.setCurrency('KES')"
              :class="bookingStore.currency.value === 'KES' ? 'bg-surface-container-lowest dark:bg-slate-700 text-primary-container dark:text-white font-bold shadow-xs' : 'text-on-surface-variant dark:text-slate-400'"
              class="px-2.5 py-0.5 rounded-full font-label-sm text-[11px] transition-all"
              type="button"
            >
              KES
            </button>
            <button 
              @click="bookingStore.setCurrency('EUR')"
              :class="bookingStore.currency.value === 'EUR' ? 'bg-surface-container-lowest dark:bg-slate-700 text-primary-container dark:text-white font-bold shadow-xs' : 'text-on-surface-variant dark:text-slate-400'"
              class="px-2.5 py-0.5 rounded-full font-label-sm text-[11px] transition-all"
              type="button"
            >
              EUR
            </button>
          </div>
        </div>

        <div>
          <button 
            @click="themeStore.toggleTheme()" 
            class="flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container-low dark:bg-slate-800 text-xs text-on-surface-variant dark:text-slate-300 border border-outline-variant/20 dark:border-slate-700"
            type="button"
          >
            <span class="material-symbols-outlined text-sm">{{ themeStore.isDark.value ? 'light_mode' : 'dark_mode' }}</span>
            <span>{{ themeStore.isDark.value ? 'Light' : 'Dark' }}</span>
          </button>
        </div>
      </div>

      <!-- Mobile Account Controls -->
      <div class="pt-2 border-t border-outline-variant/20 dark:border-slate-800 flex items-center justify-between">
        <span class="font-label-sm text-xs text-on-surface-variant dark:text-slate-400">Account</span>
        <router-link 
          v-if="!authStore.isAuthenticated.value"
          @click="mobileMenuOpen = false" 
          to="/login" 
          class="font-label-md text-xs font-bold text-secondary hover:text-primary-container dark:hover:text-white"
        >
          Sign In / Register
        </router-link>
        <button 
          v-else 
          @click="handleLogout" 
          class="font-label-md text-xs font-bold text-red-600 dark:text-red-400"
        >
          Sign Out
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
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
const avatarFailed = ref(false);

const userAvatarUrl = computed(() => {
  return authStore.user.value?.avatar || authStore.user.value?.avatar_url || null;
});

watch(userAvatarUrl, () => {
  avatarFailed.value = false;
});

const userInitial = computed(() => {
  const name = authStore.user.value?.name || authStore.user.value?.first_name || authStore.user.value?.username || 'S';
  return name.charAt(0).toUpperCase();
});

const avatarShapeClass = computed(() => {
  const shape = authStore.user.value?.avatar_shape || 'circle';
  if (shape === 'squircle') return 'rounded-2xl';
  if (shape === 'square') return 'rounded-lg';
  return 'rounded-full';
});

const avatarPositionClass = computed(() => {
  const pos = authStore.user.value?.avatar_position || 'center';
  if (pos === 'top') return 'object-top';
  if (pos === 'bottom') return 'object-bottom';
  if (pos === 'left') return 'object-left';
  if (pos === 'right') return 'object-right';
  return 'object-center';
});

function handleLogout() {
  showUserMenu.value = false;
  mobileMenuOpen.value = false;
  authStore.logout();
  bookingStore.showToast('You have been signed out.', 'info');
  router.push('/');
}
</script>
