<template>
  <nav class="md:hidden fixed bottom-0 w-full z-40 pb-safe bg-surface-container-lowest/90 dark:bg-slate-900/90 backdrop-blur-xl shadow-[0_-4px_24px_rgba(10,42,94,0.06)] border-t border-outline-variant/20 dark:border-slate-800 transition-colors duration-200">
    <div class="max-w-md mx-auto flex justify-around items-center h-16 px-2">
      <!-- Home Tab -->
      <router-link 
        :to="authStore.isAuthenticated.value ? '/home' : '/'" 
        class="flex flex-col items-center justify-center w-16 h-12 transition-colors group relative"
        :class="(route.path === '/' || route.path === '/home') ? 'text-primary-container dark:text-white font-bold' : 'text-on-surface-variant dark:text-slate-400 hover:text-primary-container'"
      >
        <span class="material-symbols-outlined text-[22px]">spa</span>
        <span class="font-label-sm text-[11px] leading-tight mt-0.5">Home</span>
        <span 
          class="transition-opacity w-1 h-1 rounded-full bg-secondary-container mt-0.5"
          :class="(route.path === '/' || route.path === '/home') ? 'opacity-100' : 'opacity-0'"
        ></span>
      </router-link>

      <!-- Offerings / Services Tab -->
      <router-link 
        to="/services" 
        class="flex flex-col items-center justify-center w-16 h-12 transition-colors group relative"
        :class="route.path.startsWith('/services') ? 'text-primary-container dark:text-white font-bold' : 'text-on-surface-variant dark:text-slate-400 hover:text-primary-container'"
      >
        <span class="material-symbols-outlined text-[22px]">view_cozy</span>
        <span class="font-label-sm text-[11px] leading-tight mt-0.5">Offerings</span>
        <span 
          class="transition-opacity w-1 h-1 rounded-full bg-secondary-container mt-0.5"
          :class="route.path.startsWith('/services') ? 'opacity-100' : 'opacity-0'"
        ></span>
      </router-link>

      <!-- Book / Schedule Tab -->
      <router-link 
        to="/book" 
        class="flex flex-col items-center justify-center w-16 h-12 transition-colors group relative"
        :class="route.path.startsWith('/book') ? 'text-primary-container dark:text-white font-bold' : 'text-on-surface-variant dark:text-slate-400 hover:text-primary-container'"
      >
        <span class="material-symbols-outlined text-[22px]">calendar_month</span>
        <span class="font-label-sm text-[11px] leading-tight mt-0.5">Schedule</span>
        <span 
          class="transition-opacity w-1 h-1 rounded-full bg-secondary-container mt-0.5"
          :class="route.path.startsWith('/book') ? 'opacity-100' : 'opacity-0'"
        ></span>
      </router-link>

      <!-- My Passes / Account Tab -->
      <router-link 
        :to="authStore.isAuthenticated.value ? '/bookings' : '/login'" 
        class="flex flex-col items-center justify-center w-16 h-12 transition-colors group relative"
        :class="(route.path === '/bookings' || route.path === '/login') ? 'text-primary-container dark:text-white font-bold' : 'text-on-surface-variant dark:text-slate-400 hover:text-primary-container'"
      >
        <span class="material-symbols-outlined text-[22px]">
          {{ authStore.isAuthenticated.value ? 'event_available' : 'account_circle' }}
        </span>
        <span class="font-label-sm text-[11px] leading-tight mt-0.5">
          {{ authStore.isAuthenticated.value ? 'My Passes' : 'Sign In' }}
        </span>
        <span 
          class="transition-opacity w-1 h-1 rounded-full bg-secondary-container mt-0.5"
          :class="(route.path === '/bookings' || route.path === '/login') ? 'opacity-100' : 'opacity-0'"
        ></span>
      </router-link>
    </div>
  </nav>
</template>

<script setup>
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';

const route = useRoute();
const authStore = useAuthStore();
</script>
