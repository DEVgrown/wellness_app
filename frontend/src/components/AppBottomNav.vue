<template>
  <nav class="md:hidden fixed bottom-0 w-full z-50 pb-safe bg-surface/90 dark:bg-slate-900/90 backdrop-blur-xl shadow-[0_-4px_24px_rgba(10,42,94,0.06)] border-t border-outline-variant/20 dark:border-slate-800 transition-colors duration-200">
    <div class="max-w-md mx-auto flex justify-around items-center h-16 px-space-xs">
      <!-- Home Tab -->
      <router-link 
        to="/home" 
        class="flex flex-col items-center justify-center w-16 h-12 transition-colors group relative"
        :class="isActive('/home') ? 'text-primary-container font-semibold' : 'text-on-surface-variant hover:text-primary'"
      >
        <span class="material-symbols-outlined text-[24px]">spa</span>
        <span class="font-label-sm text-label-sm leading-tight mt-0.5">Home</span>
        <span 
          class="active-dot transition-opacity w-1 h-1 rounded-full bg-secondary-container mt-0.5"
          :class="isActive('/home') ? 'opacity-100' : 'opacity-0'"
        ></span>
      </router-link>

      <!-- Book / Services Tab -->
      <router-link 
        to="/services" 
        class="flex flex-col items-center justify-center w-20 h-12 transition-colors group relative"
        :class="isActive('/services') || isActive('/book') ? 'text-primary-container font-semibold' : 'text-on-surface-variant hover:text-primary'"
      >
        <span class="material-symbols-outlined text-[24px]">calendar_add_on</span>
        <span class="font-label-sm text-label-sm leading-tight mt-0.5">Book</span>
        <span 
          class="active-dot transition-opacity w-1 h-1 rounded-full bg-secondary-container mt-0.5"
          :class="isActive('/services') || isActive('/book') ? 'opacity-100' : 'opacity-0'"
        ></span>
      </router-link>

      <!-- My Bookings Tab -->
      <router-link 
        to="/bookings" 
        class="flex flex-col items-center justify-center w-20 h-12 transition-colors group relative"
        :class="isActive('/bookings') ? 'text-primary-container font-semibold' : 'text-on-surface-variant hover:text-primary'"
      >
        <span class="material-symbols-outlined text-[24px]">event_available</span>
        <span class="font-label-sm text-label-sm leading-tight mt-0.5">Bookings</span>
        <span 
          class="active-dot transition-opacity w-1 h-1 rounded-full bg-secondary-container mt-0.5"
          :class="isActive('/bookings') ? 'opacity-100' : 'opacity-0'"
        ></span>
      </router-link>

      <!-- Profile Tab -->
      <router-link 
        to="/bookings" 
        class="flex flex-col items-center justify-center w-20 h-12 transition-colors group relative"
        :class="isActive('/profile') ? 'text-primary-container font-semibold' : 'text-on-surface-variant hover:text-primary'"
      >
        <span class="material-symbols-outlined text-[24px]">tune</span>
        <span class="font-label-sm text-label-sm leading-tight mt-0.5">Profile</span>
        <span 
          class="active-dot transition-opacity w-1 h-1 rounded-full bg-secondary-container mt-0.5"
          :class="isActive('/profile') ? 'opacity-100' : 'opacity-0'"
        ></span>
      </router-link>
    </div>
  </nav>
</template>

<script setup>
import { useRoute } from 'vue-router';

const route = useRoute();

function isActive(path) {
  return route.path === path;
}
</script>
