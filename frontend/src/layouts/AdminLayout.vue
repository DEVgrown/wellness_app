<template>
  <div class="min-h-screen bg-surface dark:bg-slate-950 text-on-surface dark:text-slate-100 flex flex-col transition-colors duration-200">
    <!-- Desktop Admin Wrapper -->
    <div class="flex flex-1 min-h-screen">
      <!-- Left Sidebar (Desktop >= 1024px) -->
      <aside class="hidden lg:flex flex-col w-64 bg-surface-container-lowest dark:bg-slate-900 border-r border-outline-variant/30 dark:border-slate-800 p-5 shrink-0 justify-between">
        <div>
          <!-- Brand Anchor -->
          <router-link to="/admin/overview" class="flex items-center gap-3 mb-8 group">
            <div class="w-10 h-10 rounded-2xl bg-primary-container dark:bg-sky-500 text-white dark:text-slate-950 flex items-center justify-center shadow-sm shrink-0 group-hover:scale-105 transition-transform">
              <span class="material-symbols-outlined text-xl">admin_panel_settings</span>
            </div>
            <div>
              <span class="font-headline-sm text-base font-bold text-primary-container dark:text-white block leading-tight">
                Studio Admin
              </span>
              <span class="font-eyebrow text-[10px] uppercase tracking-widest text-secondary font-semibold">
                Karina Wellness
              </span>
            </div>
          </router-link>

          <!-- Navigation Links -->
          <nav class="space-y-1.5">
            <router-link
              v-for="item in navItems"
              :key="item.to"
              :to="item.to"
              class="flex items-center gap-3 px-3.5 py-2.5 rounded-2xl font-label-md text-xs font-semibold transition-all group"
              :class="$route.path === item.to || ($route.path.startsWith(item.to) && item.to !== '/admin') ? 'bg-primary-container text-white dark:bg-sky-500 dark:text-slate-950 shadow-xs' : 'text-on-surface-variant dark:text-slate-400 hover:bg-surface-container-low dark:hover:bg-slate-800 hover:text-on-surface'"
            >
              <span class="material-symbols-outlined text-lg transition-transform group-hover:scale-110">{{ item.icon }}</span>
              <span>{{ item.label }}</span>
            </router-link>
          </nav>
        </div>

        <!-- Sidebar Footer -->
        <div class="pt-4 border-t border-outline-variant/20 dark:border-slate-800 space-y-3">
          <router-link
            to="/services"
            class="flex items-center justify-between w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 text-secondary hover:text-primary-container dark:hover:text-white font-label-sm text-xs transition-colors"
          >
            <span class="flex items-center gap-2">
              <span class="material-symbols-outlined text-sm">storefront</span>
              <span>Client Storefront</span>
            </span>
            <span class="material-symbols-outlined text-xs">arrow_forward</span>
          </router-link>

          <!-- Current Admin Profile Snippet -->
          <div class="flex items-center justify-between px-1">
            <router-link to="/admin/profile" class="flex items-center gap-2.5 overflow-hidden group hover:opacity-90 transition-opacity">
              <div class="w-8 h-8 rounded-full overflow-hidden bg-primary-container text-white font-bold flex items-center justify-center text-xs shrink-0 ring-1 ring-secondary/30">
                <img
                  v-if="adminAvatarUrl && !adminAvatarFailed"
                  :src="adminAvatarUrl"
                  alt="Admin Avatar"
                  class="w-full h-full object-cover"
                  @error="adminAvatarFailed = true"
                />
                <span v-else>{{ adminInitial }}</span>
              </div>
              <div class="truncate">
                <p class="font-label-md text-xs font-bold text-primary-container dark:text-white truncate group-hover:text-secondary transition-colors">
                  {{ authStore.user.value?.name || authStore.user.value?.username }}
                </p>
                <p class="font-body-sm text-[10px] text-emerald-600 dark:text-emerald-400 font-semibold flex items-center gap-1">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> Verified Admin
                </p>
              </div>
            </router-link>
            <button
              @click="handleLogout"
              class="w-7 h-7 rounded-full text-red-500 hover:bg-red-50 dark:hover:bg-red-950 flex items-center justify-center transition-colors"
              title="Sign Out"
              type="button"
            >
              <span class="material-symbols-outlined text-sm">logout</span>
            </button>
          </div>
        </div>
      </aside>

      <!-- Main Column -->
      <div class="flex-1 flex flex-col min-w-0">
        <!-- Top Sticky Header -->
        <header class="sticky top-0 z-30 bg-surface-container-lowest/85 dark:bg-slate-900/85 backdrop-blur-xl border-b border-outline-variant/30 dark:border-slate-800/80 px-3.5 sm:px-6 lg:px-8 h-[68px] flex items-center justify-between gap-3">
          <!-- Left: Mobile Menu Trigger + Breadcrumb + Live Indicator -->
          <div class="flex items-center gap-2.5 sm:gap-3.5 min-w-0">
            <button
              @click="mobileDrawerOpen = !mobileDrawerOpen"
              class="lg:hidden w-9 h-9 rounded-2xl bg-surface-container-low dark:bg-slate-800 flex items-center justify-center text-on-surface hover:bg-surface-container shrink-0 transition-colors"
              type="button"
              aria-label="Open navigation drawer"
            >
              <span class="material-symbols-outlined text-xl">menu</span>
            </button>
            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <span class="font-eyebrow text-[10px] text-secondary uppercase tracking-widest font-semibold hidden xs:inline-block">Admin Portal</span>
                <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 font-label-sm text-[10px] font-semibold border border-emerald-200/80 dark:border-emerald-800/60 shadow-xs">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                  <span class="hidden sm:inline">Studio Live</span>
                  <span class="sm:hidden">Live</span>
                </span>
              </div>
              <h2 class="font-headline-sm text-sm sm:text-base lg:text-lg font-bold text-primary-container dark:text-white capitalize truncate leading-tight mt-0.5">
                {{ currentSectionTitle }}
              </h2>
            </div>
          </div>

          <!-- Right Controls -->
          <div class="flex items-center gap-2 sm:gap-3 shrink-0">
            <!-- Live Date & Clock (Desktop) -->
            <div class="hidden xl:flex items-center gap-2 px-3 py-1.5 rounded-full bg-surface-container-low dark:bg-slate-800/80 text-on-surface-variant dark:text-slate-300 font-mono text-xs border border-outline-variant/20 dark:border-slate-800">
              <span class="material-symbols-outlined text-sm text-secondary">schedule</span>
              <span>{{ liveTime }}</span>
            </div>

            <!-- Currency toggle -->
            <div class="flex items-center bg-surface-container-low dark:bg-slate-800 p-0.5 rounded-full border border-outline-variant/30 dark:border-slate-700 shadow-2xs">
              <button 
                @click="bookingStore.setCurrency('KES')"
                :class="bookingStore.currency.value === 'KES' ? 'bg-surface-container-lowest dark:bg-slate-700 text-primary-container dark:text-white font-bold shadow-xs' : 'text-on-surface-variant dark:text-slate-400 hover:text-on-surface'"
                class="px-2 sm:px-2.5 py-0.5 rounded-full font-label-sm text-[11px] transition-all"
                type="button"
              >
                KES
              </button>
              <button 
                @click="bookingStore.setCurrency('EUR')"
                :class="bookingStore.currency.value === 'EUR' ? 'bg-surface-container-lowest dark:bg-slate-700 text-primary-container dark:text-white font-bold shadow-xs' : 'text-on-surface-variant dark:text-slate-400 hover:text-on-surface'"
                class="px-2 sm:px-2.5 py-0.5 rounded-full font-label-sm text-[11px] transition-all"
                type="button"
              >
                EUR
              </button>
            </div>

            <!-- Dark / Light Theme Toggle -->
            <button
              @click="themeStore.toggleTheme()"
              class="w-9 h-9 rounded-full bg-surface-container-low dark:bg-slate-800 flex items-center justify-center text-on-surface-variant dark:text-slate-300 hover:text-primary-container dark:hover:text-white transition-colors"
              :title="themeStore.isDark.value ? 'Switch to Light' : 'Switch to Dark'"
              type="button"
            >
              <span class="material-symbols-outlined text-lg">{{ themeStore.isDark.value ? 'light_mode' : 'dark_mode' }}</span>
            </button>

            <!-- Storefront Shortcut Button -->
            <router-link
              to="/"
              class="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-surface-container-low hover:bg-surface-container dark:bg-slate-800 dark:hover:bg-slate-750 text-secondary dark:text-sky-300 font-label-sm text-xs font-semibold border border-outline-variant/30 dark:border-slate-700 shadow-2xs transition-all"
            >
              <span class="material-symbols-outlined text-sm">storefront</span>
              <span>Client Site</span>
            </router-link>

            <!-- Top-Right Admin Profile Avatar & Popover -->
            <div class="relative">
              <button
                @click="showProfileMenu = !showProfileMenu"
                class="flex items-center gap-2 p-0.5 rounded-full ring-2 ring-primary-container/20 dark:ring-sky-500/30 hover:ring-primary-container/50 transition-all focus:outline-none"
                type="button"
                aria-label="Admin Profile Menu"
              >
                <div class="w-8 h-8 sm:w-9 sm:h-9 rounded-full overflow-hidden bg-primary-container text-white font-bold flex items-center justify-center text-xs shadow-xs relative">
                  <img
                    v-if="adminAvatarUrl && !adminAvatarFailed"
                    :src="adminAvatarUrl"
                    alt="Admin Avatar"
                    class="w-full h-full object-cover"
                    @error="adminAvatarFailed = true"
                  />
                  <span v-else>{{ adminInitial }}</span>
                  <span class="absolute bottom-0 right-0 w-2.5 h-2.5 rounded-full bg-emerald-500 ring-2 ring-white dark:ring-slate-900"></span>
                </div>
              </button>

              <!-- Profile Dropdown Popover -->
              <div
                v-if="showProfileMenu"
                @click="showProfileMenu = false"
                class="absolute right-0 mt-2 w-64 bg-surface-container-lowest dark:bg-slate-900 rounded-3xl shadow-2xl border border-outline-variant/30 dark:border-slate-800 py-3 z-50 animate-fadeIn"
              >
                <div class="px-4 pb-3 border-b border-outline-variant/20 dark:border-slate-800">
                  <div class="flex items-center gap-2 mb-1">
                    <span class="font-label-md text-xs font-bold text-primary-container dark:text-white truncate">
                      {{ authStore.user.value?.name || authStore.user.value?.username }}
                    </span>
                    <span class="px-1.5 py-0.2 rounded-full bg-primary-container/10 dark:bg-sky-950 text-primary-container dark:text-sky-300 text-[10px] font-bold">
                      Admin
                    </span>
                  </div>
                  <p class="font-body-sm text-[11px] text-on-surface-variant dark:text-slate-400 truncate">
                    {{ authStore.user.value?.email || 'admin@karinawellness.com' }}
                  </p>
                </div>

                <div class="py-1">
                  <router-link
                    to="/admin/profile"
                    class="flex items-center gap-2.5 px-4 py-2 text-xs font-semibold text-primary-container dark:text-sky-300 hover:bg-surface-container-low dark:hover:bg-slate-800 transition-colors"
                  >
                    <span class="material-symbols-outlined text-base text-secondary">manage_accounts</span>
                    <span>Admin Profile &amp; Settings</span>
                  </router-link>

                  <router-link
                    to="/"
                    class="flex items-center gap-2.5 px-4 py-2 text-xs font-semibold text-on-surface dark:text-slate-200 hover:bg-surface-container-low dark:hover:bg-slate-800 transition-colors"
                  >
                    <span class="material-symbols-outlined text-base text-secondary">storefront</span>
                    <span>View Client Storefront</span>
                  </router-link>

                  <router-link
                    to="/admin/services"
                    class="flex items-center gap-2.5 px-4 py-2 text-xs font-semibold text-on-surface dark:text-slate-200 hover:bg-surface-container-low dark:hover:bg-slate-800 transition-colors"
                  >
                    <span class="material-symbols-outlined text-base text-secondary">spa</span>
                    <span>Manage Services</span>
                  </router-link>

                  <router-link
                    to="/admin/sessions"
                    class="flex items-center gap-2.5 px-4 py-2 text-xs font-semibold text-on-surface dark:text-slate-200 hover:bg-surface-container-low dark:hover:bg-slate-800 transition-colors"
                  >
                    <span class="material-symbols-outlined text-base text-secondary">calendar_today</span>
                    <span>Scheduling Engine</span>
                  </router-link>
                </div>

                <div class="pt-2 border-t border-outline-variant/20 dark:border-slate-800 px-2">
                  <button
                    @click="handleLogout"
                    class="w-full flex items-center gap-2 px-3 py-2 rounded-xl text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/40 text-xs font-semibold text-left transition-colors"
                    type="button"
                  >
                    <span class="material-symbols-outlined text-base">logout</span>
                    <span>Sign Out</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </header>

        <!-- Nested View Outlet -->
        <main class="flex-1 p-3.5 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto">
          <router-view />
        </main>
      </div>
    </div>

    <!-- Mobile Slide-out Drawer (< 1024px) -->
    <div v-if="mobileDrawerOpen" class="fixed inset-0 z-50 flex lg:hidden bg-black/60 backdrop-blur-xs">
      <div class="w-72 bg-surface-container-lowest dark:bg-slate-900 h-full p-6 flex flex-col justify-between shadow-2xl animate-fadeIn">
        <div>
          <div class="flex items-center justify-between mb-6 pb-4 border-b border-outline-variant/20 dark:border-slate-800">
            <div class="flex items-center gap-2">
              <span class="material-symbols-outlined text-primary-container dark:text-sky-400">admin_panel_settings</span>
              <span class="font-headline-sm text-sm font-bold text-primary-container dark:text-white">Studio Admin</span>
            </div>
            <button @click="mobileDrawerOpen = false" class="w-8 h-8 rounded-full bg-surface-container-low dark:bg-slate-800 flex items-center justify-center text-on-surface">
              &times;
            </button>
          </div>

          <nav class="space-y-1.5">
            <router-link
              v-for="item in navItems"
              :key="item.to"
              :to="item.to"
              @click="mobileDrawerOpen = false"
              class="flex items-center gap-3 px-3.5 py-2.5 rounded-2xl font-label-md text-xs font-semibold transition-all"
              :class="$route.path === item.to ? 'bg-primary-container text-white dark:bg-sky-500 dark:text-slate-950 font-bold' : 'text-on-surface-variant dark:text-slate-300'"
            >
              <span class="material-symbols-outlined text-lg">{{ item.icon }}</span>
              <span>{{ item.label }}</span>
            </router-link>
          </nav>
        </div>

        <div class="pt-4 border-t border-outline-variant/20 dark:border-slate-800 space-y-2">
          <router-link
            to="/services"
            @click="mobileDrawerOpen = false"
            class="flex items-center gap-2 px-3 py-2 rounded-xl text-secondary text-xs font-semibold hover:bg-surface-container-low"
          >
            <span class="material-symbols-outlined text-sm">storefront</span>
            <span>Switch to Client Storefront</span>
          </router-link>

          <button
            @click="handleLogout"
            class="w-full flex items-center gap-2 px-3 py-2 rounded-xl text-red-600 text-xs font-semibold hover:bg-red-50 dark:hover:bg-red-950 text-left"
          >
            <span class="material-symbols-outlined text-sm">logout</span>
            <span>Sign Out</span>
          </button>
        </div>
      </div>
      <div class="flex-1" @click="mobileDrawerOpen = false"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import { useThemeStore } from '@/stores/themeStore';
import { useBookingStore } from '@/stores/bookingStore';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const themeStore = useThemeStore();
const bookingStore = useBookingStore();

const mobileDrawerOpen = ref(false);
const showProfileMenu = ref(false);
const liveTime = ref('');
const adminAvatarFailed = ref(false);
let timer = null;

const adminAvatarUrl = computed(() => {
  return authStore.user.value?.avatar || authStore.user.value?.avatar_url || null;
});

const adminInitial = computed(() => {
  const name = authStore.user.value?.name || authStore.user.value?.first_name || authStore.user.value?.username || 'A';
  return name.charAt(0).toUpperCase();
});

const navItems = [
  { to: '/admin/overview', label: 'Overview & KPIs', icon: 'dashboard' },
  { to: '/admin/services', label: 'Service Offerings', icon: 'spa' },
  { to: '/admin/sessions', label: 'Sessions & Slots', icon: 'calendar_month' },
  { to: '/admin/bookings', label: 'Bookings & Roster', icon: 'event_available' },
  { to: '/admin/customers', label: 'Customers & CRM', icon: 'groups' },
  { to: '/admin/profile', label: 'Profile & Settings', icon: 'manage_accounts' }
];

const currentSectionTitle = computed(() => {
  const p = route.path;
  if (p.includes('/services')) return 'Service Offerings Catalog';
  if (p.includes('/sessions')) return 'Sessions & Scheduling Engine';
  if (p.includes('/bookings')) return 'Client Bookings & Attendance';
  if (p.includes('/customers')) return 'Customers & CRM Directory';
  if (p.includes('/profile')) return 'Administrator Profile & Security';
  return 'Studio Operations Overview';
});

function updateTime() {
  const now = new Date();
  liveTime.value = now.toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric'
  }) + ' ' + now.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit'
  });
}

async function handleLogout() {
  await authStore.logout();
  router.push('/login');
}

onMounted(() => {
  updateTime();
  timer = setInterval(updateTime, 1000);
});

onUnmounted(() => {
  if (timer) clearInterval(timer);
});
</script>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.15s ease-out forwards;
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
