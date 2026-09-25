<template>
  <div class="min-h-screen bg-surface flex flex-col font-sans selection:bg-secondary-container selection:text-on-secondary-container w-full min-w-0">
    <router-view />

    <!-- Global Toast Notification Component -->
    <transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="transform translate-y-4 opacity-0"
      enter-to-class="transform translate-y-0 opacity-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="transform translate-y-0 opacity-100"
      leave-to-class="transform translate-y-4 opacity-0"
    >
      <div 
        v-if="toastMessage" 
        class="fixed bottom-20 md:bottom-8 left-1/2 md:left-auto md:right-8 -translate-x-1/2 md:translate-x-0 max-w-sm w-[90%] sm:w-auto bg-primary text-on-primary px-4 py-3 rounded-full font-label-md text-xs sm:text-sm shadow-2xl flex items-center gap-2.5 z-[110] border border-primary-fixed-dim/30 pointer-events-none"
      >
        <span class="material-symbols-outlined text-[20px] text-tertiary-fixed shrink-0">
          {{ toastType === 'success' ? 'celebration' : (toastType === 'error' ? 'error' : 'info') }}
        </span>
        <span class="flex-1 text-center md:text-left font-medium truncate">{{ toastMessage }}</span>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { useBookingStore } from '@/stores/bookingStore';

const { toastMessage, toastType } = useBookingStore();
</script>
