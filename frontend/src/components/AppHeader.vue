<template>
  <header class="fixed top-0 w-full z-50 pt-safe bg-surface/85 dark:bg-slate-900/90 backdrop-blur-xl shadow-[0_1px_12px_rgba(10,42,94,0.04)] border-b border-outline-variant/10 dark:border-slate-800 transition-colors duration-200">
    <div class="max-w-4xl mx-auto h-16 px-gutter-mobile flex items-center justify-between gap-space-sm">
      <div class="flex items-center gap-space-xs min-w-0">
        <!-- Optional Back Button -->
        <button 
          v-if="showBack" 
          aria-label="Back" 
          @click="goBack"
          class="w-11 h-11 flex items-center justify-center rounded-full text-on-surface dark:text-slate-200 hover:text-primary active:scale-95 transition-all"
        >
          <span class="material-symbols-outlined text-[24px]">arrow_back</span>
        </button>

        <router-link to="/home" class="flex items-center gap-space-sm min-w-0 group">
          <div class="w-8 h-8 rounded-full bg-secondary-fixed flex items-center justify-center text-primary shadow-xs shrink-0">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-linecap="round" stroke-width="6" viewBox="0 0 100 100">
              <circle cx="42" cy="24" r="10"></circle>
              <path d="M26 34 C44 33, 52 42, 40 55 C34 62, 35 74, 46 80"></path>
              <circle cx="62" cy="24" r="10" stroke="#7DA2D0"></circle>
              <path d="M46 34 C64 33, 72 42, 60 55 C54 62, 55 74, 66 80" stroke="#7DA2D0"></path>
            </svg>
          </div>
          <div class="flex flex-col truncate">
            <span class="font-eyebrow text-eyebrow text-secondary uppercase tracking-widest leading-none">YOUR TRAINER</span>
            <span class="font-headline-sm text-headline-sm text-primary dark:text-white tracking-tight font-bold truncate leading-snug">
              {{ title || 'by Karina' }}
            </span>
          </div>
        </router-link>
      </div>

      <!-- Right Header Actions -->
      <div class="flex items-center gap-space-xs shrink-0">
        <!-- Theme Toggle Button -->
        <button 
          aria-label="Toggle Theme" 
          @click="themeStore.toggleTheme()"
          class="w-10 h-10 flex items-center justify-center rounded-full text-on-surface-variant dark:text-slate-300 hover:text-primary dark:hover:text-white active:scale-95 transition-all"
          :title="themeStore.isDark.value ? 'Light mode' : 'Dark mode'"
          type="button"
        >
          <span class="material-symbols-outlined text-[22px]">
            {{ themeStore.isDark.value ? 'light_mode' : 'dark_mode' }}
          </span>
        </button>

        <button 
          aria-label="Notifications" 
          @click="onNotificationClick"
          class="relative w-10 h-10 flex items-center justify-center rounded-full text-on-surface-variant dark:text-slate-300 hover:text-primary dark:hover:text-white active:scale-95 transition-all"
        >
          <span class="material-symbols-outlined text-[22px]">notifications</span>
          <span class="absolute top-2 right-2 w-2 h-2 rounded-full bg-secondary ring-2 ring-surface dark:ring-slate-900"></span>
        </button>

        <router-link 
          v-if="!authStore.isAuthenticated.value"
          to="/login"
          class="text-xs font-semibold px-3 py-1.5 rounded-full bg-secondary-fixed text-primary hover:opacity-90 transition-all"
        >
          Login
        </router-link>

        <router-link 
          v-else
          to="/bookings" 
          aria-label="Profile" 
          class="w-10 h-10 flex items-center justify-center rounded-full active:scale-95 transition-all focus:outline-none"
        >
          <img 
            alt="Profile" 
            class="w-8 h-8 rounded-full object-cover shadow-[0_2px_8px_rgba(10,42,94,0.12)] ring-1 ring-secondary/30" 
            :src="user.avatar" 
          />
        </router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useBookingStore } from '@/stores/bookingStore';
import { useThemeStore } from '@/stores/themeStore';
import { useAuthStore } from '@/stores/authStore';

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  showBack: {
    type: Boolean,
    default: false
  }
});

const router = useRouter();
const route = useRoute();
const { user, showToast } = useBookingStore();
const themeStore = useThemeStore();
const authStore = useAuthStore();

function goBack() {
  if (window.history.length > 1) {
    router.back();
  } else {
    router.push('/home');
  }
}

function onNotificationClick() {
  showToast('You have 1 upcoming session tomorrow at 09:30 AM 🌿');
}
</script>
