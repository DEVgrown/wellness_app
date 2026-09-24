<template>
  <div class="bg-surface dark:bg-slate-950 text-on-surface dark:text-slate-100 flex flex-col min-h-screen transition-colors duration-200">
    <AppNavbar />

    <main class="flex-1 flex flex-col relative w-full pt-20 pb-24 md:pb-12 bg-surface dark:bg-slate-950">
      <div class="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-6">
        <!-- Welcoming Greeting Header Banner -->
        <section class="mb-8 flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-surface-container-lowest dark:bg-slate-900 p-6 rounded-3xl shadow-sm border border-outline-variant/30 dark:border-slate-800">
          <div class="flex items-center gap-4">
            <img 
              :src="authStore.user.value.avatar || user.avatar" 
              alt="Avatar" 
              class="w-16 h-16 rounded-full object-cover shadow-sm ring-4 ring-secondary/20 shrink-0"
            />
            <div>
              <div class="flex items-center gap-2">
                <h1 class="font-headline-lg text-2xl sm:text-3xl font-bold text-primary-container dark:text-white tracking-tight">
                  Welcome back, {{ authStore.user.value.name || user.name }}
                </h1>
                <span class="text-2xl">🌿</span>
              </div>
              <p class="font-body-md text-body-md text-on-surface-variant dark:text-slate-400 mt-0.5">
                "Honor your breath, nourish your energy, and move with intention today."
              </p>
            </div>
          </div>

          <div class="flex items-center gap-2.5 shrink-0">
            <router-link 
              to="/book" 
              class="inline-flex items-center gap-2 bg-primary-container hover:bg-primary text-on-primary font-label-md text-label-md px-5 py-2.5 rounded-full shadow-sm font-semibold transition-all active:scale-[0.98]"
            >
              <span class="material-symbols-outlined text-lg">calendar_add_on</span>
              <span>Book Session</span>
            </router-link>
            <router-link 
              to="/services" 
              class="inline-flex items-center gap-2 bg-surface-container-low dark:bg-slate-800 text-primary-container dark:text-white hover:bg-surface-container font-label-md text-label-md px-4 py-2.5 rounded-full transition-all border border-outline-variant/30 dark:border-slate-700 font-semibold"
            >
              <span>Explore</span>
            </router-link>
          </div>
        </section>

        <!-- 2-Column Responsive Desktop Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          <!-- LEFT COLUMN: Upcoming Session & Somatic Movement (7 Cols) -->
          <div class="lg:col-span-7 flex flex-col gap-6">
            <!-- Next Upcoming Session Card -->
            <div class="relative bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 sm:p-8 shadow-md border border-outline-variant/30 dark:border-slate-800 overflow-hidden">
              <div class="absolute -right-12 -top-12 w-48 h-48 rounded-full bg-secondary-fixed/40 dark:bg-sky-900/20 blur-3xl pointer-events-none"></div>

              <div class="flex items-start justify-between relative z-10 mb-4">
                <div>
                  <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-secondary-container/40 dark:bg-sky-950/60 text-primary-container dark:text-sky-300 font-label-sm text-label-sm font-semibold mb-2">
                    <span class="material-symbols-outlined text-sm text-secondary">verified</span>
                    <span>Confirmed Session</span>
                  </div>
                  <h2 class="font-headline-lg text-2xl font-bold text-primary-container dark:text-white">
                    1:1 Pilates Reformer &amp; Alignment
                  </h2>
                  <p class="font-body-sm text-body-sm text-on-surface-variant dark:text-slate-400">
                    With Lead Coach Karina • Tree Lane Studio Sanctuary
                  </p>
                </div>

                <div class="w-16 h-16 rounded-2xl bg-surface-container dark:bg-slate-800 flex flex-col items-center justify-center shrink-0 shadow-sm border border-outline-variant/20 dark:border-slate-700">
                  <span class="font-eyebrow text-[10px] text-secondary uppercase font-bold tracking-wider">TOMORROW</span>
                  <span class="font-headline-sm text-xl font-bold text-primary-container dark:text-white mt-0.5">09:30</span>
                </div>
              </div>

              <!-- Location & Apparatus Details Banner -->
              <div class="bg-surface-container-low dark:bg-slate-800/80 rounded-2xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
                <div class="flex items-center gap-3">
                  <span class="material-symbols-outlined text-secondary text-2xl">location_on</span>
                  <div>
                    <p class="font-label-md text-label-md text-primary-container dark:text-white font-semibold">Karen Studio, Nairobi</p>
                    <p class="font-body-sm text-body-sm text-on-surface-variant dark:text-slate-400">09:30 AM – 10:25 AM (EAT) • Allegro 2 Reformer</p>
                  </div>
                </div>
                <span class="inline-flex items-center px-3 py-1 rounded-full bg-surface-container-highest dark:bg-slate-700 text-on-secondary-fixed-variant dark:text-slate-200 font-label-sm text-label-sm font-semibold">
                  Suite 02
                </span>
              </div>

              <!-- Coach Preparation Note -->
              <div class="p-3.5 rounded-2xl bg-surface dark:bg-slate-800/40 border border-outline-variant/20 dark:border-slate-700 mb-6 flex items-start gap-3">
                <span class="material-symbols-outlined text-secondary text-lg mt-0.5">tips_and_updates</span>
                <p class="font-body-sm text-body-sm text-on-surface-variant dark:text-slate-300">
                  <strong class="text-primary-container dark:text-white font-semibold">Karina's Note:</strong> "We will focus on thoracic rotation and decompressing the lower lumbar spine. Wear comfortable movement wear and grip socks."
                </p>
              </div>

              <!-- Card Actions -->
              <div class="flex flex-wrap items-center gap-3 pt-2 border-t border-outline-variant/20 dark:border-slate-800">
                <router-link 
                  to="/bookings" 
                  class="flex-1 sm:flex-initial inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-full bg-primary-container text-on-primary font-label-md text-label-md font-semibold shadow-sm hover:bg-primary transition-all"
                >
                  <span class="material-symbols-outlined text-sm">schedule</span>
                  <span>Manage / Reschedule</span>
                </router-link>
                <a 
                  href="https://wa.me/254712345678" 
                  target="_blank"
                  class="flex-1 sm:flex-initial inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-full bg-surface-container-low dark:bg-slate-800 text-on-surface dark:text-slate-200 hover:text-primary-container font-label-md text-label-md font-semibold transition-all border border-outline-variant/30 dark:border-slate-700"
                >
                  <span class="material-symbols-outlined text-sm text-emerald-600">chat</span>
                  <span>WhatsApp Karina</span>
                </a>
              </div>
            </div>

            <!-- Daily Somatic Routine Cards -->
            <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 sm:p-8 shadow-sm border border-outline-variant/30 dark:border-slate-800">
              <div class="flex items-center justify-between mb-4">
                <div>
                  <span class="font-eyebrow text-eyebrow text-secondary uppercase tracking-wider block">Home Movement Rx</span>
                  <h3 class="font-headline-sm text-xl font-bold text-primary-container dark:text-white">Daily Somatic Focus</h3>
                </div>
                <span class="font-label-sm text-label-sm text-secondary font-semibold">Phase 2 Focus</span>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div class="p-4 rounded-2xl bg-surface dark:bg-slate-800/60 border border-outline-variant/20 dark:border-slate-700 flex flex-col justify-between">
                  <div>
                    <span class="material-symbols-outlined text-secondary text-2xl mb-1">wb_twilight</span>
                    <h4 class="font-label-md text-label-md font-semibold text-primary-container dark:text-white">Morning Pelvic Breath</h4>
                    <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400 mt-1">10 min diaphragmatic rib cage activation.</p>
                  </div>
                  <span class="font-label-sm text-xs text-secondary font-medium mt-3 block">Completed ✓</span>
                </div>

                <div class="p-4 rounded-2xl bg-surface dark:bg-slate-800/60 border border-outline-variant/20 dark:border-slate-700 flex flex-col justify-between">
                  <div>
                    <span class="material-symbols-outlined text-secondary text-2xl mb-1">sunny</span>
                    <h4 class="font-label-md text-label-md font-semibold text-primary-container dark:text-white">Mid-day Spine Elongation</h4>
                    <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400 mt-1">6 min seated cat-cow &amp; thoracic opening.</p>
                  </div>
                  <span class="font-label-sm text-xs text-on-surface-variant dark:text-slate-400 font-medium mt-3 block">In 2 hours</span>
                </div>

                <div class="p-4 rounded-2xl bg-surface dark:bg-slate-800/60 border border-outline-variant/20 dark:border-slate-700 flex flex-col justify-between">
                  <div>
                    <span class="material-symbols-outlined text-secondary text-2xl mb-1">bedtime</span>
                    <h4 class="font-label-md text-label-md font-semibold text-primary-container dark:text-white">Evening Legs-on-Wall</h4>
                    <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400 mt-1">8 min parasympathetic nervous down-regulation.</p>
                  </div>
                  <span class="font-label-sm text-xs text-on-surface-variant dark:text-slate-400 font-medium mt-3 block">Before bed</span>
                </div>
              </div>
            </div>
          </div>

          <!-- RIGHT COLUMN: Pass Tracker & Schedule Overview (5 Cols) -->
          <div class="lg:col-span-5 flex flex-col gap-6">
            <!-- Active Wellness Pass Card -->
            <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 sm:p-8 shadow-md border border-outline-variant/30 dark:border-slate-800">
              <div class="flex items-center justify-between mb-4">
                <div>
                  <span class="font-eyebrow text-eyebrow text-secondary uppercase tracking-wider block">Membership</span>
                  <h3 class="font-headline-sm text-xl font-bold text-primary-container dark:text-white">Reformer Pass (5 Pack)</h3>
                </div>
                <div class="w-12 h-12 rounded-full bg-secondary-fixed dark:bg-slate-800 flex items-center justify-center text-primary dark:text-sky-300 font-bold text-lg">
                  3/5
                </div>
              </div>

              <!-- Remaining Sessions Token Pills -->
              <p class="font-body-sm text-body-sm text-on-surface-variant dark:text-slate-400 mb-3">
                You have <strong>3 sessions remaining</strong> on your current pass.
              </p>

              <div class="grid grid-cols-5 gap-2 mb-6">
                <div class="h-10 rounded-xl bg-primary-container text-white flex items-center justify-center font-bold text-xs shadow-xs" title="Session 1 Completed">
                  ✓
                </div>
                <div class="h-10 rounded-xl bg-primary-container text-white flex items-center justify-center font-bold text-xs shadow-xs" title="Session 2 Completed">
                  ✓
                </div>
                <div class="h-10 rounded-xl bg-secondary dark:bg-sky-500 text-white dark:text-slate-950 flex items-center justify-center font-bold text-xs ring-2 ring-secondary/40" title="Session 3 Tomorrow">
                  3
                </div>
                <div class="h-10 rounded-xl bg-surface-container-low dark:bg-slate-800 text-on-surface-variant dark:text-slate-400 flex items-center justify-center font-bold text-xs border border-outline-variant/30" title="Session 4 Available">
                  4
                </div>
                <div class="h-10 rounded-xl bg-surface-container-low dark:bg-slate-800 text-on-surface-variant dark:text-slate-400 flex items-center justify-center font-bold text-xs border border-outline-variant/30" title="Session 5 Available">
                  5
                </div>
              </div>

              <div class="p-3.5 rounded-2xl bg-surface-container-low dark:bg-slate-800/60 flex items-center justify-between text-sm mb-6">
                <span class="text-on-surface-variant dark:text-slate-400">Pass Validity</span>
                <span class="font-semibold text-primary-container dark:text-white">Valid until 30 Nov 2026</span>
              </div>

              <router-link 
                to="/services" 
                class="w-full py-3.5 rounded-full bg-primary-container hover:bg-primary text-on-primary font-label-md text-label-md font-semibold shadow-md active:scale-[0.98] transition-all flex items-center justify-center gap-2"
              >
                <span>Renew / Top Up Pass (Save 15%)</span>
                <span class="material-symbols-outlined text-sm">arrow_forward</span>
              </router-link>
            </div>

            <!-- Hormone & Cycle Insight Card -->
            <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 shadow-sm border border-outline-variant/30 dark:border-slate-800">
              <div class="flex items-center gap-3 mb-3">
                <div class="w-10 h-10 rounded-full bg-secondary-container/40 dark:bg-sky-950/60 flex items-center justify-center text-primary-container dark:text-sky-300">
                  <span class="material-symbols-outlined">vital_signs</span>
                </div>
                <div>
                  <h4 class="font-label-lg text-label-lg font-bold text-primary-container dark:text-white">Hormone Rhythm</h4>
                  <span class="font-label-sm text-xs text-secondary font-medium">Phase: Mid-Follicular High Energy</span>
                </div>
              </div>
              <p class="font-body-sm text-body-sm text-on-surface-variant dark:text-slate-300 leading-relaxed mb-4">
                Estrogen is gently rising, boosting natural tendon resilience and metabolic endurance. An optimal window for progression on the Reformer and strength work!
              </p>
              <router-link to="/services/reformer" class="text-secondary hover:underline font-label-sm text-sm font-semibold flex items-center gap-1">
                Explore hormone coaching notes <span class="material-symbols-outlined text-xs">chevron_right</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </main>

    <AppBottomNav />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import AppNavbar from '@/components/AppNavbar.vue';
import AppBottomNav from '@/components/AppBottomNav.vue';
import { useBookingStore } from '@/stores/bookingStore';
import { useAuthStore } from '@/stores/authStore';

const bookingStore = useBookingStore();
const authStore = useAuthStore();
const user = bookingStore.user;
</script>
